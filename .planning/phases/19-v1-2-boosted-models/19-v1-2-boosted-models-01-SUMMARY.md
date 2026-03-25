# Plan 01 — Hybrid summary (Phase 19, MODEL-10 / MODEL-11)

**Plan:** `19-v1-2-boosted-models-01-PLAN.md`  
**Phase narrative:** `19-SUMMARY.md`

## As-built

- `make_gradient_boosting_classifier(cfg)` in `src/trading_crab_lib/prediction/classifier.py` reads `prediction.boosted_*` and `interpret_tree_on_boosted` from `config/settings.yaml`.
- GB artifacts: `outputs/models/current_regime_gb.pkl`, `outputs/reports/current_regime_tree_gb.txt` when enabled; `run_pipeline.py` step 5 and `pipelines/05_predict.py` aligned (predict standalone fixed to pass `cfg` into trainers per `19-SUMMARY.md`).
- Tests: `tests/test_models_boosting.py`, `tests/test_models_interpret_tree.py`; RF remains default production path.

## Plan fidelity

- **MODEL-10:** sklearn `GradientBoostingClassifier` wired from YAML, persisted alongside RF/DT, TS-CV discipline unchanged, metrics parity for forward horizons when boosted enabled.
- **MODEL-11:** shallow interpret tree on GB top-K features when configured.
- Non-goals: default switch to GB, LightGBM as required ship (optional extras deferred).

## Delta from plan

- **Complete:** Config-driven GB, pickles, interpret tree file, RUNBOOK + REQUIREMENTS MODEL-10/11.
- **Deferred:** Plan Task 5 **LightGBM / XGBoost** optional libraries — explicitly deferred in `19-SUMMARY.md`; sklearn GB satisfies MODEL-10 for v1.2.
