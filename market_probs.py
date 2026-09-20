# market_probs.py — market-implied match probabilities for World Cup fixtures
#
# The simulator derives team strength from no-vig win/draw/loss probabilities
# for each group-stage fixture, pulled from The Odds API (https://the-odds-api.com).
# Set your key in the environment, never in code:
#
#   export ODDS_API_KEY=your_key_here

import os

import requests

BASE          = "https://api.the-odds-api.com/v4"
SPORT_MATCHES = "soccer_fifa_world_cup"
MARKET_SOURCE = "pinnacle"   # data provider key used for the market-implied lines

NAME_MAP = {
    "Bosnia & Herzegovina": "Bosnia",
    "Curaçao":              "Curacao",
    "Korea Republic":       "South Korea",
    "United States":        "USA",
    "Côte d'Ivoire":        "Ivory Coast",
    "Congo DR":             "DR Congo",
}


def get_api_key():
    key = os.environ.get("ODDS_API_KEY", "")
    if not key:
        raise RuntimeError("Set the ODDS_API_KEY environment variable")
    return key


def _get(endpoint, params=None):
    params = dict(params or {})
    params["apiKey"] = get_api_key()
    resp = requests.get(f"{BASE}{endpoint}", params=params, timeout=30)
    resp.raise_for_status()
    remaining = resp.headers.get("x-requests-remaining", "?")
    print(f"  [API] {endpoint} — {remaining} requests remaining")
    return resp.json()


def remove_vig(probs):
    """Normalize implied probabilities so they sum to 1."""
    total = sum(probs)
    if total == 0:
        return probs
    return [p / total for p in probs]


def american_to_prob(odds):
    """Convert American odds to implied probability (before normalization)."""
    if odds > 0:
        return 100 / (odds + 100)
    return abs(odds) / (abs(odds) + 100)


def get_match_probs():
    """
    Pull market-implied group-stage win/draw/loss probabilities.
    Returns dict: {(home, away): {"win": p, "draw": p, "loss": p}}
    """
    data = _get(f"/sports/{SPORT_MATCHES}/odds", {
        "regions":    "us",
        "markets":    "h2h",
        "bookmakers": MARKET_SOURCE,
        "oddsFormat": "american",
    })

    result = {}
    for event in data:
        home = NAME_MAP.get(event.get("home_team", ""), event.get("home_team", ""))
        away = NAME_MAP.get(event.get("away_team", ""), event.get("away_team", ""))
        sources = event.get("bookmakers", [])
        if not sources:
            continue

        markets = sources[0].get("markets", [])
        h2h = next((m for m in markets if m["key"] == "h2h"), None)
        if not h2h:
            continue

        outcomes = {o["name"]: american_to_prob(o["price"]) for o in h2h["outcomes"]}
        raw = [outcomes.get(home, 0), outcomes.get("Draw", 0), outcomes.get(away, 0)]
        win, draw, loss = remove_vig(raw)
        result[(home, away)] = {"win": win, "draw": draw, "loss": loss}

    print(f"  Pulled market-implied probabilities for {len(result)} matches")
    return result
