# simulator.py
# Monte Carlo World Cup simulator.
#
# Team quality is derived entirely from market-implied head-to-head match
# probabilities (no hand-set ratings). The only model signal layered on top
# of those probabilities is the heat and crowd adjustment.
#
# Architecture:
#   1. For each group fixture with a market line:
#      - Use the no-vig win/draw/loss probabilities as the base
#      - Apply heat shift based on venue + kickoff time + squad heat profile
#   2. For knockout fixtures (no market line yet):
#      - Extract implicit team strength from the group stage probabilities
#      - Use Bradley-Terry model for matchup probabilities
#      - Apply heat shift for venue/time when known
#   3. Simulate goal counts via Poisson conditioned on the outcome
#      - Needed for group stage tiebreakers (GD, GF)

import math
import random
from collections import defaultdict

import numpy as np

from config  import GROUPS, FIXTURES, VENUE_HEAT, HEAT_TOLERANCE
from bracket import assign_r32_teams, BRACKET_MATCHES

# ── Manual fallback probabilities for fixtures with no market line yet ────────
# Hand-entered consensus estimates — replace once a market line is available
MANUAL_FIXTURE_PROBS = {
    ("Germany",  "Curacao"):    {"win": 0.919, "draw": 0.057, "loss": 0.024},
    ("Spain",    "Cape Verde"): {"win": 0.867, "draw": 0.092, "loss": 0.041},
    ("Brazil",   "Haiti"):      {"win": 0.892, "draw": 0.079, "loss": 0.028},
}

# ── Constants ─────────────────────────────────────────────────────────────────
N_SIMS       = 50_000
AVG_GOALS    = 1.30    # average WC goals per team per game (for Poisson draw)
MAX_GOALS    = 10
HEAT_WEIGHT  = 0.10    # max probability shift from heat per unit of heat_advantage
                       # tune this after seeing calibrated output


# ── Crowd advantage (knockout only — group stage lines already reflect it) ─
# Venue sets for each host nation's home-crowd effect
_MEX_FULL    = {"Los Angeles", "Dallas", "Houston", "Kansas City", "Atlanta",
                "Miami", "Philadelphia", "New Jersey"}
_MEX_PARTIAL = {"Seattle", "Foxborough", "Santa Clara"}
_MEX_MINIMAL = {"Toronto", "Vancouver"}
_USA_HOME    = {"Los Angeles", "Dallas", "Houston", "Kansas City", "Atlanta",
                "Miami", "Philadelphia", "New Jersey", "Seattle", "Foxborough",
                "Santa Clara"}

def crowd_advantage_shift(team_a, team_b, venue):
    """
    Returns a probability delta to add to P(team_a wins) based on crowd advantage.
    Only applied in knockout stage — group stage lines already have this priced in.
    """
    delta = 0.0

    for home_team, away_team in [(team_a, team_b), (team_b, team_a)]:
        sign = 1.0 if home_team == team_a else -1.0

        if home_team == "Mexico" and away_team != "USA":
            if venue in _MEX_FULL:
                delta += sign * 0.05
            elif venue in _MEX_PARTIAL:
                delta += sign * 0.03
            elif venue in _MEX_MINIMAL:
                delta += sign * 0.02

        elif home_team == "USA" and away_team != "Mexico":
            if venue in _USA_HOME:
                delta += sign * 0.04

        elif home_team == "Canada":
            if venue not in _MEX_FULL | _MEX_PARTIAL | _MEX_MINIMAL | _USA_HOME:
                delta += sign * 0.01  # Canadian venues only (group stage already handled)
            else:
                delta += sign * 0.01  # small traveling fanbase in US venues

    return delta


# ── Heat adjustment ───────────────────────────────────────────────────────────

def _time_heat_factor(local_time_str):
    """Return heat intensity multiplier based on local kickoff hour."""
    try:
        hour = int(local_time_str.split(":")[0])
    except Exception:
        return 0.4
    if hour < 12:
        return 0.25
    elif hour < 17:
        return 1.00    # peak afternoon
    elif hour < 20:
        return 0.55
    else:
        return 0.18


