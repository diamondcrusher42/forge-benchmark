# forge-benchmark

**Parallel model × effort benchmarking for Claude Code.**

Runs all model/effort combinations simultaneously in isolated git worktrees — no manual resets, no manual JSONL hunting, no prompt pasting. Edit a prompt file, run one command, get a comparison table.

## How it works

1. Define a **suite** (prompt files + setup.sh + score.py)
2. Run `bash scripts/run_parallel.sh suites/my-suite`
3. All 6 model×effort combos launch simultaneously, each in its own git worktree
4. Results scored automatically, comparison table sent to Telegram

## Default matrix

| Run | Model | Effort |
|-----|-------|--------|
| 1 | Haiku 4.5 | medium |
| 2 | Haiku 4.5 | max |
| 3 | Sonnet 4.6 | medium |
| 4 | Sonnet 4.6 | max |
| 5 | Opus 4.6 | medium |
| 6 | Opus 4.6 | max |

Custom matrix: `--matrix "sonnet:medium,sonnet:max"`

## Suite structure

```
suites/my-suite/
├── prompts/
│   ├── task-A.md     # Task prompts (one per file, alphabetical order)
│   └── task-B.md
├── setup.sh          # Idempotent reset — receives WORKTREE env var
├── score.py          # Scorer: python3 score.py --session <jsonl> --task A → JSON
└── teardown.sh       # Optional cleanup
```

All prompts are concatenated into a single context and injected via `claude -p`.

## Quick start

```bash
# 1. Create a suite
bash scripts/suite_init.sh suites/my-suite

# 2. Edit prompts and setup.sh

# 3. Run
bash scripts/run_parallel.sh suites/my-suite

# 4. View results
ls ~/.claude/benchmark/my-suite/
python3 scripts/report.py ~/.claude/benchmark/my-suite/
```

## score.py interface

```python
# Called as: python3 score.py --session /path/to/session.jsonl --task A
# Must print JSON to stdout with any metrics you want in the table:
# {"task": "A", "tokens_total": 12000, "duration_min": 4.2, "correctness": 10, ...}
```

The bundled `suites/example/score.py` extracts: tokens, duration, turns, corrections, read:edit ratio, read-before-edit %.

## Results

Stored in `~/.claude/benchmark/{suite-name}/{run-id}.json`

Report format:
```
Run            | tokens output | duration min | produced output
Haiku   medium | 450           | 0.5          | True
Haiku   max    | 380           | 0.4          | True
Sonnet  medium | 520           | 0.7          | True
...
```

## Requirements

- Claude Code CLI (`claude`) in PATH
- Python 3.10+
- `~/workspace/venv` (or adjust `source` line in run_parallel.sh)
- Git (for worktree isolation when `BENCHMARK_BASE_REPO` is set)

## Environment variables

| Variable | Description |
|----------|-------------|
| `BENCHMARK_BASE_REPO` | Base git repo to create worktrees from |
| `BENCHMARK_BRANCH` | Branch/commit to check out in each worktree |
| `WORKTREE` | Injected by runner into setup.sh and score.py |

## Origin

Built as part of the Agent4wiki Forge segment — the perpetual improvement layer of the multi-agent architecture. See [agent4wiki](https://github.com/diamondcrusher42/agent4wiki) for the full system.
