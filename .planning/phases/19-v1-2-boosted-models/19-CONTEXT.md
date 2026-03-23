# Phase 19 — Context (v1.2 boosted models & interpretability)

**Gathered:** 2026-03-21  
**Status:** Ready for execution (plan **01**)  
**Requirements:** **MODEL-10**, **MODEL-11**

## Phase boundary

**Deliver:** Productionize **gradient-boosted** regime classifiers (alongside existing RF/DT) with **config-driven hyperparameters**, **persisted artifacts** and **metrics parity**, plus **human-readable interpretability trees** derived from a **boosted** model family where **`use_boosted`** is enabled — without changing the **primary** live prediction path (remains **RandomForest** unless explicitly documented otherwise).

## Brownfield inventory

| Area | State |
|------|--------|
| **Sklearn GB** | `GradientBoostingClassifier` trained when `prediction.use_boosted: true`; CV via `TimeSeriesSplit`; rows in `cv_summary.parquet` use `model` = `gb`. |
| **Config** | `settings.yaml` has `boosted_max_depth`, `boosted_learning_rate`, `boosted_n_estimators` but **`make_gb()` in `classifier.py` ignores them** (hardcoded `max_depth=6`, etc.). |
| **Pickle** | `run_pipeline` step 5 saves `current_regime.pkl` (RF only), `decision_tree.pkl`, `forward_classifiers.pkl` (nested dict may include `gb`). **`current_regime_gb.pkl` not written.** |
| **`pipelines/05_predict.py`** | Does not save GB pickle; does not run interpret tree or `write_model_metrics_artifacts` parity with full `run_pipeline` step 5 in all branches — **align in this phase** where cheap. |
| **Interpret tree** | `train_interpretability_tree` + `current_regime_tree.txt` uses **RF** importances only. **No GB-based interpret tree artifact.** |
| **Tests** | `tests/test_models_boosting.py`, `tests/test_models_interpret_tree.py` exist. |

## Locked decisions (Plan 01)

1. **Primary predictor** stays **`RandomForest`** for `latest_regime` / checkpoints / dashboard unless a future phase explicitly switches defaults.
2. **`boosted_*` YAML keys** drive sklearn `GradientBoostingClassifier` only in Phase 19 execution; **optional LightGBM/XGBoost** behind extras is a **stretch task** (not required to close MODEL-10 if sklearn path is complete and documented).
3. **MODEL-11:** When `use_boosted` and `gb` model exists, write **`outputs/reports/current_regime_tree_gb.txt`** (shallow tree on top‑K features from **GB** importances), controlled by **`prediction.interpret_tree_on_boosted: true`** (default **true** when boosted trained).
4. **Metrics:** No new parquet schema — extend existing `write_model_metrics_artifacts` consumers only if a new model family string appears (already supports any key in `cv_scores`).

## Canonical references

- `.planning/ROADMAP.md` — Phase 19  
- `.planning/REQUIREMENTS.md` — MODEL-10, MODEL-11  
- `src/trading_crab_lib/prediction/classifier.py`  
- `run_pipeline.py` — `step5_predict`  
- `pipelines/05_predict.py`  
- `config/settings.yaml` — `prediction.*`

## Deferred

- Replacing RF as production model; per-asset behavior-model boosting (separate scope).  
- HPO / Optuna for boosted hyperparameters.
