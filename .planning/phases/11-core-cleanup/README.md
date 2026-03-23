# Phase 11 — Core cleanup & env sanity

The v1.0 **core cleanup** scope—predictable **`data/` / `outputs/`** trees, **`data.end_date: null`** resolving to today (tested), and consistent modern imports—is **shipped**. This directory is a **brownfield** GSD anchor.

**Evidence**

- [Verification](./11-core-cleanup-VERIFICATION.md) — CORE-01, CORE-02, import convention.
- [Validation](./11-VALIDATION.md).

**Code touchpoints (see Verification for detail)**

- `scripts/setup.sh` — directory scaffold.
- `src/trading_crab_lib/ingestion/fred.py`, `ingestion/assets.py` — null `end_date` → today.
- `tests/unit/test_end_date_null_fallback.py` — CORE-02 regression tests.
