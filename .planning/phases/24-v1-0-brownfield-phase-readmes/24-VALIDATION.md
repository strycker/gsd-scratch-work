---
phase: 24
slug: v1-0-brownfield-phase-readmes
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-23
---

# Phase 24 — Validation Strategy

> CLOSURE-02 — brownfield `README.md` anchors in phases **04–11**.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Type** | Documentation + shell checks |
| **Primary** | `test -f`, `grep` on each `README.md` |
| **Project health** | `node .codex/get-shit-done/bin/gsd-tools.cjs validate health` |
| **Estimated runtime** | &lt; 30 seconds |

---

## Sampling Rate

- **After each README task:** `test -f` + `grep` on that file
- **Before verify-work:** All eight paths present + REQUIREMENTS updated

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Check | Status |
|---------|------|------|-------------|-------|--------|
| 24-01-01 | 01 | 1 | CLOSURE-02 | `README.md` in 04–07 | ✅ |
| 24-01-02 | 01 | 1 | CLOSURE-02 | `README.md` in 08–11 | ✅ |
| 24-01-03 | 01 | 1 | CLOSURE-02 | REQUIREMENTS + ROADMAP rows | ✅ |

---

## Wave 0 Requirements

- Existing infrastructure covers this phase (no new test framework).

---

## Manual-Only Verifications

| Behavior | Why manual |
|----------|------------|
| Link resolution in IDE preview | Human confirms relative links open |

---

## Validation Sign-Off

- [x] All eight `README.md` files exist with required pointers
- [x] `nyquist_compliant: true` set when execution complete
- [x] CLOSURE-02 marked done in REQUIREMENTS

**Approval:** 2026-03-23
