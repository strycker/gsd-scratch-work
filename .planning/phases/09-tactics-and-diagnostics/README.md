# Phase 9 — Tactics & diagnostics integration

The v1.0 work wiring **tactics classification** into the pipeline and **weekly report** is **shipped**. This directory is a **brownfield** GSD anchor.

**Evidence**

- [Verification](./09-tactics-and-diagnostics-VERIFICATION.md) — TACTICS-01, TACTICS-02.
- [Validation](./09-VALIDATION.md).

**Primary entrypoints**

- `run_pipeline.py` — `step9_tactics` (`STEPS[9]`).
- `pipelines/09_tactics.py` — stand-alone step 9.
- `src/trading_crab_lib/tactics.py` — `compute_tactics_metrics`, `classify_tactics`.
- Artifact: `outputs/reports/tactics_signals.parquet` (column `tactics_label`, etc.).
- `trading_crab_lib.reporting.write_weekly_report_md` — optional **## Tactics** section when the parquet exists.

See **`RUNBOOK.md`** for operational context.
