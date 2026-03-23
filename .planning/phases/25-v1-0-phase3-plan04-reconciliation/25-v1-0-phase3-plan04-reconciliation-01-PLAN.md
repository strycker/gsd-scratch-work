---
phase: 25-v1-0-phase3-plan04-reconciliation
plan: 01
type: execute
wave: 1
depends_on:
  - 24-v1-0-brownfield-phase-readmes
files_modified:
  - .planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-04-SUMMARY.md
  - .planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-VERIFICATION.md
  - .planning/REQUIREMENTS.md
  - .planning/ROADMAP.md
  - .planning/phases/25-v1-0-phase3-plan04-reconciliation/README.md
  - .planning/phases/25-v1-0-phase3-plan04-reconciliation/25-SUMMARY.md
  - .planning/phases/25-v1-0-phase3-plan04-reconciliation/25-VALIDATION.md
autonomous: true
requirements:
  - CLOSURE-03
user_setup:
  - None
must_haves:
  truths:
    - "03-supervised-regime-behavior-models-04-SUMMARY.md exists with must_have matrix and trading_crab_lib evidence paths."
    - "REQUIREMENTS.md marks CLOSURE-03 complete; ROADMAP Phase 25 complete."
    - "validate health no longer lists I001 for 03-...-04-PLAN.md missing SUMMARY."
  artifacts:
    - path: ".planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-04-SUMMARY.md"
      provides: "plan–summary basename parity for CLOSURE-03"
---

<objective>
Close **CLOSURE-03**: reconcile **`03-supervised-regime-behavior-models-04-PLAN.md`** `must_haves` against the **current** repo (`trading_crab_lib`, `pipelines/05_predict.py`, `run_pipeline.py`, `config/settings.yaml`, `outputs/reports/model_metrics/*`, `tests/test_models_*.py`). Produce **`03-supervised-regime-behavior-models-04-SUMMARY.md`**. Align **VERIFICATION** status lines / stale table rows with automated evidence. Update **REQUIREMENTS** + **ROADMAP**. No product refactor unless a gap is found during audit — default expectation is **documentation closure** because step 5 wiring already matches plan intent under `trading_crab_lib`.
</objective>

**Non-goals:** Re-implementing Phase 3 from scratch; editing `legacy/*`.

<execution_context>
@.planning/phases/25-v1-0-phase3-plan04-reconciliation/25-CONTEXT.md
@.planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-04-PLAN.md
@.planning/REQUIREMENTS.md
</execution_context>

## Tasks

