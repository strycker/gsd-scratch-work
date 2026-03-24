---
phase: 22-v1-2-providers-universe
verified: 2026-03-24T18:00:00Z
status: passed
requirements:
  - DATA-11
---

# Phase 22: Providers & ETF universe — Verification Report

**Phase goal (ROADMAP):** Optional data providers and broader ETF list behind config; preserve checkpoint contracts.

**Requirement:** DATA-11

**Verified:** 2026-03-24

**Overall status:** `passed` — evidence matches `22-SUMMARY.md` and tests below.

---

## Observable truths

| # | Truth | Status | Evidence |
|---|--------|--------|----------|
| 1 | `assets.providers` toggles provider usage; defaults documented. | ✓ | `config/settings.yaml` `assets.providers`; comment block above `assets.etfs`. |
| 2 | Ingestion respects flags; stooq fallback paths (per-ticker / bulk) as shipped. | ✓ | `src/trading_crab_lib/ingestion/assets.py` `_provider_flags()` and merge logic. |
| 3 | Contract tests for providers and index. | ✓ | `tests/unit/test_assets_providers.py`; `tests/unit/test_end_date_null_fallback.py` (see `22-SUMMARY.md`). |
| 4 | Operational docs for asset prices & providers. | ✓ | `RUNBOOK.md` section **Asset prices & providers (DATA-11)**. |

---

## Requirements coverage

| Requirement | Status |
|-------------|--------|
| **DATA-11** | ✓ SATISFIED |

---

## Automated verification commands (re-run)

```bash
python -c "from trading_crab_lib.config import load; assert 'providers' in load()['assets']"
PYTHONPATH=src python -m pytest tests/unit/test_assets_providers.py tests/unit/test_end_date_null_fallback.py -q
python -m compileall -q src/trading_crab_lib/ingestion/assets.py
```
