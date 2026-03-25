# Submodule unification blueprint (v1.3 — SYNC-11)

Ordered, **owner-gated** batches to reconcile the **canonical root** with read-only mirrors. **Implementation** happens in later work; this file is the **blueprint** only. Ground truth for layout and deltas: **SUBMODULE_COMPARISON_MATRIX.md**.

## References

- `.planning/research/SUBMODULE_COMPARISON_MATRIX.md` — Phase 29 comparison (root vs `trading-crab-lib-repo-copy`, `claude-scratch-work-repo-copy`, `trading-crab-repo-copy`).
- `.planning/research/FEATURES.md` — stakeholder unification order, merge policy, superset definition.

## Winner-selection rule

When two implementations diverge for the same concern, prefer the **more complete / better-tested** implementation **regardless of which repo it lives in**. **Human or owner confirmation** is required before any later implementation phase records a winning side or performs merge-type edits that drop the other variant.

## Exclusions

- **`legacy/`** — read-only; never a merge source or target in v1.3 planning executions.
- **`*_repo-copy/`** — read-only for v1.3; refresh only via `git submodule update` (no edits, no commits in mirror working trees as part of this milestone).
- **No push to submodule remotes** in v1.3 — updating peer repos is **post-milestone** / out of scope for the v1.3 consolidation milestone.
- **Code and test changes** — **after** this blueprint; Phase 30 ships **documentation and traceability** only.

## Ordered batches

### Batch 1: LIB — Test and fixture parity

- **Objective:** Align `tests/` coverage with **`trading-crab-lib-repo-copy`** where the canonical root is missing cases or fixtures.
- **Source:** `trading-crab-lib-repo-copy` vs canonical root `tests/`.
- **Risk:** Low–medium (test-only; mechanical port risk if imports drift).
- **Depends on:** `none`.
- **Owner-confirm gate:** Owner approves **scope** of tests to port (explicit file list or directory glob) before any future port PR.

### Batch 2: LIB — Core package reconciliation

- **Objective:** Reconcile **`src/trading_crab_lib/`** module families (ingestion, features, clustering/regime, prediction, assets, reporting/diagnostics) using the LIB mirror first.
- **Source:** Primarily **`trading-crab-lib-repo-copy`** vs root `src/trading_crab_lib/`.
- **Risk:** High — API and behavior changes; checkpoint and feature parity.
- **Depends on:** **Batch 1** complete, or **explicit written waiver** from owner.
- **Owner-confirm gate:** Per **module family**, owner confirms **winner** (root vs mirror) before merge-type edits.

### Batch 3: LIB — Config, pipelines, and entrypoints

- **Objective:** Align **`config/`**, **`pipelines/`**, and **`run_pipeline.py`** with the LIB mirror where configs or step wiring differ.
- **Source:** **`trading-crab-lib-repo-copy`** vs root.
- **Risk:** Medium — CLI flags, checkpoint names, default step order.
- **Depends on:** **Batch 2** for stable public API surface.
- **Owner-confirm gate:** Owner approves **breaking CLI/config** changes vs backward-compatible shims.

### Batch 4: CLAUDE — Experimental signal modules

- **Objective:** Decide **port vs defer** for claude-only modules **`hmm.py`**, **`markov.py`**, **`divergence.py`**, **`momentum.py`** under **`src/trading_crab_lib/`** (per matrix / Phase 29 notes).
- **Source:** **`claude-scratch-work-repo-copy`**.
- **Risk:** High — experimental dependencies, incomplete test coverage, API churn.
- **Depends on:** **Batch 2** (and ideally **Batch 3**).
- **Owner-confirm gate:** **Explicit defer** is allowed; if porting, owner signs off on **dependencies + test plan** first.

### Batch 5: CRAB — Notebook and artifact reference

- **Objective:** Mine **`trading-crab-repo-copy`** for **notebooks**, **docs**, and **historical pipeline steps** only (no primary `src/` port until that mirror layout includes a package tree).
- **Source:** **`trading-crab-repo-copy`**.
- **Risk:** Low for code; medium for narrative/doc drift vs current root.
- **Depends on:** **Batch 2** recommended so documentation matches current root behavior.
- **Owner-confirm gate:** Owner approves which artifacts to **link**, **import**, or **ignore**.

## Follow-on phases

- **Phase 31 (PKG-10)** — Consumer-safe **workspace/path API** after core library surface stabilizes from batches 1–3.
- **Phase 32 (PKG-11)** — Release engineering and PyPI story once paths and packaging are settled.
- **Phase 33 (PRUNE-10)** — Root prune (notebooks, scratch, duplicate docs) **excluding** `legacy/` and `*_repo-copy/`, after merge scope is clear.
- **Phase 34 (DOCS-10)** — Library documentation pass on the unified **`src/trading_crab_lib/`** surface.
