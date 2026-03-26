"""
Prediction subpackage for supervised regime and behavior models.

This package provides two layers of API:

- Modern, test-driven helpers in `classifier.py` (used by Phase 3 tests).
- Backwards-compatible wrappers (`train_current_regime`, `train_decision_tree`,
  `train_forward_classifiers`, `predict_current`) used by the legacy pipeline
  and `run_pipeline.py`.
"""

# Wrappers below keep older call sites working; classifier.py holds the canonical implementations.

from __future__ import annotations

from typing import Any

from sklearn.tree import DecisionTreeClassifier

from . import classifier as _clf

# Re-export modern helpers for tests and new code
FoldReport = _clf.FoldReport
make_behavior_labels = _clf.make_behavior_labels
model_metrics_summary = _clf.model_metrics_summary
train_forward_behavior_models = _clf.train_forward_behavior_models


def train_current_regime(X, y, cfg: dict) -> Any:
    """
    Backwards-compatible wrapper used by legacy code.

    Delegates to classifier.train_current_regime() and returns the
    RandomForest model (RF) used for current-regime prediction.
    """
    cv_splits = cfg.get("prediction", {}).get("cv_splits", 5)
    bundle = _clf.train_current_regime(X, y, cv_splits=cv_splits)
    return bundle["models"]["rf"]


def train_decision_tree(X, y, cfg: dict) -> DecisionTreeClassifier:
    """
    Backwards-compatible DecisionTree trainer for current-regime prediction.
    """
    max_depth = cfg.get("prediction", {}).get("dt_max_depth", 8)
    dt = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    dt.fit(X, y)
    return dt


def train_forward_classifiers(X, y, cfg: dict) -> dict:
    """
    Backwards-compatible wrapper around classifier.train_forward_classifiers().

    Returns the multi-horizon bundle expected by run_pipeline.py.
    """
    pcfg = cfg.get("prediction", {})
    horizons = pcfg.get("forward_horizons_quarters", [1, 2, 4, 8])
    cv_splits = pcfg.get("cv_splits", 5)
    return _clf.train_forward_classifiers(X, y, horizons=horizons, cv_splits=cv_splits)


def predict_current(model, X_now):
    """
    Backwards-compatible helper that scores the most recent row in X_now
    and returns a simple regime + probabilities dict.
    """
    proba = model.predict_proba(X_now.iloc[[-1]])[0]
    classes = model.classes_
    prob_by_class = {int(c): float(p) for c, p in zip(classes, proba, strict=False)}
    best_regime = max(prob_by_class.items(), key=lambda kv: kv[1])[0]
    return {"regime": best_regime, "probabilities": prob_by_class}


__all__ = [
    # Modern helpers
    "FoldReport",
    "make_behavior_labels",
    "model_metrics_summary",
    "train_forward_behavior_models",
    # Legacy-compatible API
    "train_current_regime",
    "train_decision_tree",
    "train_forward_classifiers",
    "predict_current",
]
