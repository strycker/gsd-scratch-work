# Phase 8 — Data, signals & diagnostics

The v1.0 work for **extra FRED series**, **config-driven diagnostic ratios**, and **RRG-style outputs** is **shipped**. This directory is a **brownfield** GSD anchor.

**Plan–summary parity (CLOSURE-01)**

- [`08-data-signals-diagnostics-01-PLAN.md`](./08-data-signals-diagnostics-01-PLAN.md) ↔ [`08-data-signals-diagnostics-01-SUMMARY.md`](./08-data-signals-diagnostics-01-SUMMARY.md).

**Evidence**

- [Verification](./08-data-signals-diagnostics-VERIFICATION.md) — DATA-04, DIAG-01, DIAG-02.
- [Validation](./08-VALIDATION.md).

**Primary entrypoints**

- `run_pipeline.py` — `step1_ingest`, **`step8_diagnostics`** (`STEPS[8]`).
- `pipelines/01_ingest.py` / `pipelines/08_diagnostics.py` — ingest + diagnostics.
- `config/settings.yaml` — `fred.series`, `diagnostics.ratios`, `diagnostics.rrg_benchmarks`.
- Outputs: `outputs/reports/diagnostics/ratios_current.parquet`, `rrg_current.parquet`.

See **`RUNBOOK.md`** for run sequences.