<task type="auto" tdd="false">
  <name>Task 1 — Audit plan-04 must_haves (grep + read)</name>
  <read_first>
    - `.planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-04-PLAN.md` (must_haves block)
    - `src/trading_crab_lib/prediction/feature_gating.py`
    - `src/trading_crab_lib/runtime.py`
    - `pipelines/05_predict.py` (first 180 lines)
    - `run_pipeline.py` (step5_predict region: feature load, behavior train, metrics write)
    - `config/settings.yaml` (prediction section)
    - `src/trading_crab_lib/prediction/model_metrics_artifacts.py` (function signatures)
  </read_first>
  <action>
    Record for each **truth** in plan-04 frontmatter: **SATISFIED** or **GAP** with one file path + one-line rationale.

    Minimum grep/read checks (executor must run and cite results in 04-SUMMARY):

    1. `grep -n "behavior_horizons_quarters" config/settings.yaml` — non-empty.
    2. `grep -n "allow_noncausal_features\|allow-noncausal-features" run_pipeline.py pipelines/05_predict.py src/trading_crab_lib/runtime.py` — shows CLI + RunConfig + gating.
    3. `grep -n "behavior_models.pkl" run_pipeline.py pipelines/05_predict.py` — both entrypoints persist.
    4. `grep -n "model_metrics" run_pipeline.py pipelines/05_predict.py` — `write_model_metrics_artifacts` called.
    5. `wc -l src/trading_crab_lib/prediction/model_metrics_artifacts.py` — line count ≥ 80 (substantive module).

    If any check fails: note **GAP** and either (a) minimal code fix in scope of CLOSURE-03, or (b) **waiver** paragraph in 04-SUMMARY + VERIFICATION — per REQUIREMENTS.
  </action>
  <acceptance_criteria>
    - A markdown table exists in working tree after Task 2 (or same commit wave) with one row per plan-04 `must_haves.truths` string and a **Status** column.
    - `pytest tests/test_models_regime.py tests/test_models_behavior.py tests/test_models_reporting.py -q` exits 0 before merge.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 2 — Write 03-supervised-regime-behavior-models-04-SUMMARY.md</name>
  <read_first>
    - `.planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-03-SUMMARY.md` (tone/format)
    - `.planning/phases/24-v1-0-brownfield-phase-readmes/24-SUMMARY.md` (closure style)
  </read_first>
  <action>
    Create **`.planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-04-SUMMARY.md`** with YAML frontmatter (`phase`, `plan: 04`, `completed: YYYY-MM-DD`).

    Body must include:

    1. **Note:** Plan-04 lists `src/market_regime/` paths; implementation lives under **`src/trading_crab_lib/`** — equivalence table (plan path → actual path) in a short table.
    2. **Must-have matrix** — copy each truth from plan-04; status **Satisfied** / **Waived**; evidence column with repo-relative paths (minimum: `feature_gating.py`, `05_predict.py`, `run_pipeline.py`, `model_metrics_artifacts.py`, `tests/test_models_regime.py`, `tests/test_models_reporting.py` as applicable).
    3. **Artifacts** — confirm presence of writers for `outputs/reports/model_metrics/` (documented in code; runtime creation on step 5). List expected filenames: `cv_summary.parquet`, `per_fold.jsonl`, `confusion_matrices.parquet`, `calibration.parquet` per `model_metrics_artifacts.py`.
    4. **Closure statement:** one paragraph that CLOSURE-03 evidence is complete **or** waivers are documented.

    Do not duplicate the full plan-04 task XML — summary only.
  </action>
  <acceptance_criteria>
    - `test -f .planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-04-SUMMARY.md` exits 0.
    - `grep -F "trading_crab_lib" .planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-04-SUMMARY.md` exits 0.
    - `grep -F "must_have" .planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-04-SUMMARY.md` OR a table with **Satisfied** / **Waived** appears (case-insensitive grep for `Satisfied` accepted).
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 3 — VERIFICATION.md consistency pass</name>
  <read_first>
    - `.planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-VERIFICATION.md`
  </read_first>
  <action>
    Update **`.planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-VERIFICATION.md`**:

    1. Line ~43: Change `**Status:** human_needed` to **`**Status:** complete`** (or `passed`) so it matches frontmatter `status: complete` and the Observable Truths table. Add one sentence: optional human checks remain in **Human Verification Required** for judgment, not blocking GSD closure.

    2. Key link table row for `tests/test_models_reporting.py`: Replace the Details cell ending with *"behavior metrics flattener ... is not yet under test"* with text that **`test_model_metrics_artifacts_schema_and_behavior_coverage`** (in `tests/test_models_reporting.py`) covers behavior metrics artifact schema — verbatim test function name.

    3. Optional: add a single bullet under **Changelog** or end matter: **CLOSURE-03** Phase 25 reconciled plan-04; pointer to **`03-supervised-regime-behavior-models-04-SUMMARY.md`**.

    Do not remove the **Human Verification Required** section.
  </action>
  <acceptance_criteria>
    - `grep -F "human_needed" .planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-VERIFICATION.md` returns **no** matches (status line fixed).
    - `grep -F "test_model_metrics_artifacts_schema_and_behavior_coverage" .planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-VERIFICATION.md` exits 0.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 4 — REQUIREMENTS, ROADMAP, phase 25 README, 25-SUMMARY, 25-VALIDATION</name>
  <read_first>
    - `.planning/REQUIREMENTS.md`
    - `.planning/ROADMAP.md`
    - `.planning/phases/25-v1-0-phase3-plan04-reconciliation/README.md`
  </read_first>
  <action>
    1. **REQUIREMENTS.md:** `[x]` **CLOSURE-03**; add completion pointer to `03-supervised-regime-behavior-models-04-SUMMARY.md`; traceability row **CLOSURE-03 | Phase 25 | Done**.

    2. **ROADMAP.md:** Check Phase 25 in the phases list `[x]`; progress table: phase 25 row **1/1 | Complete | CLOSURE-03**.

    3. **README.md** (phase 25 folder): links to `25-CONTEXT.md`, `25-RESEARCH.md`, `25-VALIDATION.md`, `25-v1-0-phase3-plan04-reconciliation-01-PLAN.md`, `25-SUMMARY.md`.

    4. **25-SUMMARY.md:** execution date, `pytest` command run, `validate health` command, link to 04-SUMMARY.

    5. **25-VALIDATION.md:** frontmatter `status: validated`, `nyquist_compliant: true`, sign-off date; task table all ✅.
  </action>
  <acceptance_criteria>
    - `grep -E '\[x\].*CLOSURE-03|CLOSURE-03.*Done' .planning/REQUIREMENTS.md` returns at least one match.
    - `grep '| 25 |' .planning/ROADMAP.md | grep -i Complete` exits 0.
    - `test -f .planning/phases/25-v1-0-phase3-plan04-reconciliation/25-SUMMARY.md` exits 0.
    - `node .codex/get-shit-done/bin/gsd-tools.cjs validate health` outputs JSON with `"status": "healthy"` and **no** I001 line containing `03-supervised-regime-behavior-models-04-PLAN.md has no SUMMARY` (pipe through `grep` to confirm absence of that substring).
  </acceptance_criteria>
</task>

## Verification checklist (pre-merge)

- [ ] `03-supervised-regime-behavior-models-04-SUMMARY.md` present
- [ ] Targeted pytest green
- [ ] `validate health` — I001 cleared for plan-04
- [ ] CLOSURE-03 complete in REQUIREMENTS

## Plan metadata

| Field | Value |
|-------|-------|
| Roadmap | Phase 25 — Phase 3 plan 04 reconciliation |
| Nyquist | See `25-VALIDATION.md` |
