#!/usr/bin/env python3
"""
Compare results across model runs.

Usage:
    python3 compare.py results/sonnet/20260414-1200/summary.json \
                       results/opus/20260414-1215/summary.json \
                       results/opus-4-5/20260414-1230/summary.json
"""
import json
import sys
from pathlib import Path


def load_summary(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def main():
    if len(sys.argv) < 2:
        print("Usage: compare.py <summary1.json> [summary2.json ...]")
        sys.exit(1)

    summaries = [load_summary(p) for p in sys.argv[1:]]
    axes = ["correctness", "complexity", "quality", "stability", "efficiency"]
    weights = [0.40, 0.20, 0.15, 0.10, 0.05]

    print(f"\n{'='*70}")
    print("  MODEL QUALITY COMPARISON")
    print(f"{'='*70}")

    # Header
    col = 14
    header = f"  {'Axis':<14}" + "".join(f"{s['model']:>{col}}" for s in summaries)
    print(header)
    print("  " + "-" * (len(header) - 2))

    for axis, weight in zip(axes, weights):
        row = f"  {axis:<12} {weight:.0%}"
        for s in summaries:
            val = s.get("axis_averages", {}).get(axis, 0.0)
            row += f"{val:>{col}.3f}"
        print(row)

    print("  " + "-" * (len(header) - 2))
    row = f"  {'SCORE /100':<14}"
    for s in summaries:
        row += f"{s.get('scaled_score', 0):>{col}.1f}"
    print(row)
    print(f"{'='*70}")

    # Winner
    best = max(summaries, key=lambda s: s.get("scaled_score", 0))
    print(f"\n  Winner: {best['model']} ({best['model_id']}) — {best['scaled_score']:.1f}/100")

    # Per-challenge breakdown
    print(f"\n  Per-challenge breakdown:")
    all_ids = [r["challenge"] for r in summaries[0].get("per_challenge", [])]
    hdr2 = f"  {'Challenge':<26}" + "".join(f"{s['model']:>10}" for s in summaries)
    print(hdr2)
    print("  " + "-" * (len(hdr2) - 2))

    for cid in all_ids:
        row = f"  {cid:<26}"
        for s in summaries:
            pc = {r["challenge"]: r for r in s.get("per_challenge", [])}
            val = pc.get(cid, {}).get("weighted_total", 0.0)
            row += f"{val:>10.3f}"
        print(row)

    print()


if __name__ == "__main__":
    main()
