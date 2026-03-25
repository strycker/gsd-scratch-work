# Plan 01 — Hybrid summary (Phase 22, DATA-11)

**Plan:** `22-v1-2-providers-universe-01-PLAN.md`  
**Phase narrative:** `22-SUMMARY.md`

## As-built

- `config/settings.yaml`: `assets.etfs` + `assets.providers` toggles (`yfinance`, `stooq`, `openbb`).
- `src/trading_crab_lib/ingestion/assets.py`: config-driven chain; disabled providers skipped; partial Yahoo → per-ticker stooq; ImportError/missing keys fail soft.
- `tests/unit/test_assets_providers.py`: mocks, no network in CI; `RUNBOOK.md` documents providers + Finviz note.

## Plan fidelity

- **DATA-11:** optional price providers behind config, documented ETF universe, stronger stooq on partial failures, regression tests preserving `asset_prices` checkpoint expectations.

## Delta from plan

- **Complete:** Provider toggles, fetch chain, tests, RUNBOOK per `22-SUMMARY.md`.
- **Non-goals honored:** No macrotrends / new mandatory paid vendors in this phase.
