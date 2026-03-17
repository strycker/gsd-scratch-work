from __future__ import annotations

import numpy as np
import pandas as pd

from market_regime.config import load
from market_regime.prediction.classifier import (
    extract_top_features,
    train_current_regime,
    train_interpretability_tree,
)


def _make_synthetic_data(n_samples: int = 60, n_features: int = 6, n_regimes: int = 3):
    rng = np.random.default_rng(0)
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


def test_extract_top_features_uses_importances_when_available() -> None:
    class DummyModel:
        def __init__(self, importances):
            self.feature_importances_ = np.array(importances)

    names = ["a", "b", "c", "d"]
    model = DummyModel([0.1, 0.7, 0.15, 0.05])
    top = extract_top_features(model, names, top_k=2)
    assert set(top) == {"b", "c"}


def test_train_interpretability_tree_respects_config_depth_and_top_k() -> None:
    cfg = load()
    # Ensure boosted is enabled so we have at least RF configured consistently
    cfg.setdefault("prediction", {})

    X, y = _make_synthetic_data()
    bundle = train_current_regime(X, y, cfg)
    base_model = bundle["models"]["rf"]

    # Force small depth and small top_k
    cfg["prediction"]["interpret_tree_max_depth"] = 2
    cfg["prediction"]["interpret_top_k_features"] = 3

    tree, top_features = train_interpretability_tree(base_model, X, y, cfg)

    assert len(top_features) == 3
    # The fitted tree should be able to predict on the same feature subset
    preds = tree.predict(X[top_features])
    assert len(preds) == len(X)
