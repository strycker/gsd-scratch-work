# Phase 22 — Execution summary (DATA-11)

**Plan:** `22-v1-2-providers-universe-01-PLAN.md`  
**Executed:** 2026-03-23  
**Requirement:** DATA-11

## What shipped

- **`config/settings.yaml`** — **`assets.providers`**: `yfinance`, `stooq`, `openbb` (all default **true**). Comment block above **`assets.etfs`** explains ingestion + returns/dashboard use and refresh after ticker changes.
- **`src/trading_crab_lib/ingestion/assets.py`** — **`_provider_flags()`**; Yahoo phases skipped when `yfinance: false`; **per-ticker stooq** for tickers still missing after batch + per-ticker Yahoo; **bulk stooq** only when no prices yet; OpenBB bulk only when still empty. Module docstring references **`trading-crab-lib[data-extras]`** and provider toggles.
- **`tests/unit/test_assets_providers.py`** — Toggle test (stooq never called when disabled), contract test (`date` index), partial Yahoo + stooq merge, default flags.
- **`RUNBOOK.md`** — Section **Asset prices & providers (DATA-11)** + Finviz note.

## Verification

```bash
python -c "from trading_crab_lib.config import load; assert 'providers' in load()['assets']"
PYTHONPATH=src python -m pytest tests/unit/test_assets_providers.py tests/unit/test_end_date_null_fallback.py -q
python -m compileall -q src/trading_crab_lib/ingestion/assets.py
```

## Manual

- Optional: `pip install -e ".[data-extras]"` for live stooq/OpenBB; confirm step 1 or 6 with `--refresh-assets` after editing tickers.
