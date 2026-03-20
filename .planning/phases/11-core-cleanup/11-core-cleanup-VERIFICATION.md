---
phase: 11-core-cleanup
verified: 2026-03-19T00:00:00Z
status: passed
score: 3/3 roadmap success themes (CORE-01 ✓, CORE-02 ✓, import style ✓)
human_verification:
  - test: "Set data.end_date: null in settings.yaml; run ingestion paths (mock or live)"
    expected: "FRED and yfinance calls use today's calendar date as end bound."
    why_human: "Confirms runtime behavior beyond static code read."
---

# Phase 11: Core Cleanup & Env Sanity — Verification

**Phase goal (ROADMAP):** Predictable directories, null-safe `end_date`, consistent modern imports.  
**Audit closure:** Phase 13 — evidence for CORE-01, CORE-02 (+ import convention).  
**Status:** **passed**.

## Requirement coverage

| ID | Description | Status | Evidence |
|----|-------------|--------|----------|
| CORE-01 | `data/` and `outputs/` subtrees created by setup or pipeline | ✓ | `scripts/setup.sh` creates `data/raw`, `data/processed`, `data/regimes`, `data/checkpoints`, `outputs/plots`, `outputs/models`, `outputs/reports`. `run_pipeline.py` / steps use `mkdir(parents=True, exist_ok=True)` for `raw`, `processed`, `regimes`, `models`, `reports`, diagnostics dirs, etc. |
| CORE-02 | `data.end_date` null → effective “today”; **tested** | ✓ | **Implementation:** `trading_crab_lib.ingestion.fred` and `ingestion.assets` use `end = cfg["data"]["end_date"] or str(date.today())`. **Tests:** `tests/unit/test_end_date_null_fallback.py` patches `date.today`, asserts `observation_end` / `_batch_yfinance` `end` match fixed “today”; regression tests for explicit `end_date`. |
| (ROADMAP §3) | `from __future__ import annotations` consistency in key modules | ✓ | Convention followed across `trading_crab_lib` sources and many `tests/*` files (spot-check + grep patterns in test suite). |

## Code references (CORE-02)

- `src/trading_crab_lib/ingestion/fred.py` — `end = cfg["data"]["end_date"] or str(date.today())`
- `src/trading_crab_lib/ingestion/assets.py` — `end = cfg["data"]["end_date"] or str(date.today())`

## Tests

| Test file | CORE-02 |
|-----------|---------|
| `tests/unit/test_end_date_null_fallback.py` | FRED + assets fetch window end when `end_date` is `None` vs explicit string |

## `key_links`

| From | To | Via |
|------|----|-----|
| `scripts/setup.sh` | Directory scaffold | `mkdir -p data/... outputs/...` |
| `config/settings.yaml` | `data.end_date` | Loaded by `trading_crab_lib.config.load()` |
| `ingestion/fred.py`, `ingestion/assets.py` | Fetch window | Null-coalescing to today |

## Summary for auditors

- **CORE-01:** **passed** — scripts + pipeline create expected layout.  
- **CORE-02:** **passed** — code + dedicated unit tests.  
- **Import style:** **passed** — aligned with project conventions.

## Evidence checklist (audit)

- [x] `scripts/setup.sh` provisions canonical `data/` + `outputs/` paths.
- [x] Pipeline steps create canonical dirs opportunistically (`run_pipeline.py` / step implementations).
- [x] `end_date or today` idiom present in FRED and assets ingestion.
- [x] Unit tests lock null `end_date` behavior (`test_end_date_null_fallback.py`).

## Related documentation

- `CLAUDE.md` — Python 3.10+ / `from __future__ import annotations` convention for library code.
- Phase 14 roadmap — planning reconciliation (`market_regime` vs `trading_crab_lib` naming drift in older docs).

## Revision history

- 2026-03-19 — Phase 13 audit: initial `*-VERIFICATION.md` for roadmap Phase 11 (`gaps_found` on CORE-02 tests).
- 2026-03-19 — CORE-02 closed: `tests/unit/test_end_date_null_fallback.py`; status → **passed**.
