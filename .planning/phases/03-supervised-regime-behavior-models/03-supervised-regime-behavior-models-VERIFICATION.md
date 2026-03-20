---
phase: 03-supervised-regime-behavior-models
verified: 2026-03-19T00:00:00Z
status: complete
score: 4/4 must-haves verified
gaps:
  - truth: "Model-related tests exist and can be run in isolation for Phase 3 behaviors."
    status: completed
    reason: "Phase 3 validation docs were reconciled to the real test files and Wave 0 now reflects the updated test suite."
    artifacts:
      - path: ".planning/phases/03-supervised-regime-behavior-models/03-VALIDATION.md"
        issue: "References `tests/unit/test_classifier.py` and specific test names that do not exist; frontmatter has nyquist_compliant: false and wave_0_complete: false."
      - path: "tests/test_models_regime.py"
        issue: "Implements the regime tests that VALIDATION.md intends but under a different filename and without updating the validation matrix."
      - path: "tests/test_models_behavior.py"
        issue: "Implements behavior-model tests that are not wired into the current validation matrix."
      - path: "tests/test_models_reporting.py"
        issue: "Covers regime metrics aggregation only; behavior metrics summarisation is implemented separately in `trading_crab_lib.prediction` but not yet under test."
    missing:
      - "(none) — docs/test wiring reconciled"
  - truth: "Supervised model training never uses non-time-series-aware validation or forward-looking features."
    status: completed
    reason: "Step-5 now enforces `features_supervised.parquet` by default and only falls back to `features.parquet` with an explicit opt-in flag."
    artifacts:
      - path: "pipelines/05_predict.py"
        issue: "Prefers `features_supervised.parquet` (causal) but falls back silently—with only a warning—to `features.parquet` if the supervised file is missing, which may reintroduce leakage depending on how `features.parquet` was produced."
      - path: "src/trading_crab_lib/prediction/classifier.py"
        issue: "All CV helpers use `TimeSeriesSplit` with no shuffling and construct forward targets via `regimes.shift(-h)`, which is correct; there is no assertion that the features passed in are from the causal checkpoint."
      - path: "src/trading_crab_lib/prediction.py"
        issue: "Behavior-model helpers also use TimeSeriesSplit and shifted returns, but similarly assume the caller has supplied causal features."
    missing:
      - "(none) — leakage guardrails now gated + unit-tested"
human_verification:
  - test: "Inspect end-to-end supervised model performance and confusion-style summaries on real quarterly data."
    expected: "Current-regime and forward-regime models show plausible, stable accuracy/F1 across TimeSeriesSplit folds, and behavior models produce reasonable up/flat/down distributions for major ETFs and simple portfolios."
    why_human: "Judging whether numerical performance is 'good enough' for live use, and whether confusion reports and behavior distributions align with investor intuition, requires domain judgment beyond what automated tests provide."
---

# Phase 3: Supervised Regime & Behavior Models Verification Report

**Phase Goal:** Train, validate, and report on supervised models that turn regimes into real-time and forward-looking signals for regimes and ETF/portfolio behavior.
**Verified:** 2026-03-16T00:00:00Z  
**Status:** human_needed  
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| # | Truth                                                                                                      | Status        | Evidence |
|---|------------------------------------------------------------------------------------------------------------|--------------|----------|
| 1 | There is a clear, centralized API for training current-regime, forward-regime, and behavior models using causal features and Phase 2 regime labels. | ✓ VERIFIED    | `src/trading_crab_lib/prediction/classifier.py` exposes `train_current_regime`, `train_forward_classifiers`, `train_forward_behavior_models`, and `model_metrics_summary`; `src/trading_crab_lib/prediction.py` exposes behavior helpers; `pipelines/05_predict.py` wires the current and forward regime helpers into step 5. |
| 2 | Model-related tests exist and can be run in isolation for Phase 3 behaviors.                              | ✓ VERIFIED    | `tests/test_models_regime.py`, `tests/test_models_behavior.py`, and `tests/test_models_reporting.py` provide synthetic, network-free tests, and `03-VALIDATION.md` now references the correct files with Wave 0 mapped to them. |
| 3 | Supervised model training never uses non-time-series-aware validation or forward-looking features.        | ✓ VERIFIED    | Step 5 now enforces `features_supervised.parquet` by default via `select_step5_feature_path`, and only falls back to `features.parquet` with explicit `--allow-noncausal-features` (unit-tested). |
| 4 | Forward regime and behavior models are wired into the prediction layer in a way that later phases can consume. | ✓ VERIFIED    | `pipelines/05_predict.py` and `run_pipeline.py` step 5 now train/persist behavior models and write metrics artifacts; metrics + gating schema are covered in `tests/test_models_reporting.py` and `tests/test_models_regime.py`. |

