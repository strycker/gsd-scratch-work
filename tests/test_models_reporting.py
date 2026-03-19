from __future__ import annotations

import copy
import json

import numpy as np
import pandas as pd

from market_regime.prediction.classifier import (
    model_metrics_summary,
    train_current_regime,
    train_forward_classifiers,
    train_forward_behavior_models,
)
from market_regime.prediction.model_metrics_artifacts import write_model_metrics_artifacts


def _fake_report(accuracy: float, cls0_support: int, cls1_support: int):
    return {
        "0": {
            "precision": 0.8,
            "recall": 0.7,
            "f1-score": 0.75,
            "support": cls0_support,
        },
        "1": {
            "precision": 0.6,
            "recall": 0.9,
            "f1-score": 0.72,
            "support": cls1_support,
        },
        "accuracy": accuracy,
        "macro avg": {
            "precision": 0.7,
            "recall": 0.8,
            "f1-score": 0.735,
            "support": cls0_support + cls1_support,
        },
        "weighted avg": {
            "precision": 0.71,
            "recall": 0.81,
            "f1-score": 0.74,
            "support": cls0_support + cls1_support,
        },
    }


def test_model_metrics_summary_current_bundle():
    fake_results = {
        "models": {"dt": object(), "rf": object()},
        "cv_scores": {
            "dt": {
                "reports": [
                    _fake_report(0.8, 10, 12),
                    _fake_report(0.9, 8, 9),
                ]
            },
            "rf": {
                "reports": [
                    _fake_report(0.85, 11, 11),
                    _fake_report(0.88, 9, 10),
                ]
            },
        },
    }
    summary = model_metrics_summary(fake_results)

    assert "current" in summary
    cur = summary["current"]
    assert set(cur.keys()) == {"dt", "rf"}

    for model_name, stats in cur.items():
        overall = stats["overall"]
        assert 0.0 <= overall["accuracy"] <= 1.0
        assert 0.0 <= overall["macro_f1"] <= 1.0
        assert 0.0 <= overall["weighted_f1"] <= 1.0

        per_class = stats["per_class"]
        for cls, metrics in per_class.items():
            assert metrics["precision"] >= 0.0
            assert metrics["recall"] >= 0.0
            assert metrics["f1"] >= 0.0
            assert metrics["support"] >= 0.0


def test_model_metrics_summary_forward_horizons():
    fake_forward = {
        1: {
            "cv_scores": {
                "rf": {
                    "reports": [
                        _fake_report(0.7, 5, 7),
                        _fake_report(0.75, 6, 8),
                    ]
                }
            }
        },
        2: {
            "cv_scores": {
                "rf": {
                    "reports": [
                        _fake_report(0.65, 4, 6),
                        _fake_report(0.68, 5, 7),
                    ]
                }
            }
        },
    }

    original = copy.deepcopy(fake_forward)
    summary = model_metrics_summary(fake_forward)

    # Input must not be mutated
    assert fake_forward == original

    assert set(summary.keys()) == {1, 2}
    for h, models in summary.items():
        assert "rf" in models
        overall = models["rf"]["overall"]
        assert 0.0 <= overall["accuracy"] <= 1.0
        assert 0.0 <= overall["macro_f1"] <= 1.0
        assert 0.0 <= overall["weighted_f1"] <= 1.0


def test_model_metrics_summary_combined_regime_and_behavior() -> None:
    # Regime-style pre-aggregated metrics (e.g. from current / forward regime models).
    regime_rows = [
        {
            "model": "rf",
            "metric": "accuracy",
            "value": 0.82,
            "asset": None,
            "horizon": None,
            "class_label": "0",
        },
        {
            "model": "rf",
            "metric": "macro_f1",
            "value": 0.79,
            "asset": None,
            "horizon": None,
            "class_label": None,
        },
    ]

    # Behavior-style metrics keyed by asset / horizon / class.
    behavior_rows = [
        {
            "model": "behavior-rf",
            "metric": "accuracy",
            "value": 0.70,
            "asset": "ETF1",
            "horizon": 1,
            "class_label": "up",
        },
        {
            "model": "behavior-rf",
            "metric": "accuracy",
            "value": 0.65,
            "asset": "ETF1",
            "horizon": 1,
            "class_label": "down",
        },
    ]

    combined = {
        "regime": regime_rows,
        "behavior": behavior_rows,
    }

    summary = model_metrics_summary(combined)
    rows = summary["rows"]

    # All rows should carry a family tag and preserve basic fields.
    assert any(r["family"] == "regime" for r in rows)
    assert any(r["family"] == "behavior" for r in rows)

    # Behavior entries should be filterable by asset and class label.
    etf1_up = [
        r
        for r in rows
        if r["family"] == "behavior"
        and r["asset"] == "ETF1"
        and r["class_label"] == "up"
    ]
    assert len(etf1_up) == 1
    assert 0.0 <= etf1_up[0]["value"] <= 1.0


def test_model_metrics_artifacts_schema_and_behavior_coverage(tmp_path) -> None:
    # Synthetic data (no network, no repo data dependencies).
    n = 36
    rng = np.random.default_rng(0)
    index = pd.RangeIndex(n)

    X = pd.DataFrame(
        rng.normal(size=(n, 6)),
        index=index,
        columns=[f"f{i}" for i in range(6)],
    )
    regimes = pd.Series(rng.integers(0, 3, size=n), index=index)

    returns = pd.DataFrame(
        {
            "ETF1": rng.normal(loc=0.0, scale=0.03, size=n).cumsum(),
            "ETF2": rng.normal(loc=0.0, scale=0.02, size=n).cumsum(),
        },
        index=index,
    )

    current_bundle = train_current_regime(X, regimes, cv_splits=3)
    forward_models = train_forward_classifiers(
        X, regimes, horizons=[1], cv_splits=3
    )
    behavior_bundle = train_forward_behavior_models(
        X, regimes, returns, horizons=[1], cv_splits=3
    )

    out_dir = tmp_path / "outputs" / "reports" / "model_metrics"
    write_model_metrics_artifacts(
        output_dir=out_dir,
        feature_source="features_supervised",
        noncausal_used=False,
        regime_current_bundle=current_bundle,
        forward_models=forward_models,
        behavior_bundle=behavior_bundle,
    )

    cv_df = pd.read_parquet(out_dir / "cv_summary.parquet")
    required_cv_cols = {
        "family",
        "model",
        "horizon",
        "asset",
        "metric",
        "value",
        "n_splits",
    }
    assert required_cv_cols.issubset(set(cv_df.columns))
    assert (cv_df["family"] == "behavior").any(), "expected behavior metrics rows"

    conf_df = pd.read_parquet(out_dir / "confusion_matrices.parquet")
    required_conf_cols = {
        "family",
        "model",
        "horizon",
        "asset",
        "fold",
        "true_label",
        "pred_label",
        "count",
    }
    assert required_conf_cols.issubset(set(conf_df.columns))

    cal_df = pd.read_parquet(out_dir / "calibration.parquet")
    required_cal_cols = {
        "family",
        "model",
        "horizon",
        "asset",
        "fold",
        "class_label",
        "bin",
        "predicted_prob_mean",
        "observed_freq",
        "brier",
    }
    assert required_cal_cols.issubset(set(cal_df.columns))

    per_fold_path = out_dir / "per_fold.jsonl"
    assert per_fold_path.exists()
    with per_fold_path.open("r", encoding="utf-8") as f:
        first = json.loads(next(iter(f)))
    assert "train_indices" in first and "test_indices" in first
    assert "classification_report" in first

