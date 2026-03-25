# Phase 28 — Technical research

**Phase:** 28 — Hybrid PLAN/SUMMARY closure (I001)  
**Researched:** 2026-03-25

## Question

What does the executor need to produce **hybrid** summaries that satisfy tooling and humans/LLMs?

## Findings

1. **Tooling contract:** `gsd-tools validate health` I001 compares each `*-PLAN.md` to a same-basename `*-SUMMARY.md` in the same directory (`health` workflow / stats parity).
2. **Stakeholder hybrid:** Three voices per file — shipped reality, original plan intent, explicit gap list.
3. **Evidence sources:** Each phase directory often has `NN-SUMMARY.md`, `*-VERIFICATION.md`, `*-VALIDATION.md` — link or excerpt rather than duplicating entire audits.
4. **Non-goals:** Changing plan files; editing code; submodule trees.

## Validation Architecture

Phase 28 is **documentation-only**. Automated verification = **`gsd-tools validate health`** (JSON `info` array has zero I001 entries referencing the eight target `*-PLAN.md` paths). Secondary: manual spot-check that each new `*-SUMMARY.md` contains the three hybrid sections.

Sampling: after each batch of summaries, run health; full phase exit when all eight paths clear I001.

## RESEARCH COMPLETE
