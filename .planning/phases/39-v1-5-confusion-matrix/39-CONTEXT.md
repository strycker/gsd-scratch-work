# Phase 39: Confusion matrix (classifier diagnostics) — Context

**Gathered:** 2026-03-27  
**Status:** Ready for planning  
**Source:** `.planning/ROADMAP.md` (v1.5) + `.planning/REQUIREMENTS.md` (**TMPL-03**)

## Phase boundary

Deliver a **visual confusion matrix** for supervised regime classifiers, aligned with **CLAUDE.md** “Remaining Gaps” and legacy **`supervised.py`** reporting style, without duplicating metrics logic:

- **Data source:** Step 5 already writes tidy confusion counts to **`outputs/reports/model_metrics/confusion_matrices.parquet`** via **`write_model_metrics_artifacts()`** (`family`, `model`, `horizon`, `fold`, `true_label`, `pred_label`, `count`) — see **`model_metrics_artifacts.py`**.
- **Visualization:** New helper in **`src/trading_crab_lib/plotting.py`** (name TBD in plan: e.g. **`plot_regime_confusion_matrix`**) using **`matplotlib`** / **`seaborn`** consistent with **`REGIME_CMAP`** / existing step-5 plots.
- **Wiring:** Call from **`run_pipeline.py`** **`step5_predict`** when **`run_cfg.generate_plots`** (same block as **`plot_feature_importance`**, **`plot_predicted_vs_actual`**). Optional: **`pipelines/05_predict.py`** if we want parity when run standalone with plots — plan should decide one or both.

**Non-goals:** Changing **`FoldReport`** / CV splits; retraining models; editing **`legacy/`**. Full **notebook** tutorial (optional stretch).

## Implementation decisions (locked)

- **Primary plot:** **Current-regime** multiclass RF (`family == "regime"`, `model == "rf"`, `horizon` null/NaN). Aggregate **across folds** by summing `count` for each `(true_label, pred_label)` unless a clearer fold (“last fold”) is specified in plan.
- **Output path:** **`outputs/plots/`** with existing naming: **`step_05_confusion_matrix.png`** (or suffix by model if multiple plots).
- **Tests:** Synthetic tidy **`DataFrame`** or temp parquet — **no network**, no full pipeline.

## Canonical references

- `src/trading_crab_lib/prediction/model_metrics_artifacts.py` — `_confusion_tidy`, parquet schema
- `src/trading_crab_lib/plotting.py` — `_save_or_show`, `PLOT_DIR`, `RunConfig`
- `run_pipeline.py` — `step5_predict` plot block (~958–976)
- `tests/test_models_reporting.py` — metrics artifact expectations

## Deferred

- Per-forward-horizon binary matrices; behavior-model matrices — backlog-only unless plan scope expands.
