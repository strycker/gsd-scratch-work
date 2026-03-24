---
phase: 03-supervised-regime-behavior-models
plan: 04
completed: 2026-03-23
---

# 03-supervised-regime-behavior-models-04 — Execution summary (CLOSURE-03)

**Plan:** [`03-supervised-regime-behavior-models-04-PLAN.md`](./03-supervised-regime-behavior-models-04-PLAN.md)  
**Requirement:** CLOSURE-03 (GSD evidence closure)

## Path naming (plan vs repo)

Plan-04 `files_modified` lists `src/market_regime/...`. The shipped implementation uses **`src/trading_crab_lib/`** (same pipeline contract).

| Plan-04 path | Actual path |
|--------------|-------------|
| `src/market_regime/runtime.py` | `src/trading_crab_lib/runtime.py` |
| `src/market_regime/prediction.py` | `src/trading_crab_lib/prediction.py` |
| `src/market_regime/prediction/classifier.py` | `src/trading_crab_lib/prediction/classifier.py` |

## Must-have truths (plan-04 frontmatter)

| # | Truth | Status | Evidence |
|---|--------|--------|----------|
| 1 | Step 5 trains only on `features_supervised.parquet` by default; fallback to `features.parquet` only with explicit opt-in and loud warning. | **Satisfied** | `select_step5_feature_path` in `src/trading_crab_lib/prediction/feature_gating.py`; `--allow-noncausal-features` on `run_pipeline.py` and `pipelines/05_predict.py`; `RunConfig.allow_noncausal_features` in `src/trading_crab_lib/runtime.py`; tests in `tests/test_models_regime.py::test_step5_feature_path_gating_prefers_supervised_by_default`. |
| 2 | Behavior models trained in step 5, persisted alongside regime models. | **Satisfied** | `train_forward_behavior_models` + `behavior_models.pkl` in `run_pipeline.py` (step 5) and `pipelines/05_predict.py`; `tests/test_models_behavior.py`. |
| 3 | Structured metrics artifacts (CV summary, per-fold JSONL, confusion matrices, calibration) + tests. | **Satisfied** | `write_model_metrics_artifacts` → `outputs/reports/model_metrics/` in both step-5 entrypoints; `src/trading_crab_lib/prediction/model_metrics_artifacts.py`; `tests/test_models_reporting.py` including `test_model_metrics_artifacts_schema_and_behavior_coverage`. |
| 4 | Phase 3 planning/validation docs + tests aligned for verification advance. | **Satisfied** | `03-VALIDATION.md` references `tests/test_models_*.py`; Nyquist frontmatter complete; this SUMMARY + `03-supervised-regime-behavior-models-VERIFICATION.md` updated under Phase 25. |

## Artifact paths (plan-04)

| Artifact | Status | Evidence |
|----------|--------|----------|
| `pipelines/05_predict.py` (≥120 lines) | **Satisfied** | 188 lines; step 5 + metrics + behavior persistence. |
| `run_pipeline.py` step 5 (≥120 lines) | **Satisfied** | File 1452 lines; step 5 block matches `05_predict` behavior. |
| `config/settings.yaml` contains `prediction.behavior_horizons_quarters` | **Satisfied** | Line ~372: `behavior_horizons_quarters: [1]`. |
| `outputs/models/behavior_models.pkl` | **Satisfied** | Written in both entrypoints when step 5 runs. |
| `outputs/reports/model_metrics/cv_summary.parquet` (and siblings) | **Satisfied** | Produced by `write_model_metrics_artifacts` (see `model_metrics_artifacts.py` for schema). |
| `tests/test_models_reporting.py` (≥80 lines) | **Satisfied** | 276 lines. |

## Closure

Plan-04 **must_haves** are **satisfied** in the current repo under `trading_crab_lib`. No waiver is required for CLOSURE-03. Optional **human** checks for model quality remain in **VERIFICATION** — they do not block GSD closure.

**Phase 25** — `25-SUMMARY.md` in `25-v1-0-phase3-plan04-reconciliation/` records traceability and commands run.
