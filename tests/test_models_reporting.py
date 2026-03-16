from __future__ import annotations

import copy

from market_regime.prediction.classifier import model_metrics_summary


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
        "cv_reports": {
            "dt": [
                _fake_report(0.8, 10, 12),
                _fake_report(0.9, 8, 9),
            ],
            "rf": [
                _fake_report(0.85, 11, 11),
                _fake_report(0.88, 9, 10),
            ],
        },
    }
    original = copy.deepcopy(fake_results)

    summary = model_metrics_summary(fake_results)

    # Input must not be mutated
    assert fake_results == original

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
            "cv_reports": {
                "rf": [
                    _fake_report(0.7, 5, 7),
                    _fake_report(0.75, 6, 8),
                ]
            }
        },
        2: {
            "cv_reports": {
                "rf": [
                    _fake_report(0.65, 4, 6),
                    _fake_report(0.68, 5, 7),
                ]
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

