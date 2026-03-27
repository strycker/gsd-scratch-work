---
phase: 38
slug: v1-5-backlog-reconciliation
status: approved
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-27
---

# Phase 38 — Validation Strategy

> Retroactive Nyquist contract for **TMPL-02** (backlog reconciliation). Phase is **documentation-only**; automated coverage is via **`tests/unit/test_phase38_planning_validation.py`**.

## Test infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest — `pyproject.toml` `[tool.pytest.ini_options]` |
| **Phase-specific tests** | `tests/unit/test_phase38_planning_validation.py` |
| **Quick run command** | `pytest tests/unit/test_phase38_planning_validation.py -q` |
| **Full suite command** | `pytest tests/ -q` |
| **Estimated runtime** | &lt; 5 s |

## Sampling rate

- After edits to **root `ROADMAP.md`**, **`CLAUDE.md`**, **`.planning/FUTURE-TODO.md`**, or **`v1.5-CLEANUP-BACKLOG.md`**: run **`pytest tests/unit/test_phase38_planning_validation.py -q`**
- Before milestone sign-off: full **`pytest tests/ -q`**

## Per-task verification map

| Task | Plan | Wave | Requirement | Test type | Command / check |
|------|------|------|-------------|-----------|-----------------|
| 38-01-01 | 01 | 1 | TMPL-02 | unit | `test_product_roadmap_tier13_yield_shipped_story`, `test_product_roadmap_tier14_forward_window_shipped` |
| 38-01-02 | 01 | 1 | TMPL-02 | unit | `test_claude_gap6_and_no_missing_empirical_forward_bullet` |
| 38-01-03 | 01 | 1 | TMPL-02 | unit | `test_future_todo_forward_window_paths`, `test_cleanup_backlog_phase38_note` |
| REQUIREMENTS | 01 | 1 | TMPL-02 | unit | `test_requirements_tmpl02_complete` |

## Wave 0

- **Existing infrastructure** covers phase scope; Nyquist tests added in **`test_phase38_planning_validation.py`**.

## Manual-only verifications

| Behavior | Why manual |
|----------|------------|
| Editorial quality of Tier 1 prose in **`ROADMAP.md`** | Subjective — not fully asserted |

## Validation sign-off

- [x] `pytest tests/unit/test_phase38_planning_validation.py -q` green
- [x] `nyquist_compliant: true` in frontmatter
- [x] Phase **`38-VERIFICATION.md`** documents goal-backward checks

**Approval:** approved 2026-03-27 — `$gsd:validate-phase 38` (retroactive validation strategy + tests)
