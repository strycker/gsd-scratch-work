# Phase 17 — Execution summary (DATA-10)

**Plan:** `17-v1-2-expanded-macro-signals-01-PLAN.md`  
**Executed:** 2026-03-21  
**Requirement:** DATA-10 — expanded FRED series and yield spreads in feature lists.

## What shipped

- **`config/settings.yaml`** — `fred.series` unchanged (already listed Phase 8 FRED IDs). **`features.log_columns`**, **`initial_features`**, and **`clustering_features`** now include:
  - **Levels (log where appropriate):** `fred_vix`, `fred_unrate`, `fred_m2sl`, `fred_m2ns`, `fred_houst`, `fred_umcsent`
  - **Rate:** `fred_gs2` (derivatives in clustering, same as `fred_gs10`)
  - **Spreads:** `yc_10y_2y`, `yc_10y_3m`, `yc_2y_3m` from `add_yield_curve_features` (not `fred_t10y2y` / `fred_t10y3m` in features — avoids double-counting; see `17-CONTEXT.md`).
- **`17-CONTEXT.md`** — decision table + redundancy rule.
- **`RUNBOOK.md`** — checkpoint bullet for FRED / macro feature changes.
- **`.planning/REQUIREMENTS.md`** — DATA-10 marked complete.
- **Tests:** `tests/unit/test_transforms.py` — `add_yield_curve_features`, `engineer_all` smoke (narrowed cfg + synthetic frame); `tests/unit/test_fred_series_config.py` — no FRED T10Y spread duplicates in clustering.

## Verification

- `pytest tests/unit/test_transforms.py tests/unit/test_fred_series_config.py -q`
- `python -c "from trading_crab_lib.config import load; load(); print(len(load()['features']['clustering_features']))"`

## Manual

- With `FRED_API_KEY`: `python run_pipeline.py --steps 1,2 --recompute` and inspect processed features / checkpoints for new columns.

## Post-merge ops

**Changing `clustering_features` invalidates prior clusters.** Re-run **`--recompute` + steps 3–7** and **`config/regime_labels.yaml`** per **`RUNBOOK.md`** before treating regime labels as stable.

## Task 4 (optional ingest mock)

- **Not added:** a new `fredapi` mock test (existing `fetch_all` is integration-oriented). Manual smoke above is documented as sufficient for this phase.
