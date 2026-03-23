---
phase: 19-v1-2-boosted-models
verified: 2026-03-22T18:00:00Z
status: human_needed
score: 5/5 plan must-haves (code + tests); roadmap 3/3 criteria mapped
---

# Phase 19: Boosted models & interpretability — Verification Report

**Phase goal (ROADMAP):** Train/eval hooks for boosted models parallel to RF/DT with time-series CV; metrics alongside existing artifacts; human-readable interpretability for boosted models.

**Requirements:** MODEL-10, MODEL-11

**Verified:** 2026-03-22

**Overall status:** `human_needed` — all **plan must-haves** are verified in code and automated tests; **optional human** confirmation for a full **`python run_pipeline.py --steps 5 --plots`** (or `pipelines/05_predict.py`) with real checkpoints and `use_boosted: true` to confirm `current_regime_gb.pkl` and `current_regime_tree_gb.txt` on disk.

**Scope note:** ROADMAP text references “LightGBM/XGBoost-style”; **delivered path** is sklearn `GradientBoostingClassifier` with config-driven `boosted_*` keys, per **REQUIREMENTS.md** and **`19-SUMMARY.md`** (optional LightGBM deferred).

---

## Goal achievement

### Observable truths (plan `must_haves`)

| # | Truth | Status | Evidence |
|---|--------|--------|----------|
| 1 | `GradientBoostingClassifier` uses `prediction.boosted_*` from config — no duplicate hardcoded GB params in training paths. | ✓ VERIFIED | `make_gradient_boosting_classifier(cfg)` in `classifier.py`; `train_current_regime` / `train_forward_classifiers` use shared factory; `tests/test_models_boosting.py::test_make_gradient_boosting_classifier_reads_prediction_yaml_keys`. |
| 2 | When `use_boosted` and training succeeds, GB current-regime model persisted under `outputs/models/`; metrics include `gb` when present in `cv_scores`. | ✓ VERIFIED | `run_pipeline.py` / `pipelines/05_predict.py` write `current_regime_gb.pkl` when `"gb"` in models; `write_model_metrics_artifacts()` iterates `regime_current_bundle["cv_scores"]` and forward `cv_scores` by model name (includes `gb`). |
| 3 | Forward horizons include `gb` in `cv_scores` when `use_boosted`. | ✓ VERIFIED | `train_forward_classifiers` adds `cv_scores["gb"]` with `_tscv_scores(make_gb, ...)`; `tests/test_models_boosting.py::test_train_forward_classifiers_supports_gb_flag`. |
| 4 | MODEL-11: shallow interpret tree text from GB top‑K features when `interpret_tree_on_boosted` is true. | ✓ VERIFIED | `config/settings.yaml` `interpret_tree_on_boosted`; `run_pipeline.py` + `pipelines/05_predict.py` write `current_regime_tree_gb.txt`; `tests/test_models_interpret_tree.py` GB path. |
| 5 | TimeSeriesSplit CV discipline unchanged for all model families. | ✓ VERIFIED | `_tscv_scores` / `_tscv_reports` unchanged contract; GB uses same `model_factory` pattern as RF/DT. |

**Truths score:** 5/5 (automated + code evidence).

### Required artifacts (plan frontmatter)

| Artifact | Status | Details |
|----------|--------|---------|
| `config/settings.yaml` | ✓ | `interpret_tree_on_boosted`; `boosted_max_depth`, `boosted_learning_rate`, `boosted_n_estimators` under `prediction`. |
| `src/trading_crab_lib/prediction/classifier.py` | ✓ | `make_gradient_boosting_classifier`; shared by current + forward GB. |
| `run_pipeline.py` | ✓ | Step 5 saves `current_regime_gb.pkl`; writes `current_regime_tree_gb.txt` when GB + flag. |
| `pipelines/05_predict.py` | ✓ | `cfg` passed into `train_current_regime` / `train_forward_classifiers`; mirrors pickle + GB interpret tree. |
| `RUNBOOK.md` | ✓ | Step 5 table lists GB pickle + `current_regime_tree_gb.txt`. |

### Key wiring

| Link | Status |
|------|--------|
| `settings.yaml` → `make_gradient_boosting_classifier` | ✓ |
| `train_current_regime` → `models["gb"]`, `cv_scores["gb"]` | ✓ |
| Step 5 → `outputs/models/current_regime_gb.pkl` | ✓ |
| Step 5 → `outputs/reports/current_regime_tree_gb.txt` | ✓ |
| `write_model_metrics_artifacts` → rows for each model in `cv_scores` (including `gb`) | ✓ |

---

## ROADMAP success criteria (Phase 19)

| # | Criterion | Evidence |
|---|-----------|----------|
| 1 | Train/eval hooks parallel to RF/DT with time-series CV. | GB trained via same `_tscv_scores` / `FoldReport` path as RF/DT; tests exercise current + forward with `use_boosted`. |
| 2 | Metrics persisted alongside existing model artifacts. | `cv_summary.parquet` / `per_fold.jsonl` / `confusion_matrices.parquet` / `calibration.parquet` include per-model rows keyed by `cv_scores` entries (including `gb` when trained). |
| 3 | Human-readable tree/plot/text for one boosted model per task family. | **Text:** `current_regime_tree_gb.txt` (required). RF interpret tree + plots remain as before; optional GB-specific plot not required (per plan). |

---

## Requirements coverage

| Requirement | Status |
|-------------|--------|
| **MODEL-10** | ✓ SATISFIED (REQUIREMENTS.md + traceability **Complete**). |
| **MODEL-11** | ✓ SATISFIED |

---

## Anti-patterns

Scanned `classifier.py` (GB paths), `run_pipeline.py` (step 5 GB block), `pipelines/05_predict.py`: no `TODO`/`FIXME` blockers on these paths.

---

## Human verification (optional)

1. **Full step 5** — With checkpoints from steps 1–4 and `prediction.use_boosted: true`, run `python run_pipeline.py --steps 5 --plots` and confirm `outputs/models/current_regime_gb.pkl` and `outputs/reports/current_regime_tree_gb.txt`.
2. **Metrics spot-check** — Open `outputs/reports/model_metrics/cv_summary.parquet` and filter `model == 'gb'` for current-regime and forward horizons (when GB trained).

---

## Gaps summary

**None** for MODEL-10/11 delivery vs plan must-haves.

---

## Automated commands (re-run)

```bash
cd /path/to/repo
. .venv/bin/activate
export PYTHONPATH=src
python -m pytest tests/test_models_boosting.py tests/test_models_interpret_tree.py -q
python -c "from trading_crab_lib.config import load; load(); print('ok')"
```

**Last run:** 6 passed (2026-03-22, project `.venv`).

---

## Verification metadata

**Verification approach:** Goal-backward against plan `must_haves` and ROADMAP success criteria.  
**Must-haves source:** `19-v1-2-boosted-models-01-PLAN.md` frontmatter + `19-SUMMARY.md`.  
**Automated checks:** pytest + config load — green.  
**Human checks required:** 0 mandatory (optional disk/parquet checks above).

---
*Verified: 2026-03-22T18:00:00Z*