def heat_prob_shift(home, away, fixture):
    """
    Returns a probability delta to add to P(home win).
    Positive = heat benefits home team more.
    Negative = heat benefits away team more.
    """
    venue        = fixture.get("venue", "TBD")
    venue_heat   = VENUE_HEAT.get(venue, 0.5)
    time_factor  = _time_heat_factor(fixture.get("local_time", "19:00"))
    intensity    = venue_heat * time_factor

    tol_h = HEAT_TOLERANCE.get(home, 0.0)
    tol_a = HEAT_TOLERANCE.get(away, 0.0)

    return (tol_h - tol_a) * intensity * HEAT_WEIGHT


# ── Market probability extraction ─────────────────────────────────────────────

def _no_vig(raw_probs):
    """Strip vig from a list of implied probabilities."""
    total = sum(raw_probs)
    if total == 0:
        return [1 / len(raw_probs)] * len(raw_probs)
    return [p / total for p in raw_probs]


def extract_fixture_probs(market_probs):
    """
    Build a lookup of no-vig probabilities per fixture from market-implied probabilities.
    market_probs: {(home, away): {win, draw, loss}} from market_probs.py (already no-vig)
    Returns: {(home, away): (win, draw, loss)}
    """
    probs = {}
    for (home, away), p in market_probs.items():
        probs[(home, away)] = (p["win"], p["draw"], p["loss"])

    # Fill missing fixtures with the manual fallback probabilities
    for (home, away), p in MANUAL_FIXTURE_PROBS.items():
        if (home, away) not in probs:
            probs[(home, away)] = (p["win"], p["draw"], p["loss"])
            print(f"  [Manual override] {home} vs {away} — using manual fallback probabilities")

    return probs


def extract_team_strength(market_probs):
    """
    Derive implicit team strength from the group stage probabilities.
    Strength = geometric mean of (P_win + 0.5 * P_draw) across each team's group games.
    Used as Bradley-Terry parameter for knockout simulation.
    Returns: {team: strength_float}
    """
    scores = defaultdict(list)

    for (home, away), p in market_probs.items():
        scores[home].append(p["win"]  + 0.5 * p["draw"])
        scores[away].append(p["loss"] + 0.5 * p["draw"])

    strength = {}
    for team, vals in scores.items():
        # Geometric mean — avoids a single easy matchup inflating strength
        log_mean = sum(math.log(max(v, 1e-6)) for v in vals) / len(vals)
        strength[team] = math.exp(log_mean)

    # Fill any teams missing from the market data with a low default
    all_teams = {t for grp in GROUPS.values() for t in grp}
    min_strength = min(strength.values()) * 0.5 if strength else 0.05
    for team in all_teams:
        if team not in strength:
            strength[team] = min_strength

    return strength


# ── Goal simulation ───────────────────────────────────────────────────────────

def _poisson_pmf(k, lam):
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    return math.exp(-lam) * (lam ** k) / math.factorial(k)


def _sample_goals_given_outcome(outcome, avg=AVG_GOALS):
    """
    Sample (home_goals, away_goals) conditioned on outcome.
    outcome: 'H' = home win, 'D' = draw, 'A' = away win
    """
    if outcome == "D":
        g = max(0, np.random.poisson(avg * 0.85))
        return g, g
    elif outcome == "H":
        while True:
            h = np.random.poisson(avg * 1.1)
            a = np.random.poisson(avg * 0.85)
            if h > a:
                return h, a
    else:  # Away win
        while True:
            h = np.random.poisson(avg * 0.85)
            a = np.random.poisson(avg * 1.1)
            if a > h:
                return h, a


# ── Single match simulation ───────────────────────────────────────────────────

