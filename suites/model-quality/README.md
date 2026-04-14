# Model Quality Benchmark Suite

Tests coding ability across 3 models to detect quality regressions.
Mirrors the [aistupidlevel.info](https://aistupidlevel.info/methodology) 5-axis methodology.

## Why this exists

Empirical reports suggest Opus 4.6 is degraded vs Opus 4.5 (post-Feb 2026 adaptive thinking changes).
This suite produces objective, reproducible evidence — not "trust me bro."

## Axes and weights

| Axis        | Weight | What it measures                              |
|-------------|--------|-----------------------------------------------|
| Correctness | 40%    | Output passes test cases                      |
| Complexity  | 20%    | Handles non-trivial inputs, correct algorithm |
| Quality     | 15%    | Typed, documented, clean variable names       |
| Stability   | 10%    | Handles nulls, empty, boundary inputs         |
| Efficiency  | 5%     | Avoids O(n²) where O(n) is required           |

## Challenges (13 total)

| ID | Challenge | Axis |
|----|-----------|------|
| 01 | Balanced Brackets | Correctness |
| 02 | Merge Sorted Lists | Correctness |
| 03 | Flatten Nested Dict | Correctness |
| 04 | Word Frequency Top-N | Correctness |
| 05 | Coin Change (DP) | Complexity |
| 06 | BFS Shortest Path | Complexity |
| 07 | Sliding Window Max Sum | Complexity |
| 08 | LRU Cache | Quality |
| 09 | Refactor Messy Code | Quality |
| 10 | Robust Average (null safety) | Stability |
| 11 | Binary Search (bounds) | Stability |
| 12 | Dedup Preserving Order | Efficiency |
| 13 | Two Sum (hash map) | Efficiency |

## Models to test

| Short name | Full model ID | Notes |
|------------|---------------|-------|
| `sonnet`   | claude-sonnet-4-6 | Expected baseline |
| `opus`     | claude-opus-4-6 | Allegedly degraded |
| `opus-4-5` | claude-opus-4-5-20251101 | Pinned snapshot, truth baseline |

## Run order (one model at a time)

```bash
# Round 1 — Sonnet baseline
cd /home/claudebot/forge-benchmark
source ~/workspace/venv/bin/activate
python3 suites/model-quality/run.py --model sonnet

# Round 2 — Current Opus (after reviewing Round 1)
python3 suites/model-quality/run.py --model opus

# Round 3 — Pinned Opus 4.5 snapshot
python3 suites/model-quality/run.py --model opus-4-5

# Compare all three
python3 suites/model-quality/compare.py \
  suites/model-quality/results/sonnet/*/summary.json \
  suites/model-quality/results/opus/*/summary.json \
  suites/model-quality/results/opus-4-5/*/summary.json
```

## Dry run (no API calls)

```bash
python3 suites/model-quality/run.py --model sonnet --dry-run
```

## Results structure

```
results/
  sonnet/
    20260414-1200/
      01_string_balanced.txt    # raw model output
      01_string_balanced.json   # graded scores
      ...
      summary.json              # full run summary
```

## Grading

The grader (`grader.py`):
1. Extracts the code block from model output
2. Executes the code against test cases in a subprocess (real execution, not LLM eval)
3. Scores quality via static AST analysis (type hints, docstrings, naming)
4. Checks efficiency via regex pattern matching (no nested loops where O(n) required)
5. Applies axis weights to produce a final score 0–100
