# Plan summary — `36-v1-4-root-docs-import-alignment-01-PLAN.md`

**Phase:** 36 — Root docs & import alignment (**DOC-ALIGN-10**)  
**Type:** hybrid (**I001**)

## As-built

- Root guides (**`CLAUDE.md`**, **`README.md`**, **`PITFALLS.md`**, **`ARCHITECTURE.md`**, **`STATE.md`**) describe the installable package **`trading_crab_lib`** and paths under **`src/trading_crab_lib/`**, including **`checkpoints.CheckpointManager`** at package root (no **`io.checkpoints`**).
- Phase **34** planning artifacts: **`34-VALIDATION.md`** **`nyquist_compliant: true`**; **`34-VERIFICATION.md`** updated with lint/pytest from this execute.
- **`REQUIREMENTS.md`** and roadmap mark **DOC-ALIGN-10** / Phase **36** complete; **`.planning/STATE.md`** reflects **v1.4** phases **35–36** done.
- Planning regression test extended so **`milestone: v1.4`** in **`.planning/STATE.md`** satisfies the Phase 14 Nyquist hook.

## Plan fidelity

| Task | Delivered |
|------|-----------|
| 36-01-01 — CLAUDE.md | ✓ |
| 36-01-02 — README checkpoint snippet | ✓ |
| 36-01-03 — PITFALLS / ARCHITECTURE / STATE paths | ✓ |
| 36-01-04 — 34-VALIDATION / 34-VERIFICATION | ✓ |
| 36-01-05 — REQUIREMENTS, summaries, health | ✓ |

## Delta from plan

- **`test_phase14_planning_validation.py`** — Added **`milestone: v1.4`** to the acceptable **STATE.md** patterns so CI passes after **v1.4** milestone state updates (not listed in plan; required once **STATE** moved past **v1.3-only** acceptance).