def simulate_match(home, away, fixture, fixture_probs, team_strength=None, extra_shift=0.0):
    """
    Simulate one match. Returns (home_goals, away_goals).

    fixture_probs:  {(home,away): (win,draw,loss)} from the market data
    team_strength:  {team: float} for matches without a market line
    extra_shift:    additional probability delta to add to P(home win) e.g. crowd advantage
    """
    # Get base probabilities
    base = fixture_probs.get((home, away))
    if base is None:
        # No market line — use strength-based Bradley-Terry
        if team_strength:
            sh = team_strength.get(home, 0.1)
            sa = team_strength.get(away, 0.1)
            p_win  = sh / (sh + sa) * 0.75   # scale down for draw possibility
            p_loss = sa / (sh + sa) * 0.75
            p_draw = 1 - p_win - p_loss
        else:
            p_win = p_draw = p_loss = 1/3
    else:
        p_win, p_draw, p_loss = base

    # Heat + crowd adjustment
    shift = heat_prob_shift(home, away, fixture) + extra_shift
    p_win_adj  = max(0.01, min(0.95, p_win  + shift))
    p_loss_adj = max(0.01, min(0.95, p_loss - shift))
    total      = p_win_adj + p_draw + p_loss_adj
    p_win_adj  /= total
    p_draw_adj  = p_draw / total
    p_loss_adj /= total

    # Sample outcome
    r = random.random()
    if r < p_win_adj:
        outcome = "H"
    elif r < p_win_adj + p_draw_adj:
        outcome = "D"
    else:
        outcome = "A"

    return _sample_goals_given_outcome(outcome)


# ── Group stage simulation ────────────────────────────────────────────────────

def simulate_group_stage(fixture_probs, team_strength=None):
    """
    Simulate one full group stage.
    Returns {group: [(pts, gd, gf, team), ...]} sorted best→worst.
    """
    group_fixtures = defaultdict(list)
    for f in FIXTURES:
        group_fixtures[f["group"]].append(f)

    standings = {}

    for grp, teams in GROUPS.items():
        pts = defaultdict(int)
        gd  = defaultdict(int)
        gf  = defaultdict(int)

        for f in group_fixtures[grp]:
            home, away = f["home"], f["away"]
            hg, ag = simulate_match(home, away, f, fixture_probs, team_strength)

            gf[home] += hg
            gf[away] += ag
            gd[home] += hg - ag
            gd[away] += ag - hg

            if hg > ag:
                pts[home] += 3
            elif hg == ag:
                pts[home] += 1
                pts[away] += 1
            else:
                pts[away] += 3

        table = sorted(teams, key=lambda t: (pts[t], gd[t], gf[t]), reverse=True)
        standings[grp] = [(pts[t], gd[t], gf[t], t) for t in table]

    return standings


# ── Qualifier selection ───────────────────────────────────────────────────────

def get_qualifiers(standings):
    """
    Top 2 from each of 12 groups (24 teams) + 8 best 3rd-place = 32 qualifiers.
    Returns {team: {pos, group, pts, gd, gf}}
    """
    result = {}
    thirds = []

    for grp, table in standings.items():
        result[table[0][3]] = {"pos": 1,      "group": grp, "pts": table[0][0], "gd": table[0][1], "gf": table[0][2]}
        result[table[1][3]] = {"pos": 2,      "group": grp, "pts": table[1][0], "gd": table[1][1], "gf": table[1][2]}
        thirds.append(        {"team": table[2][3], "group": grp, "pts": table[2][0], "gd": table[2][1], "gf": table[2][2]})
        result[table[3][3]] = {"pos": 4,      "group": grp, "pts": table[3][0], "gd": table[3][1], "gf": table[3][2]}

    thirds_sorted = sorted(thirds, key=lambda x: (x["pts"], x["gd"], x["gf"]), reverse=True)
    for i, t in enumerate(thirds_sorted):
        pos = "3rd_q" if i < 8 else "3rd_out"
        result[t["team"]] = {"pos": pos, "group": t["group"], "pts": t["pts"], "gd": t["gd"], "gf": t["gf"]}

    return result


# ── Knockout simulation ───────────────────────────────────────────────────────

def _ko_match(team_a, team_b, fixture, fixture_probs, team_strength):
    """Simulate a single knockout match (no draws — extra time/pens if needed)."""
    # Apply crowd advantage on top of heat (knockout only)
    venue = fixture.get("venue", "Neutral")
    crowd_shift = crowd_advantage_shift(team_a, team_b, venue)

    for _ in range(15):
        hg, ag = simulate_match(team_a, team_b, fixture, fixture_probs, team_strength,
                                extra_shift=crowd_shift)
        if hg != ag:
            return team_a if hg > ag else team_b
    # Penalties: weighted coin flip using strength
    sh = team_strength.get(team_a, 0.1)
    sa = team_strength.get(team_b, 0.1)
    return team_a if random.random() < sh / (sh + sa) else team_b


