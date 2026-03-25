# Phase 30 — Technical research

**Phase:** 30 — Submodule unification blueprint (**SYNC-11**)  
**Researched:** 2026-03-25

## Question

What structure lets executors turn **SUBMODULE_COMPARISON_MATRIX.md** into an **ordered, gated** merge program without touching mirror working trees in this phase?

## Findings

1. **Batch granularity:** Separate **(A)** test/fixture parity, **(B)** core `src/trading_crab_lib/` module families (ingestion → features → clustering/regime → prediction → assets → reporting/diagnostics), **(C)** `config/` + `pipelines/` + `run_pipeline.py` alignment, **(D)** claude-only experimental top-level modules (**`hmm.py`**, **`markov.py`**, **`divergence.py`**, **`momentum.py`**) with **defer/port** owner gate, **(E)** `trading-crab-repo-copy` as **notebook/docs** reference only (no `src/` in current matrix).
2. **Dependencies:** Tests before wide module ports avoids porting untested deltas; LIB-order batches complete before claude experimental batch reduces API skew; notebook mining last.
3. **Risk labeling:** IO/ingestion and **public API** changes = higher risk; docs-only = lower. **Nested clone** paths under LIB mirror = cite **layout caveats** and require path-normalized diffs in downstream execute.
4. **Traceability:** Single blueprint path **`.planning/research/SUBMODULE_UNIFICATION_BLUEPRINT.md`** cited from **`30-SUMMARY.md`** satisfies ROADMAP “path cited in *-SUMMARY”.

## Validation Architecture

Phase 30 execute remains **documentation + traceability** (no production code in planned tasks). **Automated:** `test -f` on blueprint; `grep` for required section titles and substrings (**`Owner-confirm`**, **`Winner-selection`**, **`Exclusions`**); `node .codex/get-shit-done/bin/gsd-tools.cjs validate health` after **REQUIREMENTS** / **ROADMAP** / **STATE** updates. **Manual:** Maintainer confirms batch ordering matches stakeholder intent and that each batch has **Source:** and **Depends on:** fields.

Sampling: verify once after blueprint and **30-SUMMARY.md** exist.

## RESEARCH COMPLETE
