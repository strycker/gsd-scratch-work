# Phase 19 — Execution summary (MODEL-10 / MODEL-11)

**Plan:** `19-v1-2-boosted-models-01-PLAN.md`  
**Executed:** 2026-03-22  
**Requirements:** MODEL-10, MODEL-11

## What shipped

- **`make_gradient_boosting_classifier(cfg)`** in `classifier.py` — reads `boosted_max_depth`, `boosted_learning_rate`, `boosted_n_estimators`, `random_state` from `prediction` config; used by **current-regime** and **forward** GB training.
- **`outputs/models/current_regime_gb.pkl`** — saved when `"gb"` in `current_bundle["models"]` (`run_pipeline` step 5 + `pipelines/05_predict.py`).
- **`outputs/reports/current_regime_tree_gb.txt`** — shallow interpret tree from **GB** top‑K features when `interpret_tree_on_boosted: true` (default **true**).
- **`config/settings.yaml`** — `interpret_tree_on_boosted`.
- **`pipelines/05_predict.py`** — **Bugfix:** pass **`cfg`** into `train_current_regime` and `train_forward_classifiers` (previously omitted, so `use_boosted` / boosted hyperparameters were never applied from YAML in standalone step 5).
- **`RUNBOOK.md`** — Step 5 artifact table; **`.planning/REQUIREMENTS.md`** — MODEL-10/11 **Complete**.

## Deferred (plan Task 5)

- **LightGBM / XGBoost** optional extras — not implemented; sklearn `GradientBoostingClassifier` satisfies MODEL-10 per plan. Follow-up: optional `boosted_library` + `pip install lightgbm` guard.

## Verification

- `pytest tests/test_models_boosting.py tests/test_models_interpret_tree.py -q`
- `python -c "from trading_crab_lib.config import load; load()"`

## Manual

- `python run_pipeline.py --steps 5 --plots` with fresh steps 1–4 prerequisites; confirm `current_regime_gb.pkl` and `current_regime_tree_gb.txt` when `use_boosted: true`.
