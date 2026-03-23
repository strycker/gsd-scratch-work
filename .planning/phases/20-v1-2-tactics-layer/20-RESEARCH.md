# Phase 20 — Technical research (TACTICS-10)

**Date:** 2026-03-22  
**Question:** What do we need to implement to satisfy **TACTICS-10** and ROADMAP Phase 20 without duplicating v1.0 work?

## Current state (repo)

| Area | Finding |
|------|---------|
| Metrics | `compute_tactics_metrics` already emits multiple `vol_*`, `slope_*`, `corr_spy` per asset. |
| Labels | `classify_tactics` uses **one** vol column (middle of sorted `vol_*`) and **one** slope column — not full multi-horizon aggregation. |
| Parquet | One row per asset; **no** `as_of` / quarter columns. |
| Report | `write_weekly_report_md` lists assets by `tactics_label` only. |
| Config | `tactics:` has `vol_windows`, `vol_bands`, `trend_windows`, `trend_min_slope`, `corr_lookback`. |

## Gap vs TACTICS-10 / ROADMAP

1. **Multi-horizon** — REQUIREMENTS text: “multi-horizon volatility, trend, correlations”. **Implementation:** configurable reducer over `vol_*` columns + explicit use of multiple `slope_*` for bias; keep `corr_spy` in classification optionally (e.g. low correlation to SPY → stand_aside for beta plays) — **config-gated** to avoid behavior shock.
2. **Weekly-entry bias** — Add derived column(s) from short vs long slope alignment.
3. **Soft stops** — REQUIREMENTS mention “anchored VWAP ideas”. With **OHLCV not guaranteed**, use rolling-mean z-score as **documented proxy** in settings.
4. **Stable parquet + date/quarter** — Add `as_of`, `quarter_end` from latest price index.
5. **Tests** — Extend `tests/test_tactics.py` with fixtures that prove multi-horizon + bias + soft-stop columns behave deterministically.

## Dependencies

- Phase 18–19: no hard dependency; tactics uses `asset_prices.parquet` + cluster labels (same as step 9 today).

## Risks

- **Classification change** may re-bucket ETFs vs v1.0 — mitigate with `tactics.classification_version: "v1" | "v1_2"` or feature flag defaulting to **v1_2** only after tests document expected shifts.

## Validation Architecture

Phase 20 verification will use:

| Dimension | Approach |
|-----------|----------|
| **Unit** | `pytest tests/test_tactics.py` — synthetic prices, assert columns + label rules. |
| **Config** | `load()` succeeds; new keys documented in `RUNBOOK.md`. |
| **Integration (manual)** | Optional: `run_pipeline.py --steps 9` with real checkpoints; inspect parquet columns. |
| **Report** | Parquet with new columns → weekly report still renders; optional extra bullets when `weekly_report_enrich_tactics: true` (if added). |

Automated gate for execute-phase: **`pytest tests/test_tactics.py -q`** green.

## Research complete

No external API research required. Implementation is confined to `trading_crab_lib`, YAML, tests, and reporting.

---

## RESEARCH COMPLETE