# When a team WINS a match, they're entering the next round (temp label, overwritten later).
# When a team LOSES a match, they exit at that round (final label).
_ENTERING_ROUND = {"R32": "R16", "R16": "QF", "QF": "SF", "SF": "Final", "Final": "Winner"}
_EXITING_ROUND  = {"R32": "R32", "R16": "R16", "QF": "QF", "SF": "SF",   "Final": "Final"}


def simulate_knockout(qualifiers, standings, fixture_probs, team_strength):
    """
    Simulate full knockout bracket R32 → Final using the official 2026 WC bracket.
    Each match uses its real venue + local kickoff time so heat fires correctly.
    Returns {team: round_reached}
    """
    slot_map      = assign_r32_teams(standings, qualifiers)
    match_winners = {}   # match_id → winning team
    round_reached = {}

    def _resolve(slot):
        if slot.startswith("W"):
            return match_winners.get(int(slot[1:]))
        return slot_map.get(slot)

    for m in BRACKET_MATCHES:
        team_a = _resolve(m["a"])
        team_b = _resolve(m["b"])

        if not team_a or not team_b:
            # Should only happen if a prior match is missing a winner — skip gracefully
            continue

        fixture = {"venue": m["venue"], "local_time": m["local_time"]}
        winner  = _ko_match(team_a, team_b, fixture, fixture_probs, team_strength)
        loser   = team_b if winner == team_a else team_a

        match_winners[m["id"]] = winner
        round_reached[winner]  = _ENTERING_ROUND[m["round"]]
        round_reached[loser]   = _EXITING_ROUND[m["round"]]

    return round_reached


# ── Full tournament Monte Carlo ───────────────────────────────────────────────

def run_tournament(n_sims=N_SIMS, market_probs=None):
    """
    Run full Monte Carlo simulation.
    market_probs: {(home,away): {win,draw,loss}} from market_probs.py
    Returns {team: {advance, group_win, group_2nd, R16, QF, SF, Final, Winner}}
    """
    all_teams = {t for grp in GROUPS.values() for t in grp}
    counts = {t: defaultdict(int) for t in all_teams}

    if not market_probs:
        print("  Warning: no market probabilities — simulation will use equal probabilities")
        fixture_probs = {}
        team_strength = {t: 0.5 for t in all_teams}
    else:
        fixture_probs = extract_fixture_probs(market_probs)
        team_strength = extract_team_strength(market_probs)
        print(f"  Market lines loaded: {len(fixture_probs)} fixtures")
        print(f"  Top 5 by strength: {sorted(team_strength, key=team_strength.get, reverse=True)[:5]}")

    print(f"Running {n_sims:,} simulations...")

    for i in range(n_sims):
        if (i + 1) % 10_000 == 0:
            print(f"  {i+1:,} / {n_sims:,}")

        standings  = simulate_group_stage(fixture_probs, team_strength)
        qualifiers = get_qualifiers(standings)

        for team, info in qualifiers.items():
            pos = info["pos"]
            if pos in (1, 2, "3rd_q"):
                counts[team]["advance"] += 1
            if pos == 1:
                counts[team]["group_win"] += 1
            elif pos == 2:
                counts[team]["group_2nd"] += 1
            elif pos == 4:
                counts[team]["group_last"] += 1

        round_reached = simulate_knockout(qualifiers, standings, fixture_probs, team_strength)

        for team, rnd in round_reached.items():
            if rnd in ("R16", "QF", "SF", "Final", "Winner"):
                counts[team]["R16"] += 1
            if rnd in ("QF", "SF", "Final", "Winner"):
                counts[team]["QF"] += 1
            if rnd in ("SF", "Final", "Winner"):
                counts[team]["SF"] += 1
            if rnd in ("Final", "Winner"):
                counts[team]["Final"] += 1
            if rnd == "Winner":
                counts[team]["Winner"] += 1

    probs = {team: {k: v / n_sims for k, v in counts[team].items()} for team in all_teams}
    return probs
