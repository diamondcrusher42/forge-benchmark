#!/usr/bin/env python3
"""
Generate a comparison table from stored benchmark results.
Usage: python3 report.py ~/.claude/benchmark/my-suite/
Prints a Markdown table to stdout.
"""
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

MODEL_SHORT = {
    "claude-haiku-4-5-20251001": "Haiku",
    "claude-sonnet-4-6": "Sonnet",
    "claude-opus-4-6": "Opus",
}

def load_runs(suite_dir: Path) -> list[dict]:
    runs = []
    for f in sorted(suite_dir.glob("*.json")):
        if f.name == "report.json":
            continue
        try:
            data = json.loads(f.read_text())
            runs.append(data)
        except Exception:
            pass
    return runs

def collect_metric_keys(runs: list[dict]) -> list[str]:
    """Collect all metric keys from all tasks across all runs."""
    keys = []
    seen = set()
    for run in runs:
        for task_scores in run.get("scores", {}).values():
            for k in task_scores:
                if k != "task" and k not in seen:
                    keys.append(k)
                    seen.add(k)
    return keys

def avg_metric(run: dict, key: str) -> float | None:
    """Average a metric across all tasks in a run."""
    values = []
    for task_scores in run.get("scores", {}).values():
        v = task_scores.get(key)
        if v is not None:
            try:
                values.append(float(v))
            except (TypeError, ValueError):
                pass
    return round(sum(values) / len(values), 1) if values else None

def format_val(v) -> str:
    if v is None:
        return "—"
    if isinstance(v, float):
        return f"{v:.1f}"
    return str(v)

def generate_report(suite_dir: Path) -> str:
    runs = load_runs(suite_dir)
    if not runs:
        return "No benchmark runs found."

    # Sort: model order then effort
    model_order = ["claude-haiku-4-5-20251001", "claude-sonnet-4-6", "claude-opus-4-6"]
    effort_order = ["medium", "max"]

    def sort_key(run):
        m = model_order.index(run.get("model", "")) if run.get("model") in model_order else 99
        e = effort_order.index(run.get("effort", "")) if run.get("effort") in effort_order else 99
        return (m, e)

    runs.sort(key=sort_key)

    tasks = sorted(set(t for r in runs for t in r.get("scores", {}).keys()))
    metric_keys = collect_metric_keys(runs)

    # Header
    suite_name = suite_dir.name
    date_str = datetime.now().strftime("%Y-%m-%d")
    lines = [
        f"# BENCHMARK RESULTS — {suite_name}",
        f"Date: {date_str} | Tasks: {', '.join(tasks)}",
        "",
    ]

    # Build table
    col_headers = ["Run", "Effort"] + [k.replace("_", " ") for k in metric_keys]
    rows = []
    for run in runs:
        model_short = MODEL_SHORT.get(run.get("model", ""), run.get("model", "?"))
        effort = run.get("effort", "?")
        row = [model_short, effort]
        for k in metric_keys:
            v = avg_metric(run, k)
            row.append(format_val(v))
        rows.append(row)

    # Column widths
    widths = [max(len(h), max((len(r[i]) for r in rows), default=0)) for i, h in enumerate(col_headers)]

    def fmt_row(cells):
        return "| " + " | ".join(c.ljust(w) for c, w in zip(cells, widths)) + " |"

    lines.append(fmt_row(col_headers))
    lines.append("|" + "|".join("-" * (w + 2) for w in widths) + "|")
    for row in rows:
        lines.append(fmt_row(row))

    lines.append("")

    # Winners per metric
    lines.append("## Winners")
    for k in metric_keys:
        vals = [(avg_metric(r, k), r) for r in runs if avg_metric(r, k) is not None]
        if not vals:
            continue
        # Lower is better for: tokens, duration, corrections
        lower_is_better = any(x in k for x in ["token", "duration", "correction", "turn"])
        best_val, best_run = min(vals, key=lambda x: x[0]) if lower_is_better else max(vals, key=lambda x: x[0])
        model_short = MODEL_SHORT.get(best_run.get("model", ""), best_run.get("model", "?"))
        effort = best_run.get("effort", "?")
        direction = "lowest" if lower_is_better else "highest"
        lines.append(f"- **{k.replace('_', ' ')}**: {model_short} {effort} ({direction}: {format_val(best_val)})")

    return "\n".join(lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("suite_dir", help="Path to benchmark suite results dir")
    args = parser.parse_args()

    suite_dir = Path(args.suite_dir).expanduser()
    if not suite_dir.exists():
        print(f"Directory not found: {suite_dir}", file=sys.stderr)
        sys.exit(1)

    report = generate_report(suite_dir)
    print(report)

    # Also save
    report_path = suite_dir / "report.md"
    report_path.write_text(report)
    print(f"\n(Saved to {report_path})", file=sys.stderr)
