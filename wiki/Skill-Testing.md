# Skill Testing

The Forge tests models. It can also test **skills** — Claude Code skill prompt variants — using the same worktree isolation methodology.

## Difference: model benchmark vs skill test

| Dimension | Model benchmark | Skill test |
|---|---|---|
| Variable | Model, effort level | Skill prompt framing |
| Fixed | Task, success criteria | Model, effort level |
| Output | Correctness score | Quality score (subjective) |
| Promotion | Routing rules in config | SKILL.md rewritten |

## Methodology

```bash
# One worktree per skill variant
git worktree add ../skill-test-baseline
git worktree add ../skill-test-aggressive-cta
git worktree add ../skill-test-edu-focus

# Same prompt, same model, same effort — only SKILL.md changes
claude --model sonnet --effort medium -p "$(cat prompt.md)"
```

**Key rule:** Commit raw output before any edits. Grade what the AI produced.

## Evaluation scorecard (front-end design)

6 categories × 5 points = 30 max:

| Category | Criteria |
|---|---|
| Value Communication | Hero immediately clarifies value. Benefit-driven language. |
| Conversion & CTAs | CTAs strategically placed, visible, integrated. |
| Visual Hierarchy | Typography H1→H2→Body clear. Whitespace prevents overload. |
| Interaction & Polish | Elements give immediate feedback. Animations purposeful. |
| Component Architecture | Modular, DRY, well-structured. Hooks used appropriately. |
| Responsiveness | Graceful mobile breakpoints. Touch targets sized correctly. |

**Decision gate:** ≥ 24/30 → promote variant. Gap ≥ 4 → prompt framing matters significantly.

## Skill testing queue

| Skill | First test | Status |
|---|---|---|
| `frontend-design` | agent-janitor website (3 variants) | Queued |
| `webapp-testing` | Playwright coverage vs missed bugs | Planned |
| `code-review` | Finding overlap with Janitor + Opus | Planned |
| `janitor` (2-tier) | Model × effort quality matrix | Queued (Q1) |

## AI Execution Checklist (for front-end design)

Include in system prompt to force self-verification:

- [ ] Data Ingestion: Parse wiki data without losing technical accuracy
- [ ] Architecture: Separate UI components from business logic
- [ ] Page flow: Hero → How it Works → Interactive Tool → Social Proof → CTA
- [ ] State Management: Robust React state for interactive elements
- [ ] Design System: Tailwind utility classes, consistent typography + spacing
- [ ] Micro-interactions: Purposeful Framer Motion, not decorative
