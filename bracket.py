# bracket.py — Official 2026 WC knockout bracket structure
#
# All 32 knockout matches with:
#   - which group positions feed each slot (1A, 2B, 3rd_pool, Wxx)
#   - venue + local kickoff time for heat calculation
#
# Local times converted from BST (UK) sources:
#   EDT venues: BST - 5h  |  CDT venues: BST - 6h  |  PDT venues: BST - 8h

# ── Round of 32 slot definitions ──────────────────────────────────────────────
# slot format:
#   "1A"           = Group A winner
#   "2B"           = Group B runner-up
#   "3rd_ABCDF"    = best 3rd-place qualifier from groups A,B,C,D,F pool

BRACKET_MATCHES = [
    # ── Round of 32 ───────────────────────────────────────────────────────────
    {"id": 73,  "round": "R32",   "a": "2A",    "b": "2B",          "date": "2026-06-28", "local_time": "12:00", "venue": "Los Angeles"},
    {"id": 74,  "round": "R32",   "a": "1E",    "b": "3rd_ABCDF",   "date": "2026-06-29", "local_time": "16:30", "venue": "Foxborough"},
    {"id": 76,  "round": "R32",   "a": "1C",    "b": "2F",          "date": "2026-06-29", "local_time": "12:00", "venue": "Houston"},
    {"id": 75,  "round": "R32",   "a": "1F",    "b": "2C",          "date": "2026-06-29", "local_time": "20:00", "venue": "Monterrey"},
    {"id": 77,  "round": "R32",   "a": "1I",    "b": "3rd_CDFGH",   "date": "2026-06-30", "local_time": "17:00", "venue": "New Jersey"},
    {"id": 78,  "round": "R32",   "a": "2E",    "b": "2I",          "date": "2026-06-30", "local_time": "12:00", "venue": "Dallas"},
    {"id": 79,  "round": "R32",   "a": "1A",    "b": "3rd_CEFHI",   "date": "2026-06-30", "local_time": "20:00", "venue": "Mexico City"},
    {"id": 80,  "round": "R32",   "a": "1L",    "b": "3rd_EHIJK",   "date": "2026-07-01", "local_time": "12:00", "venue": "Atlanta"},
    {"id": 81,  "round": "R32",   "a": "1D",    "b": "3rd_BEFIJ",   "date": "2026-07-01", "local_time": "17:00", "venue": "Santa Clara"},
    {"id": 82,  "round": "R32",   "a": "1G",    "b": "3rd_AEHIJ",   "date": "2026-07-01", "local_time": "13:00", "venue": "Seattle"},
    {"id": 83,  "round": "R32",   "a": "2K",    "b": "2L",          "date": "2026-07-02", "local_time": "19:00", "venue": "Toronto"},
    {"id": 84,  "round": "R32",   "a": "1H",    "b": "2J",          "date": "2026-07-02", "local_time": "12:00", "venue": "Los Angeles"},
    {"id": 85,  "round": "R32",   "a": "1B",    "b": "3rd_EFGIJ",   "date": "2026-07-02", "local_time": "20:00", "venue": "Vancouver"},
    {"id": 86,  "round": "R32",   "a": "1J",    "b": "2H",          "date": "2026-07-03", "local_time": "18:00", "venue": "Miami"},
    {"id": 87,  "round": "R32",   "a": "1K",    "b": "3rd_DEIJL",   "date": "2026-07-03", "local_time": "20:30", "venue": "Kansas City"},
    {"id": 88,  "round": "R32",   "a": "2D",    "b": "2G",          "date": "2026-07-03", "local_time": "13:00", "venue": "Dallas"},
    # ── Round of 16 ───────────────────────────────────────────────────────────
    {"id": 89,  "round": "R16",   "a": "W74",   "b": "W77",         "date": "2026-07-04", "local_time": "17:00", "venue": "Philadelphia"},
    {"id": 90,  "round": "R16",   "a": "W73",   "b": "W75",         "date": "2026-07-04", "local_time": "12:00", "venue": "Houston"},
    {"id": 91,  "round": "R16",   "a": "W76",   "b": "W78",         "date": "2026-07-05", "local_time": "16:00", "venue": "New Jersey"},
    {"id": 92,  "round": "R16",   "a": "W79",   "b": "W80",         "date": "2026-07-05", "local_time": "19:00", "venue": "Mexico City"},
    {"id": 93,  "round": "R16",   "a": "W83",   "b": "W84",         "date": "2026-07-06", "local_time": "14:00", "venue": "Dallas"},
    {"id": 94,  "round": "R16",   "a": "W81",   "b": "W82",         "date": "2026-07-06", "local_time": "17:00", "venue": "Seattle"},
    {"id": 95,  "round": "R16",   "a": "W86",   "b": "W88",         "date": "2026-07-07", "local_time": "12:00", "venue": "Atlanta"},
    {"id": 96,  "round": "R16",   "a": "W85",   "b": "W87",         "date": "2026-07-07", "local_time": "13:00", "venue": "Vancouver"},
    # ── Quarter-finals ────────────────────────────────────────────────────────
    {"id": 97,  "round": "QF",    "a": "W89",   "b": "W90",         "date": "2026-07-09", "local_time": "16:00", "venue": "Foxborough"},
    {"id": 98,  "round": "QF",    "a": "W93",   "b": "W94",         "date": "2026-07-10", "local_time": "12:00", "venue": "Los Angeles"},
    {"id": 99,  "round": "QF",    "a": "W91",   "b": "W92",         "date": "2026-07-11", "local_time": "17:00", "venue": "Miami"},
    {"id": 100, "round": "QF",    "a": "W95",   "b": "W96",         "date": "2026-07-11", "local_time": "20:00", "venue": "Kansas City"},
    # ── Semi-finals ───────────────────────────────────────────────────────────
    {"id": 101, "round": "SF",    "a": "W97",   "b": "W98",         "date": "2026-07-14", "local_time": "14:00", "venue": "Dallas"},
    {"id": 102, "round": "SF",    "a": "W99",   "b": "W100",        "date": "2026-07-15", "local_time": "15:00", "venue": "Atlanta"},
    # ── Final ─────────────────────────────────────────────────────────────────
    {"id": 104, "round": "Final", "a": "W101",  "b": "W102",        "date": "2026-07-19", "local_time": "15:00", "venue": "New Jersey"},
]

