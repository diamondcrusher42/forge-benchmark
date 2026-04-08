# forge-benchmark Wiki

**Parallel model × effort benchmarking for Claude Code.**

This wiki documents how to use the benchmark runner, how to design suites, how to interpret results, and what decisions have been made based on benchmark data.

## Pages

* [[How-It-Works]] — Architecture, worktree isolation, scoring pipeline
* [[Writing-Suites]] — How to design a benchmark suite, prompt format, scorer contract
* [[Results-History]] — All benchmark runs: what was tested, scores, routing decisions made
* [[Skill-Testing]] — Using the Forge to compare Claude Code skill variants (not just models)
* [[Janitor-Reports]] — Janitor audit log for the forge-benchmark repo itself

## Quick start

```bash
# Run all 6 model×effort combos on a suite
bash scripts/run_parallel.sh suites/my-suite

# Custom matrix
bash scripts/run_parallel.sh suites/my-suite --matrix "sonnet:medium,opus:max"

# View results
python3 scripts/report.py suites/my-suite/results/
```

## Current benchmark matrix

| Run | Model | Effort |
|---|---|---|
| 1 | Haiku 4.5 | medium |
| 2 | Haiku 4.5 | max |
| 3 | Sonnet 4.6 | medium |
| 4 | Sonnet 4.6 | max |
| 5 | Opus 4.6 | medium |
| 6 | Opus 4.6 | max |

## Key decisions made from benchmark data

| Decision | Source benchmark | Result |
|---|---|---|
| Effort routing: max for security, medium for general | Phase 1 effort | Promoted to clone_config.json |
| Opus medium wins on Forge eval tasks | Phase 2 context | Forge default = Opus medium |
| 2-tier Janitor (planned) | Planned Q1 | Pending run |
