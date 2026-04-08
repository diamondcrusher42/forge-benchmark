# Janitor Reports

Audit log for the forge-benchmark repo itself. The Forge audits everything — including itself.

---

## [2026-04-09] Tier 1 test — Haiku --max

**Purpose:** First real Tier 1 Janitor test. Validate that Haiku (cheapest, fastest) can run a useful audit without Opus-level reasoning.

**Model:** Haiku 4.5 `--effort max`
**Tool:** agent-janitor v1.0.1 (with false positive fixes from real-world test run)

**Results:**

| Metric | Value |
|---|---|
| Health Score | 83/100 |
| Verdict | SUGGEST |
| BLOCK | 0 |
| SUGGEST | 2 |
| NOTE | 1 (false positive) |
| Good patterns | 1 |
| Tokens | 29,104 |
| Duration | 34 seconds |
| Cost | ~$0.01 |

**Findings:**
- SUGGEST — Missing tests: `scripts/report.py` (complex aggregation logic, edge cases unprotected)
- SUGGEST — Missing tests: `suites/example/score.py` (metrics calculation, JSON parsing)
- NOTE — Dead code at `suites/example/score.py:33` — **FALSE POSITIVE** (multi-line dict literal return misread as unreachable)
- GOOD — README.md exists

**Tier 1 verdict:** Haiku caught all objective findings correctly in 34s for ~$0.01. Missed (expected for Tier 1): bare `except: pass` error handling, missing type hints/docstrings — these are Tier 2 (Opus) territory.

**What to fix:**
1. Add `tests/test_score.py` and `tests/test_report.py`
2. Test edge cases: empty runs, missing metrics, None values in sorting

---

*This page is append-only. Each audit adds a new dated entry.*
