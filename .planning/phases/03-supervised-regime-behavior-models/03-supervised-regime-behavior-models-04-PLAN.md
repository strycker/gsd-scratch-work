---
phase: 03-supervised-regime-behavior-models
plan: 04
type: execute
wave: 4
depends_on:
  - 03-02
  - 03-03
files_modified:
  - run_pipeline.py
  - src/market_regime/runtime.py
  - pipelines/05_predict.py
  - config/settings.yaml
  - src/market_regime/prediction/classifier.py
  - src/market_regime/prediction.py
  - tests/test_models_regime.py
  - tests/test_models_behavior.py
  - tests/test_models_reporting.py
  - .planning/ROADMAP.md
  - .planning/phases/03-supervised-regime-behavior-models/03-VALIDATION.md
  - .planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-VERIFICATION.md
autonomous: true
requirements:
  - MODEL-01
  - MODEL-02
  - MODEL-03
  - MODEL-04
user_setup: []
must_haves:
  truths:
    - "Step 5 (predict) trains ONLY on `features_supervised.parquet` by default; it may fall back to `features.parquet` ONLY when an explicit opt-in flag is provided and the warning is unmissable."
    - "Behavior (ETF/portfolio directional) models are trained as part of step 5 and persisted alongside regime models, producing downstream-consumable artifacts."
    - "Step 5 persists structured metrics artifacts: CV summary table, per-fold JSON, confusion matrices, and calibration diagnostics, with stable schemas and tests."
    - "Phase 3 planning + validation docs reflect the actual test files, Nyquist compliance, and plan progress, enabling Phase 3 verification status to advance."
  artifacts:
    - path: "pipelines/05_predict.py"
      provides: "Step-5 runner that enforces leakage guardrails, trains regime + behavior models, and writes model + metrics artifacts."
      min_lines: 120
    - path: "run_pipeline.py"
      provides: "Step-5 implementation that enforces leakage guardrails and writes the same artifacts as pipelines/05_predict.py."
      min_lines: 120
    - path: "config/settings.yaml"
      provides: "Separate config keys for regime horizons vs behavior horizons."
      contains: "prediction.behavior_horizons_quarters"
    - path: "outputs/models/behavior_models.pkl"
      provides: "Persisted behavior model bundle (asset × horizon)."
    - path: "outputs/reports/model_metrics/cv_summary.parquet"
      provides: "CV summary table for regime + behavior models."
    - path: "outputs/reports/model_metrics/per_fold.jsonl"
      provides: "Per-fold evaluation records with fold indices + report payloads."
    - path: "outputs/reports/model_metrics/confusion_matrices.parquet"
      provides: "Confusion matrices persisted in a tidy, machine-readable table."
    - path: "outputs/reports/model_metrics/calibration.parquet"
      provides: "Calibration diagnostics persisted in a tidy, machine-readable table."
    - path: "tests/test_models_reporting.py"
      provides: "Tests that validate the metrics artifact schema and behavior-metrics coverage."
      min_lines: 80
  key_links:
    - from: "pipelines/05_predict.py"
      to: "config/settings.yaml"
      via: "reads prediction.forward_horizons_quarters vs prediction.behavior_horizons_quarters"
      pattern: "behavior_horizons_quarters"
    - from: "pipelines/05_predict.py"
      to: "data/processed/features_supervised.parquet"
      via: "default gated load"
      pattern: "features_supervised\\.parquet"
    - from: "pipelines/05_predict.py"
      to: "outputs/reports/model_metrics/"
      via: "writes structured metrics artifacts"
      pattern: "model_metrics"
---

<objective>
Complete Phase 03 by hardening leakage guardrails, wiring behavior models into step 5, persisting structured metrics artifacts, and reconciling Phase 3 planning/validation/verification docs so the phase can be marked complete.

Purpose: Phase 3 must be safely usable as a “supervised modeling layer” for downstream phases, with causal-feature guarantees, behavior model wiring (not library-only), and inspectable metrics artifacts.
Output: Updated step-5 runners (both `pipelines/05_predict.py` and `run_pipeline.py` step 5), new config key for behavior horizons, persisted metrics artifacts + schemas, and tests + doc reconciliation that enables Phase 3 verification to advance.
</objective>

