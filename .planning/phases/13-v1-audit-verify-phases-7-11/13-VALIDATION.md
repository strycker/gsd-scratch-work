---
phase: 13-v1-audit-verify-phases-7-11
validated: 2026-03-19T00:00:00Z
plan: 13-v1-audit-verify-phases-7-11-01-PLAN.md
status: complete
---

# Phase 13 — Validation (Nyquist contract)

## Test infrastructure

| Layer | Command / artifact | Notes |
|-------|-------------------|--------|
| Unit / integration | `pytest tests/test_scripts_weekly_report.py tests/test_email_weekly.py tests/test_tactics.py -q` | Email + weekly script + tactics (no network). |
| Diagnostics helpers | `pytest tests/unit/test_diagnostics_rrg.py -q` | RRG math (Phase 8 alignment). |
| Env smoke | `bash scripts/check_env.sh` | Import `trading_crab_lib` + one model test node. |
| Full E2E | *manual* | `run_pipeline.py --steps 8,9` with existing checkpoints — not required for Phase 13 doc closure. |

## Per-task map (plan Tasks 1–7)

| Task | Verify |
|------|--------|
| 1 — REQUIREMENTS traceability | `grep` PORT-04, REPORT-03, DATA-04, DIAG-01, DIAG-02, TACTICS-01..03, INSTALL-10, CORE-01, CORE-02 in `.planning/REQUIREMENTS.md` table + narrative §8. |
| 2 — Phase 07 VERIFICATION | File exists; `status: passed`; cites `load_portfolio`, `email.py`, `run_pipeline` flags. |
| 3 — Phase 08 VERIFICATION | File exists; FRED IDs match `settings.yaml`; step 8 paths cited. |
| 4 — Phase 09 VERIFICATION | File exists; `tactics_signals.parquet` filename matches `pipelines/09_tactics.py`. |
| 5 — Phase 10 VERIFICATION | File exists; `test_tactics.py` + install scripts cited. |
| 6 — Phase 11 VERIFICATION | File exists; `gaps_found` for CORE-02 tests if no pytest coverage. |
| 7 — ROADMAP / plan checkbox | Phase 13 plan `[x]`; progress row `1/1`. |

## Known gap (from Phase 11)

- **CORE-02:** Add unit test for `data.end_date: null` → `date.today()` in FRED/assets ingestion before promoting CORE-02 to **Complete** in traceability.

## Exit criteria

- [x] Five `*-VERIFICATION.md` files under phases `07`–`11`.
- [x] `REQUIREMENTS.md` extended with §8 narrative + traceability rows for Phase 13 IDs.
- [x] `13-VALIDATION.md` (this file) committed with Phase 13 execution.
- [x] `ROADMAP.md` Phase 13 plan marked complete.

## Follow-on (Phase 14)

Planning reconciliation per `.planning/ROADMAP.md` Phase 14: align any stale `STATE.md` / legacy package path mentions with `trading_crab_lib` in older verification docs.

**Validator note:** Run pytest in a project venv with `pip install -e ".[dev]"` so `python-dotenv` and other deps resolve (CI uses the same contract).
