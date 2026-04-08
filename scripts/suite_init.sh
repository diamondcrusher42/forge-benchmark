#!/bin/bash
# Create a template benchmark suite at the specified path
# Usage: bash suite_init.sh /path/to/new-suite

SUITE_DIR="${1:?Usage: suite_init.sh <suite-path>}"

mkdir -p "$SUITE_DIR/prompts"

cat > "$SUITE_DIR/setup.sh" << 'EOF'
#!/bin/bash
# Reset to clean state before each benchmark run.
# This runs automatically before every model/effort combination.
# Make it idempotent — safe to run multiple times.

set -euo pipefail

WORKTREE="${BENCHMARK_WORKTREE:-}"
if [[ -z "$WORKTREE" ]]; then
    echo "ERROR: set BENCHMARK_WORKTREE env var to your worktree path" >&2
    exit 1
fi

echo "Resetting worktree at $WORKTREE..."
# Example: git checkout <commit> -- src/file.ts
# Example: rm -f test/generated-file.ts

echo "Setup complete. Worktree is ready."
EOF
chmod +x "$SUITE_DIR/setup.sh"

cat > "$SUITE_DIR/teardown.sh" << 'EOF'
#!/bin/bash
# Optional cleanup after each run.
# Called automatically after JSONL is captured and scored.
echo "Teardown complete."
EOF
chmod +x "$SUITE_DIR/teardown.sh"

cat > "$SUITE_DIR/score.py" << 'EOF'
#!/usr/bin/env python3
"""
Score a benchmark run. Print JSON to stdout.
Called per-task: python3 score.py --session /path/to/session.jsonl --task A
"""
import argparse
import json
from pathlib import Path

def parse_events(session_path):
    events = []
    with open(session_path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return events

def score(session_path, task):
    events = parse_events(session_path)

    # ── Token count ──────────────────────────────────────────────────────────
    output_tokens = sum(
        e.get("message", {}).get("usage", {}).get("output_tokens", 0)
        for e in events if e.get("type") == "assistant"
    )
    input_tokens = sum(
        e.get("message", {}).get("usage", {}).get("input_tokens", 0)
        for e in events if e.get("type") == "assistant"
    )

    # ── Duration ─────────────────────────────────────────────────────────────
    timestamps = [
        e.get("timestamp") for e in events
        if e.get("timestamp") and e.get("type") in ("user", "assistant")
    ]
    duration_min = None
    if len(timestamps) >= 2:
        from datetime import datetime
        try:
            t0 = datetime.fromisoformat(timestamps[0].replace("Z", "+00:00"))
            t1 = datetime.fromisoformat(timestamps[-1].replace("Z", "+00:00"))
            duration_min = round((t1 - t0).total_seconds() / 60, 1)
        except Exception:
            pass

    # ── Human corrections ────────────────────────────────────────────────────
    human_turns = sum(1 for e in events if e.get("type") == "user")
    assistant_turns = sum(1 for e in events if e.get("type") == "assistant")

    # ── Read-before-edit ratio ───────────────────────────────────────────────
    tool_uses = [
        e.get("message", {}).get("content", [])
        for e in events if e.get("type") == "assistant"
    ]
    reads = 0
    edits = 0
    last_was_read = False
    edits_after_read = 0
    for content in tool_uses:
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            name = block.get("name", "")
            if name in ("Read", "read_file"):
                reads += 1
                last_was_read = True
            elif name in ("Edit", "Write", "edit_file", "write_file"):
                edits += 1
                if last_was_read:
                    edits_after_read += 1
                last_was_read = False

    read_before_edit = round(edits_after_read / edits, 2) if edits > 0 else None
    read_edit_ratio = round(reads / edits, 1) if edits > 0 else None

    # ── Task-specific checks ─────────────────────────────────────────────────
    # Add your own checks below. Return a dict with any keys you want in the table.
    # Example:
    #   correctness = check_task_a() if task == "A" else check_task_b()

    return {
        "task": task,
        "tokens_output": output_tokens,
        "tokens_input": input_tokens,
        "tokens_total": output_tokens + input_tokens,
        "duration_min": duration_min,
        "assistant_turns": assistant_turns,
        "human_corrections": human_turns,
        "reads": reads,
        "edits": edits,
        "read_edit_ratio": read_edit_ratio,
        "read_before_edit_pct": int(read_before_edit * 100) if read_before_edit is not None else None,
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", required=True, help="Path to session JSONL")
    parser.add_argument("--task", required=True, help="Task ID (A, B, C, ...)")
    args = parser.parse_args()
    result = score(args.session, args.task)
    print(json.dumps(result, indent=2))
EOF
chmod +x "$SUITE_DIR/score.py"

cat > "$SUITE_DIR/prompts/task-A.md" << 'EOF'
Your first task prompt here.
Replace this with the actual instructions you want to test.
EOF

cat > "$SUITE_DIR/prompts/task-B.md" << 'EOF'
Your second task prompt here.
Replace this with the actual instructions you want to test.
EOF

echo "Suite created at: $SUITE_DIR"
echo ""
echo "Next steps:"
echo "  1. Edit $SUITE_DIR/setup.sh — add your worktree reset logic"
echo "  2. Edit $SUITE_DIR/prompts/task-A.md — add your first task prompt"
echo "  3. Edit $SUITE_DIR/score.py — add task-specific correctness checks"
echo "  4. Set BENCHMARK_WORKTREE=/path/to/your/worktree"
echo "  5. Run: /benchmark run $SUITE_DIR"
