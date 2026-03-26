---
phase: 31
slug: v1-3-library-workspace-paths
status: approved
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-25
approved: 2026-03-25
---

# Phase 31 — Validation Strategy

## Test infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Quick run command** | `pytest tests/unit/test_library_paths.py -q` (path TBD in execute) |
| **Full suite command** | `pytest tests/ -q` |

## Sampling rate

- After **`paths` / `__init__`** edits: quick command.
- Before phase close: full **`pytest tests/`**.

## Per-task verification map

| Task | Plan | Requirement | Automated check |
|------|------|-------------|-----------------|
| 31-01-01 | 01 | PKG-10 | `pytest` env + simulated layout tests |
| 31-01-02 | 01 | PKG-10 | Same + `python -c "import trading_crab_lib as t; print(t.CONFIG_DIR)"` |
| 31-01-03 | 01 | PKG-10 | `grep TRADING_CRAB README.md`; full pytest |

## Wave 0

- **`tests/unit/test_library_paths.py`** — execute deliverable.

## Manual-only verifications

| Behavior | Why manual |
|----------|------------|
| Real `pip install` in empty venv | Environment-specific |

## Validation sign-off

- [x] Resolver module merged; **`__init__.py`** wired
- [x] **nyquist_compliant: true** — **`test_library_paths.py`** + full **`pytest tests/`**

**Approval:** 2026-03-25 — Phase 31 execute complete
