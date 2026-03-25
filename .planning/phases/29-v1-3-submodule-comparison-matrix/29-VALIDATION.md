---
phase: 29
slug: v1-3-submodule-comparison-matrix
status: approved
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-25
approved: 2026-03-25
---

# Phase 29 — Validation Strategy

## Test infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (optional); primary = file + `grep` |
| **Quick run command** | `test -f .planning/research/SUBMODULE_COMPARISON_MATRIX.md` |
| **Full suite command** | `pytest tests/ -q` (optional — expect green, no code change) |

## Sampling rate

- After **`SUBMODULE_COMPARISON_MATRIX.md`** is written: run **`grep`** checks from plan **acceptance_criteria** once.

## Per-task verification map

| Task | Plan | Requirement | Automated check |
|------|------|-------------|-----------------|
| 29-01 | 01 | SYNC-10 | Artifact exists + required headings / substrings |

## Wave 0

- No new Wave 0 test stubs; phase is planning docs only.

## Manual-only verifications

| Behavior | Why manual |
|----------|------------|
| Matrix accuracy vs live trees | Spot-check after submodule refresh |

## Validation sign-off

- [x] Artifact path matches **29-CONTEXT.md** (`.planning/research/SUBMODULE_COMPARISON_MATRIX.md`)
- [x] **nyquist_compliant: true** — matrix + phase **29-SUMMARY.md** + **01-SUMMARY.md** + REQUIREMENTS/ROADMAP/STATE updated

**Approval:** 2026-03-25 — Phase 29 execute complete
