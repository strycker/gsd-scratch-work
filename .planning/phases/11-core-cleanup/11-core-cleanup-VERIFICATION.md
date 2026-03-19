---
phase: 11-core-cleanup
verified: 2026-03-19T00:00:00Z
status: gaps_found
score: 2/3 roadmap success themes fully verified in automated tests (CORE-01 ✓, import style ✓, CORE-02 partial)
human_verification:
  - test: "Set data.end_date: null in settings.yaml; run ingestion paths (mock or live)"
    expected: "FRED and yfinance calls use today's calendar date as end bound."
    why_human: "Confirms runtime behavior beyond static code read."
gaps_found:
  - id: CORE-02-tests
    detail: "No dedicated unit test asserts `cfg['data']['end_date'] is None` → end string equals `date.today()` in FRED/ETF fetchers (implementation present; coverage gap)."
    next_action: "Add tests that monkeypatch `date.today` or pass cfg with null end_date into ingest helpers."
---

# Phase 11: Core Cleanup & Env Sanity — Verification

**Phase goal (ROADMAP):** Predictable directories, null-safe `end_date`, consistent modern imports.  
**Audit closure:** Phase 13 — evidence for CORE-01, CORE-02 (+ import convention).  
**Status:** **gaps_found** — **CORE-02** implementation verified in source; **automated test** for null `end_date` **missing**.

## Requirement coverage

| ID | Description | Status | Evidence |
|----|-------------|--------|----------|
| CORE-01 | `data/` and `outputs/` subtrees created by setup or pipeline | ✓ | `scripts/setup.sh` creates `data/raw`, `data/processed`, `data/regimes`, `data/checkpoints`, `outputs/plots`, `outputs/models`, `outputs/reports`. `run_pipeline.py` / steps use `mkdir(parents=True, exist_ok=True)` for `raw`, `processed`, `regimes`, `models`, `reports`, diagnostics dirs, etc. |
| CORE-02 | `data.end_date` null → effective “today”; **tested** | **partial** | **Implementation:** `trading_crab_lib.ingestion.fred` uses `end = cfg["data"]["end_date"] or str(date.today())`. `trading_crab_lib.ingestion.assets` uses same pattern for ETF fetch. **Tests:** repository `tests/` grep shows **no** `end_date` null/today assertion tied to ingestion (gap). |
| (ROADMAP §3) | `from __future__ import annotations` consistency in key modules | ✓ | Convention followed across `trading_crab_lib` sources and many `tests/*` files (spot-check + grep patterns in test suite). |

## Code references (CORE-02)

- `src/trading_crab_lib/ingestion/fred.py` — `end = cfg["data"]["end_date"] or str(date.today())`
- `src/trading_crab_lib/ingestion/assets.py` — `end = cfg["data"]["end_date"] or str(date.today())`

## Tests

| Test file | CORE-02 |
|-----------|---------|
| *(none)* | Add `tests/unit/test_end_date_fallback.py` or extend ingest tests |

## `key_links`

| From | To | Via |
|------|----|-----|
| `scripts/setup.sh` | Directory scaffold | `mkdir -p data/... outputs/...` |
| `config/settings.yaml` | `data.end_date` | Loaded by `trading_crab_lib.config.load()` |
| `ingestion/fred.py`, `ingestion/assets.py` | Fetch window | Null-coalescing to today |

## Summary for auditors

- **CORE-01:** **passed** — scripts + pipeline create expected layout.  
- **CORE-02:** **gaps_found** for **test coverage** only; runtime behavior matches ROADMAP intent in code.  
- **Import style:** **passed** — aligned with project conventions.

After adding a focused unit test for null `end_date`, this document’s frontmatter can move to `status: passed` and `REQUIREMENTS.md` CORE-02 row to **Complete**.

## Evidence checklist (audit)

- [x] `scripts/setup.sh` provisions canonical `data/` + `outputs/` paths.
- [x] Pipeline steps create canonical dirs opportunistically (`run_pipeline.py` / step implementations).
- [x] `end_date or today` idiom present in FRED and assets ingestion.
- [ ] Unit test locking null `end_date` behavior (missing — see `gaps_found`).

## Related documentation

- `CLAUDE.md` — Python 3.10+ / `from __future__ import annotations` convention for library code.
- Phase 14 roadmap — planning reconciliation (`market_regime` vs `trading_crab_lib` naming drift in older docs).

## Revision history

- 2026-03-19 — Phase 13 audit: initial `*-VERIFICATION.md` for roadmap Phase 11 (`gaps_found` on CORE-02 tests).
