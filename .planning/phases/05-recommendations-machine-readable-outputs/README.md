# Phase 5 — Recommendations & machine-readable outputs

The v1.0 work for **portfolio-aware recommendations, weekly markdown, and machine-readable bundles** is **shipped**. This directory is a **brownfield** GSD anchor (no historical `*-PLAN.md` for the original delivery).

**Evidence**

- [Verification](./05-recommendations-machine-readable-outputs-VERIFICATION.md) — UX-01..03.
- [Validation](./05-VALIDATION.md).

**Primary entrypoints**

- `run_pipeline.py` — `step7_dashboard`.
- `pipelines/07_dashboard.py` — stand-alone dashboard / recommendations.
- `src/trading_crab_lib/reporting.py` — `write_weekly_report_md`, CSV/parquet writers.
- Artifacts under `outputs/reports/` (e.g. `dashboard.csv`, `trade_recommendations.csv`, `weekly_report.md`, `recommendation_bundle.parquet` when inputs exist).

See repo-root **`RUNBOOK.md`** for operational context.
