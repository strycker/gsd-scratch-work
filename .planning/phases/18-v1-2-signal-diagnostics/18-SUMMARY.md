# Phase 18 — Execution summary (SIGNAL-10 / SIGNAL-11)

**Plan:** `18-v1-2-signal-diagnostics-01-PLAN.md`  
**Executed:** 2026-03-21  
**Requirements:** SIGNAL-10, SIGNAL-11

## What shipped

- **`config/settings.yaml`** — `diagnostics.weekly_report_include`, `rrg_lookback`, `trigger_defaults` (`z_abs_min`, `percentile_high`, `percentile_low`); per-ratio overrides via `triggers:` on a ratio entry.
- **`src/trading_crab_lib/diagnostics.py`** — `merge_trigger_config`, `evaluate_ratio_triggers`, `compute_ratios_diagnostics` (shared by `run_pipeline` step 8 and `pipelines/08_diagnostics.py`).
- **`src/trading_crab_lib/plotting.py`** — `plot_diagnostics_ratios_summary`, `plot_diagnostics_rrg` → `08_diagnostics_ratios.png`, `08_diagnostics_rrg.png`.
- **`src/trading_crab_lib/reporting.py`** — `write_weekly_report_md(..., cfg=...)` + optional **## Diagnostics** via `_append_diagnostics_section`.
- **`run_pipeline.py` `step8_diagnostics`** — uses shared compute, configurable RRG lookback, plots when `--plots`.
- **`pipelines/08_diagnostics.py`** — aligned with step 8 behavior.
- **`pipelines/07_dashboard.py`** — passes `cfg` into `write_weekly_report_md`.
- **Tests:** `tests/unit/test_diagnostics_ratios.py`, `tests/unit/test_weekly_report_diagnostics.py`.
- **`notebooks/08_diagnostics.ipynb`** — loads diagnostic parquets and lists plot filenames.
- **`RUNBOOK.md`**, **`.planning/REQUIREMENTS.md`** — traceability.

## Verification

- `pytest tests/unit/test_diagnostics_ratios.py tests/unit/test_diagnostics_rrg.py tests/unit/test_weekly_report_diagnostics.py tests/unit/test_phase12_gsd_validation.py -q`
- `python -c "from trading_crab_lib.config import load; load()"`

## Manual

- `python run_pipeline.py --steps 6,8 --plots` (needs `data/raw/asset_prices.parquet`).

## Ops note

Re-run step **7** after step **8** if you need `weekly_report.md` to include the **Diagnostics** section in the same run order.
