# Writing Suites

A suite is the unit of a benchmark. One suite = one task type. Multiple suites = multiple capability areas being tracked.

## Suite structure

```
suites/my-suite/
├── prompts/
│   ├── 01-context.md    # Background + repo state
│   ├── 02-task.md       # The concrete task
│   └── 03-criteria.md   # What success looks like (optional but helpful)
├── setup.sh             # Resets worktree state (receives WORKTREE env var)
├── score.py             # Grades output: python3 score.py --session <jsonl> --task A
└── teardown.sh          # Optional cleanup
```

## Prompt design principles

**Be specific about the success state.** Don't say "fix the bug" — say "the function should return BLOCK when tests_passed is False, regardless of status field."

**Include the context the model needs.** Paste the relevant source file or function, not the whole repo. The runner can inject Repomix for you if needed.

**One task per prompt file.** Multi-task prompts make scoring ambiguous.

## Scorer contract

`score.py` outputs JSON to stdout:

```json
{
  "score": 8,
  "max_score": 10,
  "correctness": true,
  "precision": 0.9,
  "notes": "Found the bug but missed the edge case in None handling",
  "tokens_consumed": 4200,
  "duration_seconds": 45
}
```

- `score` / `max_score`: your rubric, whatever makes sense for the task
- `correctness`: boolean — did it solve the core problem?
- `precision`: 0-1 — did it do exactly what was asked, no more, no less?
- `notes`: free text for the comparison table

## setup.sh requirements

- Must be idempotent (safe to run multiple times)
- Must use `$WORKTREE` env var for paths
- Must exit 0 on success

```bash
#!/bin/bash
set -e
# Example: copy input files to worktree
cp fixtures/input.py "$WORKTREE/src/target.py"
```

## Good suite ideas

| Suite type | What to measure |
|---|---|
| Security fix | Does it find and fix the actual vulnerability, not just the symptom? |
| Precision wiring | Does it wire the exact interface asked, no more? |
| Dead code detection | Does it identify the correct block as dead? |
| Janitor audit | Does it catch the semantic issues, not just syntax? |
| Brief quality | Does the plan it produces lead to green tests when executed? |

## Naming convention

```
suites/{domain}-{version}/
# Examples:
suites/security-v1/
suites/janitor-tier-comparison-v1/
suites/frontend-skill-v1/
```

Version the suite when you change the prompts or scorer — old results stay comparable to old runs.
