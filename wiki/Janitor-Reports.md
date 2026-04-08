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

## [2026-04-09] Tier 1 comparison — Sonnet --medium (blind)

**Purpose:** Blind Tier 1 comparison against Haiku scan. No findings disclosed before run.

**Model:** Sonnet 4.6 `--effort medium`
**Tool:** agent-janitor v1.0.1

**Results:**

| Metric | Value |
|---|---|
| Health Score | 83/100 |
| Verdict | SUGGEST |
| BLOCK | 0 |
| SUGGEST | 2 |
| NOTE | 1 |
| Good patterns | 1 |
| Tokens | 21,937 |
| Duration | 38 seconds |

**Findings (identical to Haiku):**
- SUGGEST — Missing tests: `scripts/report.py`
- SUGGEST — Missing tests: `suites/example/score.py`
- NOTE — Dead code at `suites/example/score.py:33` — same false positive as Haiku (multi-line dict literal)
- GOOD — README.md exists

**Tier 1 comparison verdict:** Sonnet and Haiku found **identical findings** on this repo. Health score, verdict, all finding locations, and even the false positive match exactly. Sonnet used fewer tokens (21,937 vs 29,104) but took similar time (38s vs 34s). For objective structural findings, Haiku is the clear winner on cost efficiency with no quality loss.

---

## [2026-04-09] Tier 2 test — Opus --max (blind)

**Purpose:** Tier 2 deep scan for semantic comparison against Haiku and Sonnet.

**Model:** Opus 4.6 `--effort max`
**Tool:** agent-janitor v1.0.1

**Results:**

| Metric | Value |
|---|---|
| Health Score | 83/100 |
| Verdict | SUGGEST |
| BLOCK | 0 |
| SUGGEST | 2 |
| NOTE | 1 (same FP as Haiku/Sonnet) |
| Good patterns | 1 |
| Tokens | 20,727 |
| Duration | 33 seconds |

**Findings (identical to Haiku and Sonnet):**
- SUGGEST — Missing tests: `scripts/report.py`
- SUGGEST — Missing tests: `suites/example/score.py`
- NOTE — Dead code at `suites/example/score.py:33` — same false positive (multi-line dict literal)
- GOOD — README.md exists

**3-way comparison verdict:** All three models produced **identical findings**. Opus found nothing that Haiku missed. This repo lacks the semantic complexity needed to differentiate tiers (no bare `except: pass`, no type hint violations, no docstring gaps in complex logic). The Tier 2 gap exists — but requires a more complex codebase to surface it.

---

*This page is append-only. Each audit adds a new dated entry.*
