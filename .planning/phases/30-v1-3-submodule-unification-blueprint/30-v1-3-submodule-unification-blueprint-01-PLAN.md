---
phase: 30-v1-3-submodule-unification-blueprint
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - .planning/research/SUBMODULE_UNIFICATION_BLUEPRINT.md
  - .planning/phases/30-v1-3-submodule-unification-blueprint/30-SUMMARY.md
  - .planning/phases/30-v1-3-submodule-unification-blueprint/30-v1-3-submodule-unification-blueprint-01-SUMMARY.md
  - .planning/phases/30-v1-3-submodule-unification-blueprint/30-VALIDATION.md
  - .planning/REQUIREMENTS.md
  - .planning/ROADMAP.md
  - .planning/STATE.md
autonomous: true
requirements:
  - SYNC-11
user_setup:
  - Optional — `git submodule update --init --recursive` before reading mirrors (read-only thereafter).
must_haves:
  truths:
    - "`.planning/research/SUBMODULE_UNIFICATION_BLUEPRINT.md` exists and is cited from `30-SUMMARY.md`."
    - "Blueprint lists ordered batches; each batch includes **Objective**, **Source**, **Risk**, **Depends on**, **Owner-confirm gate** (use those exact bold labels per batch)."
    - "Blueprint includes ## Winner-selection rule and ## Exclusions matching ROADMAP Phase 30 criteria (read-only mirrors; no submodule remote push in v1.3)."
    - "`REQUIREMENTS.md` SYNC-11 marked complete after execute with pointer to `30-SUMMARY.md`."
  artifacts:
    - path: ".planning/research/SUBMODULE_UNIFICATION_BLUEPRINT.md"
      provides: "executable ordered batches + gates for post–Phase 30 implementation"
---

<objective>
Deliver **SYNC-11**: **`.planning/research/SUBMODULE_UNIFICATION_BLUEPRINT.md`** — an ordered, **owner-gated** unification program derived from **`.planning/research/SUBMODULE_COMPARISON_MATRIX.md`** and **`.planning/research/FEATURES.md`**, without editing code inside **`legacy/`** or **`*_repo-copy/`** in this phase.
</objective>

**Non-goals:** Porting code, changing `src/trading_crab_lib/`, opening PRs to submodule remotes.

<execution_context>
@.planning/phases/30-v1-3-submodule-unification-blueprint/30-CONTEXT.md
@.planning/phases/30-v1-3-submodule-unification-blueprint/30-RESEARCH.md
@.planning/research/SUBMODULE_COMPARISON_MATRIX.md
@.planning/research/FEATURES.md
@.planning/REQUIREMENTS.md
@.planning/ROADMAP.md
</execution_context>

<tasks>