**Score:** 4/4 must-haves verified.

### Required Artifacts

| Artifact                                | Expected                                                                                  | Status     | Details |
|-----------------------------------------|------------------------------------------------------------------------------------------|-----------|---------|
| `src/trading_crab_lib/prediction/classifier.py` | Centralized supervised regime and (classifier-based) behavior model helpers with TimeSeriesSplit CV and metric aggregation. | ✓ VERIFIED | File exists (~400+ lines); defines `_tscv_reports`, `FoldReport`, `train_current_regime`, `train_forward_classifiers`, `make_behavior_labels`, `train_forward_behavior_models`, and `model_metrics_summary`, all using walk-forward CV and shifted targets. |
| `src/trading_crab_lib/prediction.py`      | Higher-level supervised helpers, including behavior models and a generic metrics flattener. | ✓ VERIFIED | File exists and provides `make_behavior_labels`, `train_forward_behavior_models`, and a row-oriented `model_metrics_summary` used by behavior-focused tests. |
| `tests/test_models_regime.py`          | Tests for current and forward regime classifiers, including leakage/CV ordering checks and probability sanity checks. | ✓ VERIFIED | Synthetic tests assert TimeSeriesSplit ordering (train indices < test indices), presence of `FoldReport`, and well-formed probability outputs for current and forward regime bundles. |
| `tests/test_models_behavior.py`        | Tests for ETF/portfolio behavior label construction and directional behavior models.      | ✓ VERIFIED | Synthetic tests cover up/flat/down labelling semantics, dropping of trailing periods, and per-asset behavior models with probability-normalisation checks. |
| `tests/test_models_reporting.py`       | Tests for model metrics and reporting helpers.                                            | ✓ VERIFIED | Exercises `classifier.model_metrics_summary` for current and forward regime bundles and now validates metrics-artifact schema + behavior coverage. |

### Key Link Verification

| From                            | To                                         | Via / Pattern                                                       | Status   | Details |
|---------------------------------|--------------------------------------------|---------------------------------------------------------------------|----------|---------|
| `pipelines/05_predict.py`       | `src/trading_crab_lib/prediction/classifier.py` | `from trading_crab_lib.prediction.classifier import train_current_regime, train_forward_classifiers` | ✓ WIRED  | Step 5 uses the centralized helpers on causal features (when available) and persists model bundles to `outputs/models/`. |
| `tests/test_models_regime.py`   | `src/trading_crab_lib/prediction/classifier.py` | `from trading_crab_lib.prediction.classifier import FoldReport, train_current_regime, train_forward_classifiers` | ✓ WIRED  | Regime tests import and exercise the supervised helpers directly on synthetic data. |
| `tests/test_models_behavior.py` | `src/trading_crab_lib/prediction.py`          | `from trading_crab_lib.prediction import make_behavior_labels, train_forward_behavior_models` | ✓ WIRED  | Behavior tests exercise the behavior helpers exposed from the prediction module. |
| `tests/test_models_reporting.py`| `src/trading_crab_lib/prediction/classifier.py` | `from trading_crab_lib.prediction.classifier import model_metrics_summary` | ✓ WIRED  | Reporting tests cover regime metrics aggregation; behavior metrics flattener lives in `prediction.py` and is not yet under test. |

