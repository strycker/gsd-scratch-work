---
gsd_state_version: 1.1
milestone: v1.1
milestone_name: ETF Behavior & Portfolios
status: defining_requirements
last_updated: "2026-03-16T21:59:00.000Z"
progress:
  total_phases: 6
  completed_phases: 0
  total_plans: 0
  completed_plans: 0
---

## Project State — Trading-Crab (v1.1)

## Project Reference

- **Project**: Trading-Crab — Market Regime Analysis & ETF Portfolio Guidance
- **Core value**: Turn macro-driven market regimes and ETF behavior into transparent, regime-aware portfolio recommendations and a weekly advisory-style report.
- **Scope (v1)**: ETF-only universe, weekly/quarterly cadence, recommendation-focused (no auto-trading, no single stocks or direct crypto).

## Current Position

- **Current milestone**: v1.1 ETF Behavior & Portfolios
- **Current phase**: Not yet started (requirements and roadmap for v1.1 to be (re)defined)
- **Overall status**: New milestone initialized; ready for refreshed REQUIREMENTS and ROADMAP.

### Phase Progress

| Phase | Name                               | Plans Complete | Status      | Notes                                      |
|-------|------------------------------------|----------------|-------------|--------------------------------------------|
| 1     | Data & Constraints Foundations     | 0/0            | Completed   | Shipped as part of v1.0 Trading-Crab       |
| 2     | Regime Clustering & Interpretation | 0/0            | Completed   | Shipped as part of v1.0 Trading-Crab       |
| 3     | Supervised Regime & Behavior Models | 0/0           | Completed   | Shipped as part of v1.0 Trading-Crab       |
| 4     | Regime-Conditional ETF Behavior    | 0/0            | Not started | Primary focus area for milestone v1.1      |
| 5     | Recommendations & Outputs          | 0/0            | Not started | Builds on enhanced behavior & regime views |
| 6     | Weekly Report Pipeline             | 0/0            | Not started | Downstream consumer of v1.1 enhancements   |

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