<execution_context>
@CLAUDE.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/REQUIREMENTS.md
@.planning/phases/03-supervised-regime-behavior-models/03-CONTEXT.md
@.planning/phases/03-supervised-regime-behavior-models/03-RESEARCH.md
@.planning/phases/03-supervised-regime-behavior-models/03-VALIDATION.md
@.planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-VERIFICATION.md
@.planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-02-SUMMARY.md
@.planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-03-SUMMARY.md
</execution_context>

<context>
Key Phase-03 realities from the current codebase snapshot:
- `pipelines/05_predict.py` already *requires* `data/processed/features_supervised.parquet` (good for leakage guardrails).
- `run_pipeline.py` Step 5 currently falls back from `features_supervised.parquet` → `features.parquet` with only a warning (must be gated behind explicit opt-in per locked decision).
- Behavior model logic exists (in `src/market_regime/prediction.py` and partially in `src/market_regime/prediction/classifier.py`), but step 5 does not train/persist behavior models yet (must be wired in now).
- Existing tests cover:
  - regime CV ordering + probability sanity (`tests/test_models_regime.py`)
  - behavior label semantics + behavior model probabilities (`tests/test_models_behavior.py`)
  - regime metrics aggregation + combined-row behavior shape (`tests/test_models_reporting.py`)

Locked decisions to honor (from `03-CONTEXT.md`):
- Step 5 must default to `features_supervised.parquet`, with fallback ONLY behind explicit opt-in and a loud warning.
- Wire behavior models into step 5 now.
- Persist structured metrics artifacts (CV summary table, per-fold JSON, confusion matrices, calibration diagnostics; optional plots ok).
- Separate config keys for horizons: regime horizons vs behavior horizons.
</context>

<tasks>

<task type="auto" tdd="true">
  <name>Task 1: Enforce leakage-guard feature gating in BOTH step-5 entrypoints</name>
  <files>run_pipeline.py, src/market_regime/runtime.py, pipelines/05_predict.py, tests/test_models_regime.py</files>
  <behavior>
    - Default: When `data/processed/features_supervised.parquet` is missing, step 5 FAILS with an error that explains how to generate it (run step 2) and how to opt in to non-causal fallback.
    - Opt-in: When an explicit CLI flag is provided (e.g. `--allow-noncausal-features`), step 5 may load `data/processed/features.parquet` instead, but MUST emit an unmissable warning (and ideally write a “NONCAUSAL_USED=true” marker into the metrics artifacts).
    - Tests must be network-free and must not rely on existing `data/` in the repo.
  </behavior>
  <action>
    Implement the locked leakage guardrails consistently across:
    - `pipelines/05_predict.py` (standalone step runner)
    - `run_pipeline.py` step 5 (`step5_predict`)

    Concrete implementation requirements:
    - Add a CLI flag named `--allow-noncausal-features` to `run_pipeline.py` and plumb it through `RunConfig` (update `src/market_regime/runtime.py` accordingly).
    - Add the same flag to `pipelines/05_predict.py` (argparse) for parity.
    - Create a small, testable helper function (shared or duplicated minimally, but must be deterministic and unit-testable) that selects the feature path:
      - Prefers/Requires `features_supervised.parquet` by default
      - Falls back to `features.parquet` only when `allow_noncausal_features=True`
      - Emits a loud warning on fallback that includes BOTH filenames.
    - Update/extend `tests/test_models_regime.py` with a unit test that:
      - Uses `tmp_path` to create a fake `data/processed/` directory tree
      - Asserts that missing `features_supervised.parquet` raises by default
      - Asserts that opt-in allows fallback to `features.parquet` (no need to run full model training; just validate the gating helper output / exception).

    Constraints:
    - Do not modify `legacy/*`.
    - No network calls in tests.
  </action>
  <verify>
    <automated>pytest -q -k "leakage or noncausal or features_supervised"</automated>
  </verify>
  <done>
    - Both step-5 entrypoints enforce `features_supervised.parquet` by default.
    - Fallback to `features.parquet` is impossible without explicit opt-in and produces a conspicuous warning.
    - Unit test(s) prove the gating behavior.
  </done>
</task>

