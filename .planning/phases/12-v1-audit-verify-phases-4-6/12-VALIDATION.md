---
phase: 12
slug: v1-audit-verify-phases-4-6
status: complete
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-19
---

# Phase 12 — Validation strategy (Nyquist)

> Gap-closure phase: verification documents for roadmap phases 4–6 + `run_pipeline` parity. Most evidence is **planning artifacts**; automated hooks tie **PORT/UX/REPORT** to existing and new unit tests.

---

## Test infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.x |
| **Config file** | `pyproject.toml` |
| **Quick run command** | `pytest tests/unit/test_returns.py tests/unit/test_phase12_gsd_validation.py tests/test_scripts_weekly_report.py -q` |
| **Full suite command** | `pytest -q` |
| **Syntax guard** | `python3 -m py_compile run_pipeline.py` |
| **Estimated runtime** | &lt; 60 seconds |

---

## Sampling rate

- After changes to `run_pipeline.py` steps 6–7: quick run above + `py_compile`
- Before merge / `$gsd-audit-milestone`: full `pytest -q`
- Max feedback latency: 90s target

---

## Per-task verification map

| Task ID | Plan | Wave | Requirement | Test type | Automated command | File exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 12-01-01 | 01 | 1 | Discovery (parity) | smoke | `python3 -m py_compile run_pipeline.py` | — | ✅ green |
| 12-02-01 | 01 | 1 | PORT-01..03 | unit | `pytest tests/unit/test_returns.py -q` | ✅ | ✅ green |
| 12-03-01 | 01 | 1 | UX-01, REPORT-02 (helpers) | unit | `pytest tests/unit/test_phase12_gsd_validation.py -q` | ✅ | ✅ green |
| 12-04-01 | 01 | 1 | REPORT-01 | unit | `pytest tests/test_scripts_weekly_report.py -q` | ✅ | ✅ green |
| 12-05-01 | 01 | 1 | Docs: VERIFICATION 04–06 | manual | Review `04/05/06-*-VERIFICATION.md` | ✅ | ✅ green |
| 12-06-01 | 01 | 1 | Traceability / ROADMAP | manual | `grep -E 'PORT-0|UX-0|REPORT-0' .planning/REQUIREMENTS.md` | ✅ | ✅ green |

*Status: ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 requirements

- [x] `tests/unit/test_returns.py` — `returns_by_regime`, `behavior_tables`, `compute_template_returns` (PORT-01, PORT-02 mechanics)
- [x] `tests/unit/test_phase12_gsd_validation.py` — `generate_recommendation`, `write_weekly_report_md` (UX-01, REPORT-02 prose contract)
- [x] `tests/test_scripts_weekly_report.py` — weekly script argv / archive (REPORT-01)
- [x] `04/05/06-*-VERIFICATION.md` — milestone evidence

---

## Manual-only verifications

| Behavior | Requirement | Why manual | Test instructions |
|----------|---------------|------------|-------------------|
| Numeric sanity of live `asset_return_profile` / behavior layouts on real data | PORT-01..03 | Needs real checkpoints + judgment | Run steps 1–6; open parquet / plots |
| Whether weekly prose is “good enough” for your clients | UX-02, REPORT-02 | Tone and completeness | Read `outputs/reports/weekly_report.md` after full run |

---

## Validation sign-off

- [x] All tasks have automated verify **or** explicit manual-only row
- [x] No three consecutive tasks without automated or documented manual path
- [x] Wave 0 covers PORT math, UX recommendation helper, weekly script
- [x] No watch-mode flags in sampling plan
- [x] `nyquist_compliant: true` in frontmatter

**Approval:** 2026-03-19

---

## Validation audit 2026-03-19

| Metric | Count |
|--------|------:|
| Gaps found (initial audit) | 3 areas: thin VALIDATION.md, no dedicated UX/weekly unit tests, planning-only tasks |
| Resolved | Added `test_phase12_gsd_validation.py`; expanded Nyquist tables; mapped to existing `test_returns` + `test_scripts_weekly_report` |
| Escalated to manual | Full multi-step E2E parity (live `data/` + network optional) |
