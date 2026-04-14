#!/usr/bin/env python3
"""
Model Quality Benchmark Runner.

Runs one model at a time against all 13 coding challenges.
Each challenge runs in its own fresh claude -p session.

Usage:
    python3 run.py --model sonnet         # claude-sonnet-4-6
    python3 run.py --model opus           # claude-opus-4-6
    python3 run.py --model opus-4-5       # claude-opus-4-5-20251101
    python3 run.py --model sonnet --dry-run  # preview prompts only

Results saved to: results/<model>/<timestamp>/
"""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# ── Model ID map ──────────────────────────────────────────────────────────────
MODEL_IDS = {
    "sonnet":   "claude-sonnet-4-6",
    "opus":     "claude-opus-4-6",
    "opus-4-5": "claude-opus-4-5-20251101",
    "haiku":    "claude-haiku-4-5-20251001",
}

SUITE_DIR = Path(__file__).parent
CHALLENGES_DIR = SUITE_DIR / "challenges"
RESULTS_DIR = SUITE_DIR / "results"


def get_challenge_ids() -> list[str]:
    """Return sorted list of challenge IDs from challenges/ directory."""
    return sorted(
        p.stem for p in CHALLENGES_DIR.glob("*.md")
        if p.name[0].isdigit()
    )


def run_challenge(challenge_id: str, model_id: str, effort: str, dry_run: bool) -> dict:
    """
    Run one challenge against one model in a fresh claude -p session.
    Returns dict with raw output and timing.
    """
    prompt_file = CHALLENGES_DIR / f"{challenge_id}.md"
    prompt = prompt_file.read_text()

    print(f"  [{challenge_id}] Sending to {model_id}...", flush=True)

    if dry_run:
        print(f"  [{challenge_id}] DRY RUN — skipping")
        return {"challenge": challenge_id, "output": "", "duration_s": 0, "dry_run": True}

    start = time.monotonic()
    try:
        result = subprocess.run(
            ["claude", "-p", prompt,
             "--model", model_id,
             "--effort", effort,
             "--permission-mode", "bypassPermissions"],
            capture_output=True,
            text=True,
            timeout=120,  # 2 min per challenge
            env={**os.environ, "MAX_THINKING_TOKENS": "16000"},
        )
        output = result.stdout.strip()
        stderr = result.stderr.strip()
        success = result.returncode == 0
    except subprocess.TimeoutExpired:
        output = ""
        stderr = "TIMEOUT"
        success = False

    duration = round(time.monotonic() - start, 1)
    print(f"  [{challenge_id}] Done in {duration}s — {'OK' if success else 'FAIL'}", flush=True)

    return {
        "challenge": challenge_id,
        "output": output,
        "stderr": stderr,
        "duration_s": duration,
        "success": success,
    }


def main():
    parser = argparse.ArgumentParser(description="Run model quality benchmark")
    parser.add_argument(
        "--model", required=True,
        choices=list(MODEL_IDS.keys()),
        help="Model to test"
    )
    parser.add_argument(
        "--effort", default="max",
        choices=["low", "medium", "high", "max"],
        help="Effort level (default: max)"
    )
    parser.add_argument(
        "--challenges", nargs="*",
        help="Specific challenge IDs to run (default: all)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview challenges without calling Claude"
    )
    args = parser.parse_args()

    model_id = MODEL_IDS[args.model]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
    run_dir = RESULTS_DIR / args.model / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)

    challenge_ids = args.challenges or get_challenge_ids()

    print(f"\n{'='*60}")
    print(f"  Model Quality Benchmark")
    print(f"  Model:  {model_id}")
    print(f"  Effort: {args.effort}")
    print(f"  Challenges: {len(challenge_ids)}")
    print(f"  Results: {run_dir}")
    print(f"{'='*60}\n")

    # Import grader
    sys.path.insert(0, str(SUITE_DIR))
    from grader import grade_challenge

    all_results = []

    for challenge_id in challenge_ids:
        # Run challenge
        run_result = run_challenge(challenge_id, model_id, args.effort, args.dry_run)

        # Save raw output
        output_file = run_dir / f"{challenge_id}.txt"
        output_file.write_text(run_result.get("output", ""))

        # Grade
        if not args.dry_run and run_result.get("success"):
            grade = grade_challenge(challenge_id, run_result["output"])
        else:
            grade = {"challenge": challenge_id, "weighted_total": 0.0, "error": "no output"}

        grade["duration_s"] = run_result.get("duration_s", 0)

        # Save grade
        grade_file = run_dir / f"{challenge_id}.json"
        grade_file.write_text(json.dumps(grade, indent=2))

        all_results.append(grade)

        if not args.dry_run:
            time.sleep(2)  # Rate limit between calls

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  RESULTS — {args.model} ({args.effort})")
    print(f"{'='*60}")

    total_weighted = 0.0
    axis_totals = {"correctness": [], "complexity": [], "quality": [], "stability": [], "efficiency": []}

    header = f"  {'Challenge':<26} {'Corr':>5} {'Comp':>5} {'Qual':>5} {'Stab':>5} {'Effi':>5} {'Total':>6}"
    print(header)
    print("  " + "-" * (len(header) - 2))

    for r in all_results:
        cid = r.get("challenge", "?")
        if "error" in r and "weighted_total" not in r:
            print(f"  {cid:<26} ERROR")
            continue

        corr = r.get("correctness", 0.0)
        comp = r.get("complexity", 0.0)
        qual = r.get("quality", 0.0)
        stab = r.get("stability", 0.0)
        effi = r.get("efficiency", 0.0)
        total = r.get("weighted_total", 0.0)

        print(f"  {cid:<26} {corr:>5.2f} {comp:>5.2f} {qual:>5.2f} {stab:>5.2f} {effi:>5.2f} {total:>6.3f}")

        total_weighted += total
        for axis in axis_totals:
            if axis in r:
                axis_totals[axis].append(r[axis])

    print("  " + "-" * (len(header) - 2))

    n = len(all_results)
    avg = total_weighted / n if n > 0 else 0.0

    print(f"\n  Axis averages:")
    for axis, vals in axis_totals.items():
        avg_axis = sum(vals) / len(vals) if vals else 0.0
        weight = {"correctness": 0.40, "complexity": 0.20, "quality": 0.15,
                  "stability": 0.10, "efficiency": 0.05}[axis]
        print(f"    {axis:<12} {avg_axis:.3f}  (weight {weight:.0%})")

    print(f"\n  WEIGHTED AVERAGE: {avg:.3f} / 1.000")
    print(f"  SCALED SCORE:     {avg*100:.1f} / 100")
    print(f"{'='*60}\n")

    # Save summary
    summary = {
        "model": args.model,
        "model_id": model_id,
        "effort": args.effort,
        "timestamp": timestamp,
        "challenges_run": n,
        "weighted_average": round(avg, 4),
        "scaled_score": round(avg * 100, 2),
        "axis_averages": {
            axis: round(sum(vals)/len(vals), 4) if vals else 0.0
            for axis, vals in axis_totals.items()
        },
        "per_challenge": all_results,
    }

    summary_file = run_dir / "summary.json"
    summary_file.write_text(json.dumps(summary, indent=2))
    print(f"  Summary saved: {summary_file}")

    return summary


if __name__ == "__main__":
    main()
