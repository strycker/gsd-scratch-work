# Plan 01 — Hybrid summary (Phase 18, SIGNAL-10 / SIGNAL-11)

**Plan:** `18-v1-2-signal-diagnostics-01-PLAN.md`  
**Phase narrative:** `18-SUMMARY.md`

## As-built

- `config/settings.yaml` drives `diagnostics.*` (triggers, `weekly_report_include`, RRG lookback).
- `src/trading_crab_lib/diagnostics.py` — shared ratio + trigger evaluation; `plotting.py` — diagnostics figures; `reporting.py` — optional **## Diagnostics** in weekly markdown.
- `run_pipeline.py` step 8 and `pipelines/08_diagnostics.py` share behavior; tests in `tests/unit/test_diagnostics_ratios.py`, `test_diagnostics_rrg.py`, `test_weekly_report_diagnostics.py`.
- `notebooks/08_diagnostics.ipynb` documents parquet + plot paths; step 8 remains read-only on prices checkpoint per contract.

## Plan fidelity

- Close **SIGNAL-10** and **SIGNAL-11**: productize step 8 with YAML-first trigger rules, stable parquets under `outputs/reports/diagnostics/`, RRG-style machine-readable outputs, weekly report + notebook hooks, plots under `outputs/plots/` when configured.
- Do not mutate clustering/supervised feature matrices or copy diagnostics into `features.parquet` unless explicitly documented.

## Delta from plan

- **Complete:** Config audit pattern, triggers, plots, weekly section, tests, RUNBOOK / REQUIREMENTS pointers per `18-SUMMARY.md`.
- **Superseded / ops:** `18-SUMMARY.md` notes re-run step **7** after **8** if same-run weekly must include Diagnostics — ordering refined further in **Phase 27** (`resolve_pipeline_step_order`).
