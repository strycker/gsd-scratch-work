---
phase: 16
slug: v1-gap-e2e-integration-runbook
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-20
---

# Phase 16 — Validation strategy (doc-only)

## Gates

| Check | Command / rule |
|-------|----------------|
| RUNBOOK H2 count | `grep -c '^## ' RUNBOOK.md` ≥ 9 |
| Audit index present | `grep -n 'integration index' RUNBOOK.md` matches |
| ARCHITECTURE pointer | `grep -n 'RUNBOOK.md' ARCHITECTURE.md \| head -1` non-empty |
| Line budget | `wc -l RUNBOOK.md` ≤ 350 (soft; planner may waive in SUMMARY if justified) |

No pytest required for Phase 16 unless a doc-validation test is added later.