<task type="auto" tdd="false">
  <name>30-01-01 — Write SUBMODULE_UNIFICATION_BLUEPRINT.md</name>
  <read_first>
    - `.planning/phases/30-v1-3-submodule-unification-blueprint/30-CONTEXT.md`
    - `.planning/research/SUBMODULE_COMPARISON_MATRIX.md`
    - `.planning/research/FEATURES.md` (§ Unification order, Merge policy, Superset definition)
    - `.planning/ROADMAP.md` (Phase 30 success criteria)
  </read_first>
  <action>
    Create **`.planning/research/SUBMODULE_UNIFICATION_BLUEPRINT.md`** with this **exact** top-level structure:

    1. `# Submodule unification blueprint (v1.3 — SYNC-11)`  
    2. `## References` — bullet links to **`SUBMODULE_COMPARISON_MATRIX.md`** and **`FEATURES.md`** (relative paths from repo root: `.planning/research/...`).  
    3. `## Winner-selection rule` — paragraph that **verbatim** includes the sentence: **`more complete / better-tested`** and states **human or owner confirmation** is required before implementation phases pick a winning implementation.  
    4. `## Exclusions` — bullet list that **explicitly** includes all of: **`legacy/`** read-only; **`*_repo-copy/`** read-only for v1.3; **no push to submodule remotes** in v1.3 (post-milestone); implementation work is **after** this blueprint.  
    5. `## Ordered batches` — **five** subsections in **this order**, each titled `### Batch 1: LIB — Test and fixture parity` through `### Batch 5: CRAB — Notebook and artifact reference` (use those exact `###` titles):

    - **Batch 1:** **Objective** — align `tests/` coverage with **`trading-crab-lib-repo-copy`** where root is missing cases. **Source** — `trading-crab-lib-repo-copy` vs canonical root `tests/`. **Risk** — low–medium (test-only). **Depends on** — `none`. **Owner-confirm gate** — owner approves **scope** of tests to port (file list or directory glob) before any future port PR.

    - **Batch 2:** **Objective** — reconcile **`src/trading_crab_lib/`** module families (ingestion, features, clustering/regime, prediction, assets, reporting/diagnostics) using LIB mirror first. **Source** — primarily **`trading-crab-lib-repo-copy`** vs root. **Risk** — high (API + behavior). **Depends on** — **Batch 1** complete (or explicitly waived in writing by owner). **Owner-confirm gate** — per **module family**, owner confirms **winner** (root vs mirror) before merge-type edits.

    - **Batch 3:** **Objective** — align **`config/`**, **`pipelines/`**, **`run_pipeline.py`** with LIB mirror where configs or step wiring differ. **Source** — **`trading-crab-lib-repo-copy`** vs root. **Risk** — medium (CLI and checkpoint names). **Depends on** — **Batch 2** for API surface stability. **Owner-confirm gate** — owner approves **breaking CLI/config** changes vs backward-compatible shims.

    - **Batch 4:** **Objective** — decide **port vs defer** for claude-only modules **`hmm.py`**, **`markov.py`**, **`divergence.py`**, **`momentum.py`** under **`src/trading_crab_lib/`** (per matrix deltas). **Source** — **`claude-scratch-work-repo-copy`**. **Risk** — high (experimental dependencies). **Depends on** — **Batch 2** (and ideally **Batch 3**). **Owner-confirm gate** — **explicit defer** allowed; if porting, owner signs off on **deps + test plan** first.

    - **Batch 5:** **Objective** — mine **`trading-crab-repo-copy`** for **notebooks / docs / historical pipeline steps** only (no primary `src/` port until mirror layout changes). **Source** — **`trading-crab-repo-copy`**. **Risk** — low for code; medium for doc drift. **Depends on** — **Batch 2** recommended so narrative matches current root behavior. **Owner-confirm gate** — owner approves which artifacts to **link, import, or ignore**.

    Within **each** batch body, include the five labeled lines **exactly** as markdown bold labels: **`Objective:`**, **`Source:`**, **`Risk:`**, **`Depends on:`**, **`Owner-confirm gate:`** (each on its own bullet or line immediately under the batch heading).

    6. `## Follow-on phases` — 2–4 bullets pointing to **Phase 31** (**PKG-10** path API) and **Phase 33** (**PRUNE-10**) as consumers of a stable root after batches execute.

    Do **not** modify files under `trading-crab-lib-repo-copy/`, `claude-scratch-work-repo-copy/`, or `trading-crab-repo-copy/`.
  </action>
  <acceptance_criteria>
    - `test -f .planning/research/SUBMODULE_UNIFICATION_BLUEPRINT.md` exits 0
    - `grep -q 'Submodule unification blueprint (v1.3 — SYNC-11)' .planning/research/SUBMODULE_UNIFICATION_BLUEPRINT.md` exits 0
    - `grep -q 'more complete / better-tested' .planning/research/SUBMODULE_UNIFICATION_BLUEPRINT.md` exits 0
    - `grep -q 'Winner-selection rule' .planning/research/SUBMODULE_UNIFICATION_BLUEPRINT.md` exits 0
    - `grep -q 'Exclusions' .planning/research/SUBMODULE_UNIFICATION_BLUEPRINT.md` exits 0
    - `grep -q '### Batch 1: LIB — Test and fixture parity' .planning/research/SUBMODULE_UNIFICATION_BLUEPRINT.md` exits 0
    - `grep -q '### Batch 5: CRAB — Notebook and artifact reference' .planning/research/SUBMODULE_UNIFICATION_BLUEPRINT.md` exits 0
    - `grep -q 'Owner-confirm gate:' .planning/research/SUBMODULE_UNIFICATION_BLUEPRINT.md` exits 0
    - `grep -qi 'no push' .planning/research/SUBMODULE_UNIFICATION_BLUEPRINT.md` exits 0
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>30-01-02 — SUMMARY, REQUIREMENTS, ROADMAP, STATE, VALIDATION, hybrid 01-SUMMARY</name>
  <read_first>
    - `.planning/REQUIREMENTS.md` (SYNC-11 row)
    - `.planning/ROADMAP.md` (Phase 30 checklist)
    - `.planning/STATE.md`
    - `.planning/research/SUBMODULE_UNIFICATION_BLUEPRINT.md`
    - `.planning/phases/29-v1-3-submodule-comparison-matrix/29-SUMMARY.md` (format reference)
  </read_first>
  <action>
    1. Write **`.planning/phases/30-v1-3-submodule-unification-blueprint/30-SUMMARY.md`**: execution date **`2026-03-25`** or actual date, **primary artifact** path **`.planning/research/SUBMODULE_UNIFICATION_BLUEPRINT.md`**, one-line pointer to **Phase 29** matrix, verification command block with `test -f` and `node .codex/get-shit-done/bin/gsd-tools.cjs validate health`.
    2. Update **`.planning/REQUIREMENTS.md`**: set **SYNC-11** checklist line from `- [ ]` to `- [x]`; add **Evidence:** line citing **`SUBMODULE_UNIFICATION_BLUEPRINT.md`** and **`30-SUMMARY.md`**; traceability table row **SYNC-11 | 30 | Complete**.
    3. Update **`.planning/ROADMAP.md`**: Phase **30** bullet from `- [ ]` to `- [x]`; in v1.3 milestone line, extend “shipped” set to include **30** (e.g. **28–30** shipped).
    4. Update **`.planning/STATE.md`**: **Phase 30** complete narrative; **next action** **`$gsd-plan-phase 31`** or **`$gsd-execute-phase 31`**; increment **`completed_phases`** under **`progress`** by 1 (use **`3`** completed if **28–30** done and **`total_phases`** remains **7**).
    5. Update **`.planning/phases/30-v1-3-submodule-unification-blueprint/30-VALIDATION.md`**: **`status: approved`**, **`nyquist_compliant: true`**, **`approved: 2026-03-25`**, sign-off checkboxes `[x]` where applicable.
    6. Replace **`.planning/phases/30-v1-3-submodule-unification-blueprint/30-v1-3-submodule-unification-blueprint-01-SUMMARY.md`** with hybrid sections: **As-built**, **Plan fidelity**, **Delta from plan**, **Verification** (mirror **29** hybrid style).
  </action>
  <acceptance_criteria>
    - `test -f .planning/phases/30-v1-3-submodule-unification-blueprint/30-SUMMARY.md` exits 0
    - `grep -q 'SUBMODULE_UNIFICATION_BLUEPRINT.md' .planning/phases/30-v1-3-submodule-unification-blueprint/30-SUMMARY.md` exits 0
    - `grep -q 'SYNC-11 | 30 | Complete' .planning/REQUIREMENTS.md` exits 0
    - `grep -q '\[x\].*SYNC-11' .planning/REQUIREMENTS.md` exits 0
    - `grep -q '\[x\].*Phase 30:' .planning/ROADMAP.md` exits 0
    - `grep -q 'nyquist_compliant: true' .planning/phases/30-v1-3-submodule-unification-blueprint/30-VALIDATION.md` exits 0
    - `grep -q '## As-built' .planning/phases/30-v1-3-submodule-unification-blueprint/30-v1-3-submodule-unification-blueprint-01-SUMMARY.md` exits 0
    - `node .codex/get-shit-done/bin/gsd-tools.cjs validate health` prints `"status": "healthy"` with empty `errors`
  </acceptance_criteria>
</task>

</tasks>

<verification_criteria>

1. **SYNC-11** closed in **REQUIREMENTS.md** with evidence paths.
2. **`validate health`** — no **I001** for **`30-v1-3-submodule-unification-blueprint-01-PLAN.md`** (hybrid **01-SUMMARY** present).

</verification_criteria>
