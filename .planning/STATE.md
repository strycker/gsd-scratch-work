---
gsd_state_version: 1.2
milestone: v1.2
milestone_name: TBD
status: defining_requirements
last_updated: "2026-03-17"
progress:
  total_phases: 0
  completed_phases: 0
  total_plans: 0
  completed_plans: 0
---

## Project State — Trading-Crab (v1.2)

## Project Reference

- **Project**: Trading-Crab — Market Regime Analysis & ETF Portfolio Guidance
- **Core value**: Turn macro-driven market regimes and ETF behavior into transparent, regime-aware portfolio recommendations and a weekly advisory-style report.
- **Scope (v1)**: ETF-only universe, weekly/quarterly cadence, recommendation-focused (no auto-trading, no single stocks or direct crypto).

## Current Position

- **Current milestone**: v1.2 (name and goal TBD)
- **Current phase**: Not started — define milestone focus, then requirements & roadmap.
- **Overall status**: New milestone started; ready for goal + requirements.

### Phase Progress

| Phase | Name                               | Status      | Notes                    |
|-------|------------------------------------|-------------|--------------------------|
| 1–3   | Foundations, Clustering, Models    | Completed   | Shipped in v1.0          |
| 4–6   | ETF Behavior, Recommendations, Weekly | Completed | Shipped in v1.1          |
| 7+    | v1.2 phases                        | Not started | To be defined            |

## Performance & Health

- **Pipeline health**: Unknown (v1 implementation not yet executed end-to-end).
- **Data freshness**: Unknown (to be tracked once ingestion/checkpoints are live).
- **Model performance**: Not yet measured (pending Phases 2–3).

## Accumulated Context

### Key Decisions (from PROJECT.md)

- Focus on ETF-level portfolios only; no single stocks or direct crypto in v1.
- Allow bitcoin exposure only via ETF wrappers.
- Weekly report cadence; regime focus is quarterly.

### Open Questions / Risks

- How stable are regime labels over time as new data arrives?
- How robust are supervised models and portfolio templates to regime changes outside historical experience?

### Working Notes

- Use `ROADMAP.md` as the source of truth for phase goals, dependencies, and success criteria.
- Use `REQUIREMENTS.md` to keep requirement IDs and traceability aligned as implementation proceeds.

