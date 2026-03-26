---
phase: 33
slug: v1-3-root-prune
status: complete
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-26
---

# Phase 33 — Validation Strategy

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Quick run** | `pytest tests/ -q` |
| **Health** | `node .codex/get-shit-done/bin/gsd-tools.cjs validate health` |

## Per-Task Verification Map

| Task | Requirement | Automated |
|------|-------------|-----------|
| Inventory table | PRUNE-10 | `test -f` inventory markdown |
| Forbidden paths | Roadmap criterion 3 | grep / script in SUMMARY |
| Link sanity | Roadmap criterion 2 | `rg` in canonical docs |

## Manual-Only

| Behavior | Why |
|----------|-----|
| “Redundant” judgment for borderline docs | Human/product call |

## Validation Sign-Off

- [ ] `nyquist_compliant: true` after execute when applicable

**Approval:** pending
