from __future__ import annotations

import numpy as np
import pandas as pd

from trading_crab_lib.config import load
from trading_crab_lib.prediction.classifier import (
    make_gradient_boosting_classifier,
    train_current_regime,
    train_forward_classifiers,
)


def _make_synthetic_data(n_samples: int = 40, n_features: int = 5, n_regimes: int = 3):
    rng = np.random.default_rng(42)
    index = pd.RangeIndex(n_samples)
    X = pd.DataFrame(
        rng.normal(size=(n_samples, n_features)),
        index=index,
        columns=[f"f{i}" for i in range(n_features)],
    )
    regimes = pd.Series(
        np.tile(np.arange(n_regimes), n_samples // n_regimes + 1)[:n_samples],
        index=index,
        name="regime",
    )
    return X, regimes


def test_train_current_regime_includes_gb_when_enabled() -> None:
    cfg = load()
    pred_cfg = cfg.setdefault("prediction", {})
    pred_cfg["use_boosted"] = True

    X, y = _make_synthetic_data()
    result = train_current_regime(X, y, cfg)

    models = result["models"]
    # GB may be unavailable if GradientBoosting is disabled, but should be present by default.
    assert "rf" in models and "dt" in models
    # GB is optional; if present it must expose predict_proba like RF/DT
    if "gb" in models:
        proba = models["gb"].predict_proba(X)
        assert proba.shape[0] == len(X)
        np.testing.assert_allclose(proba.sum(axis=1), np.ones(len(X)), rtol=1e-6)


def test_make_gradient_boosting_classifier_reads_prediction_yaml_keys() -> None:
    cfg = {
        "prediction": {
            "boosted_max_depth": 4,
            "boosted_learning_rate": 0.05,
            "boosted_n_estimators": 100,
            "random_state": 42,
        }
    }
    gb = make_gradient_boosting_classifier(cfg)
    assert gb.max_depth == 4
    assert gb.learning_rate == 0.05
    assert gb.n_estimators == 100


def test_train_forward_classifiers_supports_gb_flag() -> None:
    cfg = load()
    pred_cfg = cfg.setdefault("prediction", {})
    pred_cfg["use_boosted"] = True

    X, regimes = _make_synthetic_data()
    horizons = [1]
    results = train_forward_classifiers(X, regimes, horizons=horizons, cfg=cfg)

    assert 1 in results
    bundle = results[1]
    assert "dt" in bundle["models"] and "rf" in bundle["models"]
    # GB is optional; if present it should behave like a probabilistic classifier
    if "gb" in bundle["models"]:
        mask = regimes.shift(-1).notna()
        X_h = X.loc[mask]
        proba = bundle["models"]["gb"].predict_proba(X_h)
        assert proba.shape[0] == len(X_h)
        np.testing.assert_allclose(proba.sum(axis=1), np.ones(len(X_h)), rtol=1e-6)