<task type="auto" tdd="true">
  <name>Task 2: Wire behavior models into step 5 and persist models + metrics artifacts</name>
  <files>pipelines/05_predict.py, run_pipeline.py, config/settings.yaml, src/market_regime/prediction.py, src/market_regime/prediction/classifier.py, tests/test_models_behavior.py, tests/test_models_reporting.py</files>
  <behavior>
    - Step 5 trains/persists behavior models (asset × horizon) using causal features and quarterly returns (prefer cached ETF prices if available; otherwise fall back to a non-network proxy returns source already in the codebase).
    - Step 5 writes structured metrics artifacts for BOTH regime and behavior models:
      - CV summary table (tidy rows) for regime + behavior
      - Per-fold JSONL records (include fold indices + report payloads)
      - Confusion matrices table (tidy)
      - Calibration diagnostics table (tidy; include at least Brier score and calibration_curve bins)
    - Horizons are separately configurable:
      - Regime: `prediction.forward_horizons_quarters` (existing)
      - Behavior: `prediction.behavior_horizons_quarters` (new)
  </behavior>
  <action>
    1) Separate horizon config keys
    - Update `config/settings.yaml` to add `prediction.behavior_horizons_quarters` (initially mirror `[1]` or `[1, 2]`—keep conservative).
    - Update step 5 to read the correct list for behavior vs regime.

    2) Decide one canonical behavior training implementation surface (reconciliation)
    - Prefer to centralize the train/eval logic in ONE place and make step 5 call that, to avoid duplicate definitions between `prediction.py` and `prediction/classifier.py`.
    - If you keep both for backward compatibility, ensure step 5 uses only one canonical API and tests target that API.

    3) Wire behavior models into step 5 without network dependence
    - In `pipelines/05_predict.py`, after regime models:
      - Load returns data needed for behavior labels:
        - If `data/raw/asset_prices.parquet` exists, compute quarterly returns from it using existing project helpers.
        - Else, compute proxy returns from macro data using existing project helpers (no network).
      - Train behavior models via the canonical behavior helper using `behavior_horizons_quarters`.
      - Persist to `outputs/models/behavior_models.pkl`.
    - Mirror the same wiring in `run_pipeline.py` step 5 so “master runner” and “step runner” stay consistent.

    4) Persist structured metrics artifacts (MODEL-04)
    - Create a `outputs/reports/model_metrics/` directory and write:
      - `cv_summary.parquet`: tidy rows with required columns, e.g.:
        - `family` in {"regime","behavior"}
        - `model` (e.g. "rf","dt","gb","behavior-rf")
        - `horizon` (int or null)
        - `asset` (str or null)
        - `metric` (e.g. "accuracy","macro_f1","weighted_f1","brier")
        - `value` (float)
        - `n_splits` (int)
      - `per_fold.jsonl`: one JSON object per fold, including:
        - `family`, `model`, `horizon`, `asset`, `fold`, `train_indices`, `test_indices`
        - a payload for confusion matrix and/or `classification_report(output_dict=True)`
      - `confusion_matrices.parquet`: tidy confusion matrices with columns:
        - `family`, `model`, `horizon`, `asset`, `fold` (or "overall"), `true_label`, `pred_label`, `count`
      - `calibration.parquet`: tidy calibration data with columns:
        - `family`, `model`, `horizon`, `asset`, `fold` (or "overall"), `class_label`, `bin`, `predicted_prob_mean`, `observed_freq`, plus `brier` at a suitable grain
    - Optional plots: only if `--plots` / `run_cfg.generate_plots` is enabled, and save under the existing plots directory conventions.

    5) Tests
    - Add/update tests so we have automated coverage for:
      - “behavior models are wired into step 5 outputs”: at minimum, a unit-level test that calls the step-5 behavior training function (or a thin wrapper) on synthetic data and asserts the returned bundle is serializable and includes expected keys; and/or checks that the step-5 runner writes `behavior_models.pkl` and the metrics files when run against a temp directory fixture (prefer unit-level over full CLI invocation).
      - “metrics artifacts schema”: validate the written tables contain required columns and that row types are correct (no network, no reliance on real data).
    - Ensure behavior-metrics coverage closes the currently flagged WARN in `03-supervised-regime-behavior-models-VERIFICATION.md`.
  </action>
  <verify>
    <automated>pytest -q -k "models_behavior or models_reporting"</automated>
  </verify>
  <done>
    - Step 5 trains and saves behavior models (`outputs/models/behavior_models.pkl`) using `prediction.behavior_horizons_quarters`.
    - Metrics artifacts exist under `outputs/reports/model_metrics/` with stable, tested schemas.
    - Automated tests prove wiring and schema integrity without network calls.
  </done>
