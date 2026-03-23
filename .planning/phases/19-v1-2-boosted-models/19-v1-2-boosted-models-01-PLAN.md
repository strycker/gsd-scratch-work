---
phase: 19-v1-2-boosted-models
plan: 01
type: execute
wave: 1
depends_on:
  - 18-v1-2-signal-diagnostics
files_modified:
  - config/settings.yaml
  - src/trading_crab_lib/prediction/classifier.py
  - src/trading_crab_lib/plotting.py
  - run_pipeline.py
  - pipelines/05_predict.py
  - tests/test_models_boosting.py
  - tests/test_models_interpret_tree.py
  - RUNBOOK.md
  - .planning/REQUIREMENTS.md
  - .planning/phases/19-v1-2-boosted-models/19-SUMMARY.md
autonomous: true
requirements:
  - MODEL-10
  - MODEL-11
user_setup:
  - Steps 1–4 (features + cluster labels) for full step 5 smoke; optional minimal synthetic fixtures for unit tests only
must_haves:
  truths:
    - "GradientBoostingClassifier (or optional alternate when implemented) uses prediction.boosted_* hyperparameters from settings.yaml — no hardcoded duplicates in make_gb()."
    - "When use_boosted is true and training succeeds, GB current-regime model is persisted to outputs/models/ alongside RF/DT (e.g. current_regime_gb.pkl) and metrics artifacts include gb rows."
    - "Forward horizons include gb in cv_scores when use_boosted — already true; verify metrics parquet after config wiring."
    - "At least one interpretability artifact per roadmap MODEL-11: shallow tree text file trained from boosted model top-K features when interpret_tree_on_boosted is true."
    - "TimeSeriesSplit CV discipline unchanged for all model families."
  artifacts:
    - path: "config/settings.yaml"
      provides: "interpret_tree_on_boosted; boosted_* consumed by classifier"
    - path: "src/trading_crab_lib/prediction/classifier.py"
      provides: "_make_gradient_boosting_factory(cfg) or equivalent; shared by current + forward"
    - path: "run_pipeline.py"
      provides: "step5 saves gb pickle; writes current_regime_tree_gb.txt when configured"
    - path: "pipelines/05_predict.py"
      provides: "parity with run_pipeline for gb pickle + interpret gb artifact + metrics"
---

<objective>
Close **MODEL-10** and **MODEL-11** for v1.2: wire **boosted** classifier settings to YAML, **persist** boosted regime models, ensure **metrics parity** in `outputs/reports/model_metrics/`, and add **GB-based interpretability** output (text, and optional plot) — keeping **RF** as the default production predictor.
</objective>

**Non-goals:** Switching default prediction to GB; boosting behavior (per-asset) models; full Optuna tuning.

<execution_context>
@.planning/phases/19-v1-2-boosted-models/19-CONTEXT.md
@.planning/REQUIREMENTS.md
@.planning/ROADMAP.md
@RUNBOOK.md
@config/settings.yaml
@src/trading_crab_lib/prediction/classifier.py
@run_pipeline.py
@pipelines/05_predict.py
</execution_context>

<context>
**Regression guard:** Run `pytest tests/test_models_boosting.py tests/test_models_interpret_tree.py` after each task cluster.

**Checkpoint contract:** Step 5 still reads `features_supervised.parquet` (or gated fallback); no change to causal feature discipline.
</context>

<tasks>

<task type="auto" tdd="true">
  <name>Task 1 — Config-driven GradientBoosting hyperparameters</name>
  <read_first>
    - config/settings.yaml (prediction.boosted_*)
    - src/trading_crab_lib/prediction/classifier.py (make_gb in train_current_regime, train_forward_classifiers)
  </read_first>
  <action>
    1. Build `GradientBoostingClassifier` using `boosted_max_depth`, `boosted_learning_rate`, `boosted_n_estimators` from `cfg["prediction"]` with defaults matching current behavior if keys missing.
    2. Refactor both call sites to share a single factory helper to avoid drift.
    3. Extend unit tests to assert hyperparameters flow from a minimal cfg dict.
  </action>
  <acceptance_criteria>
    - `pytest tests/test_models_boosting.py -q` passes.
  </acceptance_criteria>
</task>

<task type="auto" tdd="true">
  <name>Task 2 — Persist boosted current-regime model</name>
  <read_first>
    - run_pipeline.py (`step5_predict`)
    - pipelines/05_predict.py
  </read_first>
  <action>
    1. When `"gb"` in `current_bundle["models"]`, save `pickle.dump` to `outputs/models/current_regime_gb.pkl` (name fixed in docs).
    2. Mirror the same in `pipelines/05_predict.py` if it trains `train_current_regime`.
    3. Document in RUNBOOK under step 5 / model outputs.
  </action>
  <acceptance_criteria>
    - Test with mocked bundle or integration test that path is written when gb present (or extend existing boosting test with tmp_path monkeypatch).
  </acceptance_criteria>
</task>

<task type="auto" tdd="true">
  <name>Task 3 — Interpretability tree on boosted (MODEL-11)</name>
  <read_first>
    - src/trading_crab_lib/prediction/classifier.py (`train_interpretability_tree`)
    - run_pipeline.py (interpret tree block)
  </read_first>
  <action>
    1. Add `prediction.interpret_tree_on_boosted: true` in settings.yaml.
    2. When `use_boosted` and `gb` model exists and flag true, call `train_interpretability_tree(gb_model, X, y, cfg)` and write `outputs/reports/current_regime_tree_gb.txt`.
    3. Optionally add `plotting.plot_interpret_tree` (matplotlib) saving `05_interpret_tree_gb.png` when `run_cfg.generate_plots` — only if low effort; otherwise text-only satisfies roadmap “tree/plot/text” with existing RF plot + new text.
  </action>
  <acceptance_criteria>
    - `pytest tests/test_models_interpret_tree.py -q` extended for gb path (or new test file).
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 4 — REQUIREMENTS + RUNBOOK + SUMMARY</name>
  <read_first>
    - .planning/REQUIREMENTS.md
    - RUNBOOK.md
  </read_first>
  <action>
    1. Mark MODEL-10 / MODEL-11 complete when executed; update traceability table.
    2. RUNBOOK: list new model/report files for step 5.
    3. Write `19-SUMMARY.md` on `$gsd:execute-phase 19`.
  </action>
  <acceptance_criteria>
    - `grep MODEL-10 .planning/REQUIREMENTS.md` shows Complete.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 5 — Optional: LightGBM behind extras (stretch)</name>
  <read_first>
    - pyproject.toml optional dependencies
  </read_first>
  <action>
    1. If time permits: add optional extra `lgbm` and `prediction.boosted_library: sklearn | lightgbm` with import guard; otherwise document deferral in 19-SUMMARY.md.
  </action>
  <acceptance_criteria>
    - Either working guarded import path **or** explicit “deferred” note — no blocking gap for MODEL-10 closure on sklearn path.
  </acceptance_criteria>
</task>

</tasks>

<verification>

## Automated

- `pytest tests/test_models_boosting.py tests/test_models_interpret_tree.py -q`
- `python -c "from trading_crab_lib.config import load; load()"`

## Manual

- Full pipeline: `python run_pipeline.py --steps 5 --plots` with `use_boosted: true` and verify `outputs/models/current_regime_gb.pkl` and `outputs/reports/current_regime_tree_gb.txt`.
- Inspect `outputs/reports/model_metrics/cv_summary.parquet` for `model == gb`.

</verification>
