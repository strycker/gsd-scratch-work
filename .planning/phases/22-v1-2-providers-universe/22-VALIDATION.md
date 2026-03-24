---
phase: 22
slug: v1-2-providers-universe
status: validated
nyquist_compliant: true
created: 2026-03-23
validated: 2026-03-20
---

# Phase 22 — Validation Strategy

> DATA-11 — optional providers + ETF universe documentation + ingestion contracts.

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config** | `pyproject.toml` (`pythonpath = ["src"]`) |
| **Primary** | `PYTHONPATH=src python -m pytest tests/unit/test_assets_providers.py tests/unit/test_end_date_null_fallback.py -q` |

## Per-Task Map

| Task | Requirement | Automated Command | Status |
|------|-------------|-------------------|--------|
| 22-01-01 | Config | `python -c "from trading_crab_lib.config import load; a=load().get('assets',{}); assert 'providers' in a"` | ✅ |
| 22-01-02 | Toggles | `pytest tests/unit/test_assets_providers.py -q` | ✅ |
| 22-01-03 | End-date regression | `pytest tests/unit/test_end_date_null_fallback.py -q` | ✅ |

## Manual-Only

| Behavior | Why manual |
|----------|------------|
| Live Yahoo / stooq / OpenBB | Network + rate limits |

## Validation Audit 2026-03-23

Automated commands run at phase execute; all green.

### Re-verify (`$gsd:verify-phase 22`) — 2026-03-20

| Check | Result |
|-------|--------|
| `python -c "… assert 'providers' in load()['assets']"` | OK |
| `pytest tests/unit/test_assets_providers.py tests/unit/test_end_date_null_fallback.py` | **8 passed** |
| `compileall src/trading_crab_lib/ingestion/assets.py` | OK |

## Sign-Off

- [x] `nyquist_compliant: true`

**Approval:** automated verification complete.
