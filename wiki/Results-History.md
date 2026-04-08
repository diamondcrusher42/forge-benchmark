# Results History

All benchmark runs, scores, and routing decisions. Append-only.

---

## [2026-04-08] Phase 1 — Effort Level Routing

**Suite:** agent4wiki tasks (3 prompts: security fix, precision wiring, general implementation)
**Matrix:** Sonnet 4.6 × {medium, high, max}

**Results:**

| Task | medium | high | max | Winner |
|---|---|---|---|---|
| Security fix (shell injection) | partial | correct | correct | max |
| Precision wiring (confidence gate) | partial | correct | correct | max |
| General implementation (OOM guard) | correct | correct | correct | medium (speed) |

**Decision made:**
- Security / precision wiring → `--effort max`
- General implementation → `--effort medium`
- Never use `--effort high` — no measurable improvement, ~60% cost premium
- Promoted to: `decision-effort-level-routing.md`, `clone_config.json`

---

## [2026-04-08] Phase 2 — Context Window + Full Matrix

**Suite:** Same 3 agent4wiki tasks + full repo context via Repomix
**Matrix:** All 6 combos (Haiku, Sonnet, Opus × {medium, max})

**Results:**

| Model | Effort | Score | Tokens | Time |
|---|---|---|---|---|
| Opus 4.6 | medium | 10/10 | 6,142 | 1.6 min |
| Sonnet 4.6 | max | 10/10 | ~8,900 | ~2.1 min |
| Sonnet 4.6 | medium | 10/10 | ~7,500 | ~1.9 min |
| Haiku 4.5 | max | 10/10 | ~14,200 | ~2.8 min |
| Opus 4.6 | max | 10/10 | ~9,800 | ~3.0 min |
| Haiku 4.5 | medium | 10/10 | 19,612 | 3.2 min |

**Decision made:**
- All 6 combos correct on these tasks — correctness alone doesn't differentiate
- Opus medium wins on token efficiency + speed
- Haiku medium worst (uses 3× tokens of Opus medium — compensates with retrieval)
- Forge evaluation default: **Opus medium**
- Forge scheduling: run at token reset for $0 marginal cost

---

## [2026-04-09] Janitor Tier 1 Test — forge-benchmark self-scan

**Model:** Haiku 4.5 `--max`
**Target:** `diamondcrusher42/forge-benchmark` (this repo)
**Purpose:** First real Tier 1 Janitor test. Validate Haiku can run audit without Opus-level reasoning.

**Results:** → See [[Janitor-Reports]]

---

## Planned: Janitor 2-Tier Benchmark

**Suite:** 5 test cases targeting semantic finding quality (dead code confusion traps, design contradictions, silent failures, stale artifacts, good pattern preservation)
**Matrix:** Haiku max, Sonnet medium, Opus max+extended

**Decision gate:** Tier 1 ≥ 4/5 → single tier. Gap ≥ 2 → 2-tier routing justified.

**Status:** Queued. See [[Skill-Testing]] for the full framework.
