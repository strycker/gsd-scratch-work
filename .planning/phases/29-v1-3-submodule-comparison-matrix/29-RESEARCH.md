# Phase 29 — Technical research

**Phase:** 29 — Submodule comparison matrix (**SYNC-10**)  
**Researched:** 2026-03-25

## Question

What signal does **Phase 30** need from **SYNC-10** beyond raw file counts?

## Findings

1. **Dimension coverage:** Package layout, public API surface, config/data path assumptions, test inventory, notable **features by area** (ingestion, transforms, prediction, reporting/diagnostics), planning/docs presence — per **FEATURES.md** matrix.
2. **Ordering:** Stakeholder merge order + risk notes (e.g. shared `trading_crab_lib` naming vs divergent package names in older mirrors).
3. **Operational guard:** Restate “read-only mirrors” in the artifact header so **execute-phase** agents do not patch submodules.

## Validation Architecture

Phase 29 is **documentation-only**. Automated verification: targeted **`grep`** / **`test -f`** on the artifact path; **`pytest`** optional (no product code change required). Manual: maintainer skim for five column families (root + three mirrors + notes) and merge-order section.

Sampling: single deliverable — verify once after file is written.

## RESEARCH COMPLETE