</task>

<task type="auto">
  <name>Task 3: Reconcile Phase 3 docs (ROADMAP + VALIDATION + VERIFICATION) so GSD is consistent</name>
  <files>.planning/ROADMAP.md, .planning/phases/03-supervised-regime-behavior-models/03-VALIDATION.md, .planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-VERIFICATION.md</files>
  <action>
    1) Update `.planning/ROADMAP.md` Phase 3 section
    - Set `**Plans:** 4 plans` and list Phase-3 plans explicitly:
      - 03-01 (incomplete / superseded by 03-04; leave as historical, unchecked)
      - 03-02 (completed)
      - 03-03 (completed)
      - 03-04 (this comprehensive closure plan)
    - Update the Phase list checkbox entry for Phase 3 to `- [x]` once 03-04 is complete.
    - Update the Phase 3 details line `**Plans**: TBD` → `**Plans**: 4 plans` (and ensure the filenames above are present).
    - Update the global Progress table row for Phase 3 so “Plans Complete” and “Status” are coherent with the presence of 03-04:
      - Plans Complete should read `4/4`
      - Status should be `Complete`
      - Completed date should be set (YYYY-MM-DD)

    2) Fix `.planning/phases/03-supervised-regime-behavior-models/03-VALIDATION.md`
    - Remove references to `tests/unit/test_classifier.py` (it does not exist).
    - Replace the Per-Task Verification Map with references to the actual tests and mark file/status truthfully:
      - `tests/test_models_regime.py` (MODEL-01/02 + CV ordering and probability checks)
      - `tests/test_models_behavior.py` (MODEL-03 + per-asset/horizon behavior models)
      - `tests/test_models_reporting.py` (MODEL-04 + metrics artifact schema, including behavior-metrics coverage)
      - Any newly added tests from Tasks 1–2 should be included and referenced by exact `pytest` commands.
    - Ensure “File Exists” is ✅ for the existing test files and no stale “pending” rows remain once files are present.
    - Ensure frontmatter accurately reflects Nyquist state AFTER Tasks 1–2:
      - `nyquist_compliant: true`
      - `wave_0_complete: true`
      - `status:` should reflect the phase’s real state (likely “complete” once this plan lands).

    3) Update Phase 3 verification report to close WARNs where possible
    - In `03-supervised-regime-behavior-models-VERIFICATION.md`, update:
      - the leakage safeguard truth from partial → verified once gating is in place
      - the behavior wiring truth from partial → verified once step 5 trains/persists behavior models + metrics
      - the reporting truth from WARN → PASS once metrics artifacts + tests exist
    - Keep the “human verification needed” section, but ensure “Phase 3 status can be advanced” once automated gaps are closed.
  </action>
  <verify>
    <automated>python -c "import pathlib; p=pathlib.Path('.planning/phases/03-supervised-regime-behavior-models/03-VALIDATION.md'); print('ok', p.exists())" && pytest -q -k "models_regime or models_behavior or models_reporting"</automated>
  </verify>
  <done>
    - ROADMAP Phase 3 plan list/counts and progress are coherent.
    - 03-VALIDATION.md references the real test files and accurately indicates Nyquist compliance.
    - Phase 3 verification report no longer flags the resolved WARNs (leakage gating, behavior wiring, behavior-metrics reporting).
  </done>
</task>

</tasks>

<verification>
- Focused test suite passes (no network):
  - `pytest -q -k "models_regime or models_behavior or models_reporting"`
- Feature gating verified by tests: missing supervised features fails by default; opt-in fallback works and warns loudly.
- Step 5 produces:
  - `outputs/models/current_regime.pkl`
  - `outputs/models/forward_classifiers.pkl`
  - `outputs/models/behavior_models.pkl`
  - `outputs/reports/model_metrics/` with the four required artifact types.
</verification>

<success_criteria>
- Locked decisions are fully implemented:
  - leakage guardrails are enforced by default with explicit opt-in fallback only
  - behavior models are wired into step 5
  - structured metrics artifacts are persisted and tested
  - separate horizon config keys exist and are used correctly
- Phase 3 documentation is consistent and Phase 3 verification can be advanced to “complete” (with only human judgment checks remaining).
</success_criteria>

<output>
After completion, create `.planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-04-SUMMARY.md`.
</output>

