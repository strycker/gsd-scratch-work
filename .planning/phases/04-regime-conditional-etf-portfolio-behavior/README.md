# Phase 4 — Regime-conditional ETF & portfolio behavior

The v1.0 product work for **regime-conditional ETF returns, template portfolios, and dashboard integration** is **shipped**. This directory is a **brownfield** GSD evidence anchor: the original delivery predates a historical `*-PLAN.md` in this folder.

**Evidence**

- [Verification (audit)](./04-regime-conditional-etf-portfolio-behavior-VERIFICATION.md) — PORT-01..03, artifact map.
- [Validation](./04-VALIDATION.md) — Nyquist / checklist for this phase.

**Primary entrypoints**

- `run_pipeline.py` — `step6_asset_returns`, `step7_dashboard`.
- `pipelines/06_asset_returns.py` — stand-alone step 6.
- `pipelines/07_dashboard.py` — stand-alone step 7.

Operational sequences and flags: repo-root **`RUNBOOK.md`**.
