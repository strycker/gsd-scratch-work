# Phase 20 — Execution summary (TACTICS-10)

**Plan:** `20-v1-2-tactics-layer-01-PLAN.md`  
**Executed:** 2026-03-23  
**Requirement:** TACTICS-10

## What shipped

- **`src/trading_crab_lib/tactics.py`**
  - Snapshot columns: **`as_of`**, **`quarter_end`**, **`last_price`**
  - **`soft_stop_z`** — z-score of last close vs rolling mean (`soft_stop_proxy.window`); optional disable via `enabled: false`
  - **`entry_bias_score`** — `tanh(slope_short − slope_long)` from `entry_bias.short_slope_window` / `long_slope_window`
  - **`classify_tactics`**: **`classification_version`** — `v1` (legacy mid-vol + lexicographic first slope) vs **`v1_2`** ( **`vol_aggregate`** over all `vol_*` + shortest-window `slope_*` )
  - **`min_corr_spy`** — optional floor; below → `stand_aside`
- **`config/settings.yaml`** — `classification_version`, `vol_aggregate`, `entry_bias`, `soft_stop_proxy`, `min_corr_spy`, `weekly_report_enrich`, default **`trend_windows: [5, 20, 60]`**
- **`reporting.write_weekly_report_md`** — when **`tactics.weekly_report_enrich: true`** and parquet has **`entry_bias_score`** / **`soft_stop_z`**, appends enriched bullets under **## Tactics**
- **Tests** — `tests/test_tactics.py`: as_of/quarter columns, bounded entry bias, v1 vs v1_2 max-vol behavior, `min_corr_spy`

## Deferred

- **Anchored VWAP** with volume — still using rolling-mean z-score as proxy (documented in plan CONTEXT).

## Verification

- `PYTHONPATH=src python -m pytest tests/test_tactics.py -q`
- `python -c "from trading_crab_lib.config import load; load()"`
