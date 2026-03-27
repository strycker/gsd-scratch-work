---
phase: 37-v1-5-fork-dependency-docs
plan: "01"
subsystem: docs
tags: [pyproject, pip, forks, onboarding]

requires: []
provides:
  - docs/DEPENDENCIES.md canonical dependency narrative for forks
  - README and CURSOR cross-links to dependency story
affects: [template-forks, onboarding]

tech-stack:
  added: []
  patterns: [single-doc deep-dive + README/CURSOR pointers]

key-files:
  created:
    - docs/DEPENDENCIES.md
  modified:
    - README.md
    - docs/CURSOR.md

key-decisions:
  - "Canonical source remains pyproject.toml; requirements*.txt documented as aligned mirrors."

patterns-established:
  - "Dependency policy: explain in docs/DEPENDENCIES.md; Installation section links once."

requirements-completed:
  - TMPL-01

duration: 5min
completed: 2026-03-26
---

# Plan summary — `37-01-PLAN.md`

**Phase:** 37 — Fork & dependency docs (**TMPL-01**)

## As-built

**`docs/DEPENDENCIES.md`** documents **`pyproject.toml`** as canonical for **`trading-crab-lib`**, explains **`requirements.txt`** / **`requirements-dev.txt`** vs **`pip install -e ".[dev]"`**, **`scripts/setup.sh`**, optional lockfiles, and a fork checklist. **`README.md`** adds **Dependency files (forks)** under Installation with a link; **`docs/CURSOR.md`** links to the same doc for IDE setup. **TMPL-01** acceptance: **`notebooks/README.md`** was already linked from root **`README.md`** (notebook imports section).

Delivered in commit **`48356fd`** during plan-phase; this execute pass adds **SUMMARY** and closes GSD state.

## Plan fidelity

| Task | Delivered |
|------|-----------|
| 37-01-01 — `docs/DEPENDENCIES.md` | ✓ |
| 37-01-02 — README link | ✓ |
| 37-01-03 — CURSOR link | ✓ |

## Delta from plan

- None — no code or dependency version changes.

## Self-Check: PASSED

- `test -f docs/DEPENDENCIES.md`; greps for `pyproject.toml`, `requirements.txt`, `pip install -e`; README + CURSOR link to `DEPENDENCIES.md`.
