#!/usr/bin/env python3
"""
main.py — World Cup 2026 tournament simulator runner
Pulls market-implied match probabilities, runs a Monte Carlo tournament
simulation, and writes per-team advancement probabilities.

Usage:
    python main.py                # full run (50k sims)
    python main.py --sims 5000    # quick test
    python main.py --no-market    # skip the API call (equal-strength baseline)
"""

import argparse

import pandas as pd

from market_probs import get_match_probs
from simulator    import run_tournament, N_SIMS
from config       import GROUPS

OUTPUT_CSV = "model_probs.csv"


def get_group_for_team(team):
    for grp, teams in GROUPS.items():
        if team in teams:
            return grp
    return "?"


def print_summary(sim_probs):
    """Print top model probabilities per stage to console."""
    stages = [
        ("Winner",     "Winner"),
        ("Final",      "Final"),
        ("SF",         "Semi-final"),
        ("QF",         "Quarter-final"),
        ("R16",        "Round of 16"),
        ("advance",    "Advance from group"),
        ("group_win",  "Group win"),
        ("group_last", "Finish last"),
    ]

    for key, label in stages:
        ranked = sorted(
            [(t, p.get(key, 0)) for t, p in sim_probs.items()],
            key=lambda x: x[1], reverse=True
        )[:10]
        print(f"\n── Top 10: {label} ──")
        for team, prob in ranked:
            if prob < 0.005:
                break
            print(f"  {team:<20} ({get_group_for_team(team)})  {prob*100:5.1f}%")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sims",      type=int, default=N_SIMS)
    parser.add_argument("--no-market", action="store_true", help="Skip the market probability API call")
    args = parser.parse_args()

    # ── 1. Pull market-implied match probabilities ────────────────────────────
    market_probs = None
    if not args.no_market:
        print("Pulling market-implied match probabilities...")
        try:
            market_probs = get_match_probs()
        except Exception as e:
            print(f"  Warning: could not pull market probabilities ({e}) — using equal-strength baseline")

    # ── 2. Run tournament simulation ──────────────────────────────────────────
    print(f"\nRunning {args.sims:,} simulations...")
    sim_probs = run_tournament(n_sims=args.sims, market_probs=market_probs)

    # ── 3. Print summary ──────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("MODEL PROBABILITIES")
    print("=" * 60)
    print_summary(sim_probs)

    # ── 4. Save per-team probabilities ────────────────────────────────────────
    rows = []
    for team, probs in sim_probs.items():
        row = {"team": team, "group": get_group_for_team(team)}
        for k, v in probs.items():
            row[k] = round(v * 100, 2)
        rows.append(row)
    model_df = pd.DataFrame(rows).sort_values("Winner", ascending=False)
    model_df.to_csv(OUTPUT_CSV, index=False)
    print(f"\nSaved {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
