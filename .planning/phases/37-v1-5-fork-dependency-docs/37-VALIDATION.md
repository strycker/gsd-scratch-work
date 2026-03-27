---
phase: 37
slug: v1-5-fork-dependency-docs
status: approved
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-27
---

# Phase 37 — Validation Strategy

> Retroactive Nyquist contract for **TMPL-01** (fork & dependency docs). Phase is **documentation-only**; automated coverage is via **`tests/unit/test_phase37_planning_validation.py`**.

## Test infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest — `pyproject.toml` `[tool.pytest.ini_options]` |
| **Phase-specific tests** | `tests/unit/test_phase37_planning_validation.py` |
| **Quick run command** | `pytest tests/unit/test_phase37_planning_validation.py -q` |
| **Full suite command** | `pytest tests/ -q` |
| **Estimated runtime** | &lt; 5 s |

## Sampling rate

- After edits to **`docs/DEPENDENCIES.md`**, **`README.md`**, or **`docs/CURSOR.md`**: run **`pytest tests/unit/test_phase37_planning_validation.py -q`**
- Before milestone sign-off: full **`pytest tests/ -q`**

## Per-task verification map

| Task | Plan | Wave | Requirement | Test type | Command / check |
|------|------|------|-------------|-----------|-----------------|
| 37-01-01 | 01 | 1 | TMPL-01 | unit | `test_phase37_dependencies_doc_exists_and_canonical_story` |
| 37-01-02 | 01 | 1 | TMPL-01 | unit | `test_phase37_readme_links_dependencies_doc` |
| 37-01-03 | 01 | 1 | TMPL-01 | unit | `test_phase37_cursor_links_dependencies_doc` |
| TMPL-01 (notebooks) | 01 | 1 | TMPL-01 | unit | `test_phase37_notebooks_readme_crosslink_tmplt01` |
| REQUIREMENTS | 01 | 1 | TMPL-01 | unit | `test_requirements_tmpl01_complete` |
| ROADMAP row | 01 | 1 | TMPL-01 | unit | `test_roadmap_v15_phase37_complete_row` |

## Wave 0

- **Existing infrastructure** covers phase scope; Nyquist tests added in **`test_phase37_planning_validation.py`** (no stub-only Wave 0).

## Manual-only verifications

| Behavior | Why manual |
|----------|------------|
| Reader clarity of **`docs/DEPENDENCIES.md`** prose | Subjective quality — not asserted in unit tests |

## Validation sign-off

- [x] `pytest tests/unit/test_phase37_planning_validation.py -q` green
- [x] `nyquist_compliant: true` in frontmatter
- [x] Phase **`37-VERIFICATION.md`** documents shell parity with these checks

**Approval:** approved 2026-03-27 — `$gsd:validate-phase 37` (retroactive validation strategy + tests)
