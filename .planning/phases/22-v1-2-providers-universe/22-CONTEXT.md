---
phase: 22
slug: v1-2-providers-universe
status: locked
created: 2026-03-23
requirements:
  - DATA-11
---

# Phase 22 — Context (locked decisions)

## Boundary

Implement **DATA-11**: optional / configurable price-data providers and a **documented** ETF universe in `config/settings.yaml`, without breaking **`asset_prices`** / checkpoint contracts used by steps 1 and 6.

## Decisions

1. **Single config source** — `cfg["assets"]["etfs"]` remains the canonical ticker list; provider toggles live under `cfg["assets"]["providers"]`, not scattered env-only flags.
2. **Fail soft** — Missing optional packages (`pandas-datareader`, `openbb`) or missing API keys for future paid providers must **log + skip**, never abort the pipeline; empty matrix still defers to existing macro-proxy behavior in downstream steps.
3. **No Finviz historical API** — Finviz Elite does not expose historical OHLCV suitable for this pipeline; document “not applicable” in code comment or RUNBOOK and do **not** add a fake provider stub that implies it works.
4. **Checkpoint contract** — `asset_prices` checkpoint / `data/raw/asset_prices.parquet`: wide DataFrame, `date` index (quarter-end), one column per successfully fetched ticker from the configured list; changing ticker list implies operator refresh / `--refresh` semantics unchanged.
5. **Strengthen stooq** — Prefer **per-ticker stooq attempts for tickers still missing after yfinance phases** (when stooq is enabled), before declaring total failure and moving to OpenBB — so partial Yahoo outages don’t force an all-or-nothing fallback.

## Canonical refs

- `config/settings.yaml` — `assets` section
- `src/trading_crab_lib/ingestion/assets.py` — fetch chain
- `src/trading_crab_lib/checkpoints.py` — `asset_prices` save/load
- `.planning/REQUIREMENTS.md` — DATA-11
