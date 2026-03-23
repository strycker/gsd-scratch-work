# Phase 25 — Research (CLOSURE-03 / plan 04 reconciliation)

## Repo vs plan-04 naming

| Plan-04 reference | Current repo |
|-------------------|--------------|
| `src/market_regime/...` | **`src/trading_crab_lib/...`** (same roles: `prediction/`, `prediction/classifier.py`, `runtime.py`) |
| `tests/test_models_reporting.py` | Exists; includes `test_model_metrics_artifacts_schema_and_behavior_coverage` |

## Quick must_have signals (pre-plan audit)

- **Leakage gating:** `trading_crab_lib/prediction/feature_gating.py` — `select_step5_feature_path`; `--allow-noncausal-features` on `run_pipeline.py` and `pipelines/05_predict.py`; `RunConfig.allow_noncausal_features` in `runtime.py`.
- **Behavior horizons:** `config/settings.yaml` — `prediction.behavior_horizons_quarters`.
- **Behavior models + metrics:** `train_forward_behavior_models`, `behavior_models.pkl`, `write_model_metrics_artifacts` → `outputs/reports/model_metrics/` in `run_pipeline.py` and `pipelines/05_predict.py`.

## Gaps to resolve in execution

1. **I001:** `03-supervised-regime-behavior-models-04-PLAN.md` has no matching `*-04-SUMMARY.md` — add **`03-supervised-regime-behavior-models-04-SUMMARY.md`**.
2. **VERIFICATION.md** frontmatter says `status: complete` but body still contains **`Status:** human_needed** under Goal Achievement — align for auditor clarity.
3. **Key link table** (end of VERIFICATION) may still say behavior metrics "not yet under test" — verify against `test_models_reporting.py` and update row if stale.

## Validation Architecture

- **Type:** Evidence matrix (grep + file read) + pytest spot-check.
- **Primary:** `pytest tests/test_models_regime.py tests/test_models_behavior.py tests/test_models_reporting.py -q`
- **Health:** `node .codex/get-shit-done/bin/gsd-tools.cjs validate health` — expect I001 cleared for plan-04 path after SUMMARY exists.

## RESEARCH COMPLETE