### Requirements Coverage (MODEL-01 – MODEL-04)

| Requirement | Description (short)                                  | Status | Evidence |
|------------|------------------------------------------------------|--------|----------|
| MODEL-01   | Current-regime classifier with causal features and time-series aware validation. | PASS   | `train_current_regime` uses `TimeSeriesSplit` via `_tscv_reports`; step 5 preferentially consumes `features_supervised.parquet`; `tests/test_models_regime.py` asserts temporal ordering and probability shape, and `pipelines/05_predict.py` demonstrates end-to-end integration and model persistence. |
| MODEL-02   | Forward regime transition models with probabilities for ≥1 quarter ahead. | PASS   | `train_forward_classifiers` builds shifted targets via `regimes.shift(-h)`, drops trailing quarters, and trains DT/RF bundles per horizon; `pipelines/05_predict.py` calls this helper for configured horizons and saves the resulting bundles; tests verify correct shifting, exclusion of trailing samples, and probability normalisation for `h=1`. |
| MODEL-03   | Forward ETF/portfolio behavior models (directional up/flat/down). | PASS   | `pipelines/05_predict.py` and `run_pipeline.py` step 5 now train and persist behavior models (asset × horizon) and write metrics artifacts; behavior coverage is asserted in `tests/test_models_behavior.py` and `tests/test_models_reporting.py`. |
| MODEL-04   | Transparent, time-series aware evaluation and reporting for supervised models. | PASS   | Regime + behavior CV diagnostics are captured via walk-forward `FoldReport`s, persisted as structured metrics artifacts (`cv_summary.parquet`, `per_fold.jsonl`, `confusion_matrices.parquet`, `calibration.parquet`), and validated by the updated `tests/test_models_reporting.py`. |

### Anti-Patterns and Nyquist Validation Gaps

| File                                       | Line(s) (approx) | Pattern / Issue                                           | Severity | Impact |
|--------------------------------------------|------------------|-----------------------------------------------------------|----------|--------|
| `.planning/phases/03-supervised-regime-behavior-models/03-VALIDATION.md` | frontmatter & table | Validation matrix now references existing test files and Wave 0 mapping. | PASS     | Nyquist tracking is now aligned with actual test suite. |
| `pipelines/05_predict.py`                 | feature load block | Supervised feature gating is enforced (no silent fallback without opt-in). | PASS     | Leakage guardrails are gated behind `--allow-noncausal-features` and covered by unit tests. |

### Human Verification Required

1. **Model performance sanity on real data**
   - **Test:** Run `pipelines/05_predict.py` against real checkpoints, inspect printed current-regime probabilities and any downstream plots/notebooks that use the supervised bundles.
   - **Expected:** Probabilities and predicted regimes should look plausible across history (no degenerate always-one-regime behaviour; CV metrics should be in a reasonable range for quarterly macro data).
   - **Why human:** Determining whether the achieved metrics are acceptable for your decision-making tolerance is a judgment call, not a binary pass/fail.

2. **Behavior model usefulness**
   - **Test:** On a sample of ETFs/portfolios and horizons, inspect behavior model up/flat/down predictions in a notebook (e.g. overlay against realised returns).
   - **Expected:** Predicted directional labels should correlate with realised returns better than chance and be stable enough to inform regime-aware allocations.
   - **Why human:** Assessing whether the directional signals are economically meaningful (vs. noisy but statistically non-zero) requires domain expertise.

### Gaps Summary

Phase 3’s supervised regime and behavior models are **functionally implemented, safety-hardened, and fully wired** into step 5 with walk-forward validation. Both structured metrics artifacts and gating behavior are covered by automated tests, and Phase 3 validation docs are reconciled to reflect the real test suite and Nyquist status.

---

_Verified: 2026-03-19T00:00:00Z_  
_Verifier: Claude (gsd-verifier)_

