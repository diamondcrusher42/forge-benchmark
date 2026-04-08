# How It Works

## Overview

forge-benchmark runs all model × effort combinations simultaneously in isolated git worktrees. No manual resets, no prompt pasting, no JSONL hunting.

```
suites/my-suite/
├── prompts/task-A.md     → injected via claude -p
├── setup.sh              → resets worktree state before each run
├── score.py              → grades each run, outputs JSON
└── teardown.sh           → optional cleanup
```

## Execution flow

```
run_parallel.sh
  ↓
for each (model, effort) combo:
  git worktree add /tmp/run-{model}-{effort}
  bash setup.sh WORKTREE=/tmp/run-{model}-{effort}
  claude --model {model} --effort {effort} -p "$(cat prompts/*.md)"
    → session.jsonl written to worktree
  python3 score.py --session session.jsonl --task A → score.json
  ↓
report.py aggregates all score.json → comparison table → Telegram
```

## Worktree isolation

Each run gets a fresh git worktree from the same commit. `setup.sh` resets any state the worktree needs (e.g., creating input files, clearing output dirs). This ensures runs don't interfere.

## Scoring contract

`score.py` must accept `--session <jsonl-path> --task <label>` and write JSON to stdout:

```json
{
  "score": 8,
  "max_score": 10,
  "correctness": true,
  "notes": "Found the bug but missed the edge case",
  "tokens_consumed": 4200,
  "duration_seconds": 45
}
```

The runner captures this and feeds it to `report.py`.

## Output: comparison table

```
════════════════════════════════════════════
  forge-benchmark results — agent4wiki suite
════════════════════════════════════════════

  Model          Effort   Score    Tokens   Time
  ─────────────────────────────────────────────
  Opus 4.6       medium   10/10    6,142    1.6m  ← winner
  Sonnet 4.6     max       10/10    8,891    2.1m
  Haiku 4.5      max        8/10   14,203    2.8m
  Haiku 4.5      medium     7/10   19,612    3.2m

  Recommendation: Opus medium for this task type.
════════════════════════════════════════════
```
