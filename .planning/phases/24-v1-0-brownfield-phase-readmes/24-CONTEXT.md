# Phase 24: v1.0 brownfield phase READMEs — Context

**Gathered:** 2026-03-23  
**Status:** Ready for planning  
**Source:** `.planning/REQUIREMENTS.md` (CLOSURE-02), `.planning/ROADMAP.md` Phase 24

## Phase boundary

Add a **short `README.md`** in each brownfield `.planning/phases/` directory **04, 05, 06, 07, 08, 09, 10, 11** so auditors can discover shipped v1.0 work without a historical `*-PLAN.md` in-repo for those efforts. Primary evidence remains each phase’s **`*-VERIFICATION.md`** and **`NN-VALIDATION.md`**, plus repo-root **`RUNBOOK.md`** and pipeline entrypoints (`run_pipeline.py`, `pipelines/*.py`, `scripts/*` as cited in VERIFICATION).

## Locked decisions

- **Scope:** Eight directories listed in CLOSURE-02 (06 and 08 included — README is additive to CLOSURE-01 summaries).
- **Tone:** Factual pointer doc; no “not started” for product scope; acknowledge brownfield / v1.0 delivery.
- **Links:** Use **relative** paths from each phase directory to sibling `*-VERIFICATION.md` and `NN-VALIDATION.md` files (exact basenames differ per phase).
- **Out of scope:** Code changes unless a link is objectively wrong; **CLOSURE-03** / Phase 25.

## Canonical references

- `.planning/REQUIREMENTS.md` — CLOSURE-02 wording
- `.planning/phases/23-v1-0-plan-summary-parity/23-SUMMARY.md` — prior closure context
- `RUNBOOK.md` (repo root)
- `run_pipeline.py`, `CLAUDE.md`
