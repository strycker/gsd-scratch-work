---
phase: 38-v1-5-backlog-reconciliation
plan: "01"
subsystem: docs
tags: [roadmap, backlog, yc_, regime, TMPL-02]

requires: []
provides:
  - Root ROADMAP Tier 1.3–1.4 aligned with transforms/regime
  - CLAUDE.md Gap 6 + next priority cleanup
  - FUTURE-TODO + v1.5-CLEANUP-BACKLOG reconciliation notes
affects: [onboarding, product-backlog]

tech-stack:
  added: []
  patterns: [shipped vs backlog labeling]

key-files:
  created: []
  modified:
    - ROADMAP.md
    - CLAUDE.md
    - .planning/FUTURE-TODO.md
    - .planning/v1.5-CLEANUP-BACKLOG.md

key-decisions:
  - "Tier 1.3–1.4 marked shipped with yc_* and build_forward_window_probabilities; backlog = expansion/UX not greenfield."

patterns-established: []

requirements-completed:
  - TMPL-02

duration: 15min
completed: 2026-03-27
---

# Plan summary — `38-01-PLAN.md`

**Phase:** 38 — Backlog reconciliation (**TMPL-02**)

## As-built

- **Root `ROADMAP.md`:** §1.3 documents **`add_yield_curve_features`** / **`yc_*`**; §1.4 documents **`build_forward_window_probabilities`**, **`forward_window_probabilities.parquet`**, tests, legacy name note. **Suggested starting points** list updated (removed stale profiler / pre-shipped yield items).
- **`CLAUDE.md`:** Removed empirical forward from “missing in src”; **Gap 6** closed; **Next Priority** renumbered; **377+** tests note; confusion matrix remains **TMPL-03**.
- **`.planning/FUTURE-TODO.md`:** Forward-window bullet + confusion matrix → Phase **39** pointer.
- **`.planning/v1.5-CLEANUP-BACKLOG.md`:** TMPL-02 section + **Still outstanding** product bullets refreshed.

## Plan fidelity

| Task | Delivered |
|------|-----------|
| 38-01-01 — `ROADMAP.md` | ✓ |
| 38-01-02 — `CLAUDE.md` | ✓ |
| 38-01-03 — `FUTURE-TODO` + cleanup backlog | ✓ |

## Delta from plan

- None — documentation-only.

## Self-Check: PASSED

- `rg` checks for **`yc_*`**, **`build_forward_window_probabilities`**, **`forward_window_probabilities.parquet`** on **`ROADMAP.md`**; **`build_forward_window_probabilities`** on **`CLAUDE.md`** / **`FUTURE-TODO.md`**.