# ── 3rd-place pool assignment ─────────────────────────────────────────────────
# Maps each R32 3rd-place slot to the groups that feed it
THIRD_PLACE_POOLS = {
    "3rd_ABCDF": list("ABCDF"),
    "3rd_CDFGH": list("CDFGH"),
    "3rd_CEFHI": list("CEFHI"),
    "3rd_EHIJK": list("EHIJK"),
    "3rd_BEFIJ": list("BEFIJ"),
    "3rd_AEHIJ": list("AEHIJ"),
    "3rd_EFGIJ": list("EFGIJ"),
    "3rd_DEIJL": list("DEIJL"),
}


def assign_r32_teams(standings, qualifiers):
    """
    Map group positions to actual teams for every R32 slot.

    standings:  {group: [(pts, gd, gf, team), ...]}  sorted best→worst
    qualifiers: {team: {pos, group, pts, gd, gf}}

    Returns: {slot_key: team}  e.g. {"1A": "France", "2B": "Canada", ...}
    """
    slot_map = {}

    # Group winners and runners-up — straightforward
    for grp, table in standings.items():
        slot_map[f"1{grp}"] = table[0][3]
        slot_map[f"2{grp}"] = table[1][3]

    # Collect all 3rd-place teams and their rank (already sorted in qualifiers)
    thirds = [
        (t, info)
        for t, info in qualifiers.items()
        if info["pos"] in ("3rd_q", "3rd_out")
    ]
    # Sort by pts desc, then gd desc, then gf desc
    thirds_sorted = sorted(thirds, key=lambda x: (x[1]["pts"], x[1]["gd"], x[1]["gf"]), reverse=True)
    qualified_thirds = [t for t, info in thirds_sorted if info["pos"] == "3rd_q"]

    # Assign 3rd-place teams to pool slots
    # Each slot takes the best available 3rd-place from that pool
    pool_order = [
        "3rd_ABCDF",
        "3rd_CDFGH",
        "3rd_CEFHI",
        "3rd_EHIJK",
        "3rd_BEFIJ",
        "3rd_AEHIJ",
        "3rd_EFGIJ",
        "3rd_DEIJL",
    ]

    used = set()
    for pool_key in pool_order:
        eligible_groups = THIRD_PLACE_POOLS[pool_key]
        # Find best unassigned 3rd-place team from eligible groups
        assigned = False
        for team in qualified_thirds:
            if team in used:
                continue
            team_group = qualifiers[team]["group"]
            if team_group in eligible_groups:
                slot_map[pool_key] = team
                used.add(team)
                assigned = True
                break
        if not assigned:
            # Fallback: best unassigned 3rd-place regardless of pool
            for team in qualified_thirds:
                if team not in used:
                    slot_map[pool_key] = team
                    used.add(team)
                    break

    return slot_map


def build_knockout_bracket(slot_map):
    """
    Build the full knockout schedule with actual teams substituted in.
    Returns list of match dicts with home/away team names resolved.
    """
    match_winners = {}   # match_id → winning team (filled in as we simulate)
    resolved = []

    for m in BRACKET_MATCHES:
        match = m.copy()
        match["team_a"] = slot_map.get(m["a"], m["a"])   # fallback to slot label if unresolved
        match["team_b"] = slot_map.get(m["b"], m["b"])
        resolved.append(match)

    return resolved
