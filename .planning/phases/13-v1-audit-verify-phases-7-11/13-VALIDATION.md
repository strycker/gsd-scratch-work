---
phase: 13-v1-audit-verify-phases-7-11
slug: v1-audit-verify-phases-7-11
validated: 2026-03-20T00:00:00Z
plan: 13-v1-audit-verify-phases-7-11-01-PLAN.md
status: complete
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-19
---

# Phase 13 — Validation Strategy (Nyquist contract)

> **GSD:** `GSD > VALIDATE PHASE 13: v1-audit-verify-phases-7-11`  
> Per-phase validation contract for Phase 13 (audit + verification docs for roadmap phases 7–11).

Phase 13 is **documentation-first**: primary deliverables are `*-VERIFICATION.md` files and `REQUIREMENTS.md` traceability. **Implementation behavior** is cross-checked with **automated tests** that already target the underlying REQ IDs (not new tests for “markdown exists” — those are **file/section audits** below).

---

## Test infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest ≥8 (`pyproject.toml` `[tool.pytest.ini_options]`) |
| **Config file** | `pyproject.toml` (`testpaths = ["tests"]`, `pythonpath = ["src"]`) |
| **Quick run (Phase 13 REQ slice)** | `.venv/bin/python -m pytest tests/unit/test_end_date_null_fallback.py tests/test_scripts_weekly_report.py tests/test_email_weekly.py tests/test_tactics.py tests/unit/test_diagnostics_rrg.py tests/unit/test_fred_series_config.py -q` |
| **Full suite** | `.venv/bin/python -m pytest tests/ -q` (after `pip install -e ".[dev]"`) |
| **Env smoke** | `bash scripts/check_env.sh` |
| **Estimated runtime (slice)** | ~5–30s (depends on machine / cold import) |

**Interpreter:** Use an environment where `python-dotenv` resolves (`trading_crab_lib` import). Project deps: `pip install -e ".[dev]"` from repo root (`.venv/` gitignored).

---

## Sampling rate

- **After Phase-13-style doc edits:** Run the **quick slice** above.
- **Before milestone audit:** Full `tests/` green on CI or local venv.
- **Max feedback latency:** Prefer slice under ~60s for inner loop.

---

## Per-task verification map (Plan `13-v1-audit-verify-phases-7-11-01-PLAN.md`)

| Task ID | Plan | Wave | Focus / REQ IDs | Test type | Automated command / audit | File exists | Status |
|---------|------|------|-----------------|-----------|---------------------------|-------------|--------|
| 1 | 01 | 1 | §8 + traceability table (PORT-04…CORE-02) | **audit** | `grep` IDs in `.planning/REQUIREMENTS.md` | ✅ | ✅ green |
| 2 | 01 | 1 | 07 VERIFICATION — PORT-04, REPORT-03 | **audit** + **unit** | `.planning/phases/07-…/07-…-VERIFICATION.md` + `pytest tests/test_scripts_weekly_report.py tests/test_email_weekly.py` | ✅ | ✅ green * |
| 3 | 01 | 1 | 08 VERIFICATION — DATA-04, DIAG-01/02 | **audit** + **unit** | `08-…-VERIFICATION.md` + `pytest tests/unit/test_fred_series_config.py tests/unit/test_diagnostics_rrg.py` | ✅ | ✅ green * |
| 4 | 01 | 1 | 09 VERIFICATION — TACTICS-01/02 | **audit** + **unit** | `09-…-VERIFICATION.md` + `pytest tests/test_tactics.py` | ✅ | ✅ green * |
| 5 | 01 | 1 | 10 VERIFICATION — TACTICS-03, INSTALL-10 | **audit** | `10-…-VERIFICATION.md` + `scripts/check_env.sh` (smoke) | ✅ | ✅ green * |
| 6 | 01 | 1 | 11 VERIFICATION — CORE-01/02 | **audit** + **unit** | `11-…-VERIFICATION.md` + `pytest tests/unit/test_end_date_null_fallback.py` | ✅ | ✅ green * |
| 7 | 01 | 1 | ROADMAP Phase 13 complete | **audit** | `.planning/ROADMAP.md` Phase 13 `[x]`, progress `1/1` | ✅ | ✅ green |

\*Automated commands require a venv with `pip install -e ".[dev]"` (see **Test infrastructure**). `test_end_date_null_fallback.py` alone can run without importing package `__init__` (importlib loader).

---

## Wave 0 requirements

- [x] Existing `tests/` layout covers Phase 7–11 **behavioral** requirements (portfolio/email/tactics/diagnostics/FRED config/CORE-02).
- [x] **No new Wave-0 stubs required** for Phase 13 — phase scope is verification docs + traceability.

---

## Manual-only verifications

| Behavior | Requirement | Why manual | Test instructions |
|----------|-------------|------------|-------------------|
| Live SMTP send | REPORT-03 | Needs real creds + mailbox | Configure `config/email.local.yaml`; run `scripts/run_weekly_report.py --send-email` or `run_pipeline.py --send-email`. |
| Live FRED fetch | DATA-04 | Needs `FRED_API_KEY` + network | `run_pipeline.py --refresh --steps 1` (or subset); inspect `macro_raw` columns. |
| Step 8/9 artifact smoke | DIAG-*, TACTICS-* | Needs checkpoints + prices | With existing `data/` artifacts: `run_pipeline.py --steps 8,9`; inspect `outputs/reports/diagnostics/*.parquet`, `tactics_signals.parquet`. |
| Human tone of weekly report | REPORT-02/03 (narrative) | Subjective | Open `outputs/reports/weekly_report.md` after full weekly flow. |

---

## Exit criteria (Phase 13)

- [x] Five `*-VERIFICATION.md` files under phases `07`–`11`.
- [x] `REQUIREMENTS.md` §8 + traceability rows for Phase 13 IDs (**CORE-02** Complete).
- [x] `13-VALIDATION.md` (this file) maintained.
- [x] `ROADMAP.md` Phase 13 plan complete.

---

## Validation audit **2026-03-20**

| Metric | Count |
|--------|-------|
| Gaps found (Nyquist) | 0 — CORE-02 filled by `test_end_date_null_fallback.py` |
| Resolved | Phase 13 plan tasks 1–7 traced to docs + commands |
| Escalated | 0 |
| Manual-only rows | 4 (SMTP, FRED live, pipeline E2E smoke, narrative) |

**Sampling note:** Validator ran **automated slice** in a project venv when available; `test_end_date_null_fallback.py` passes on minimal interpreters without `python-dotenv` (importlib load path).

---

## Validation sign-off

- [x] All plan tasks have **automated** verify **or** **manual-only** / **audit** column above
- [x] Sampling continuity: behavioral REQs map to pytest or scripted smoke
- [x] No watch-mode flags required for Phase 13
- [x] `nyquist_compliant: true` — acceptable with documented manual-only network paths

**Approval:** approved **2026-03-20**

---

## Follow-on

- **Phase 14** — `.planning/ROADMAP.md`: planning reconciliation (`STATE.md`, path drift `market_regime` vs `trading_crab_lib`).
- **Next:** `$gsd-audit-milestone` when ready for v1.0 milestone close-out.
