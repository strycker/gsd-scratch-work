from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Callable, Dict, Hashable, Iterable, List

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import TimeSeriesSplit
from sklearn.tree import DecisionTreeClassifier

log = logging.getLogger(__name__)


@dataclass
class FoldReport:
    """Container for a single CV fold report and its indices."""

    report: Dict[str, dict]
    train_indices: List[int]
    test_indices: List[int]


def _tscv_reports(
    model_factory: Callable[[], RandomForestClassifier | DecisionTreeClassifier],
    X: pd.DataFrame,
    y: pd.Series,
    n_splits: int,
    label: str,
) -> List[FoldReport]:
    """
    Run TimeSeriesSplit CV and return per-fold classification_report dicts.

    Each FoldReport also includes the train/test index positions so callers and
    tests can verify temporal ordering (no leakage).
    """
    tscv = TimeSeriesSplit(n_splits=n_splits)
    results: List[FoldReport] = []

    for fold, (train_idx, test_idx) in enumerate(tscv.split(X), start=1):
        clf = model_factory()
        clf.fit(X.iloc[train_idx], y.iloc[train_idx])
        y_pred = clf.predict(X.iloc[test_idx])

        rep = classification_report(
            y.iloc[test_idx],
            y_pred,
            output_dict=True,
            zero_division=0,
        )

        results.append(
            FoldReport(
                report=rep,
                train_indices=train_idx.tolist(),
                test_indices=test_idx.tolist(),
            )
        )

        log.debug(
            "%s fold %d/%d — accuracy=%.3f",
            label,
            fold,
            n_splits,
            float(rep.get("accuracy", 0.0)),
        )

    return results


def _unique_labels(labels: pd.Series | Iterable[Hashable]) -> List[Hashable]:
    """Return a stable, sorted list of unique labels."""
    if isinstance(labels, pd.Series):
        uniques = pd.unique(labels)
    else:
        uniques = list(dict.fromkeys(labels))  # preserve order
    try:
        # Sort when possible for determinism; fall back to original order
        return sorted(uniques.tolist() if isinstance(uniques, np.ndarray) else list(uniques))
    except TypeError:
        return list(uniques)


def train_current_regime(
    features: pd.DataFrame,
    labels: pd.Series,
    cv_splits: int = 5,
) -> dict:
    """
    Train current-regime classifiers with walk-forward TimeSeriesSplit CV.

    Returns a dict:
        {
            "models": {"dt": DecisionTreeClassifier, "rf": RandomForestClassifier},
            "cv_reports": {
                "dt": [FoldReport, ...],
                "rf": [FoldReport, ...],
            },
            "labels": [label0, label1, ...],
        }
    """
    if features.empty:
        raise ValueError("features must be non-empty")
    if len(features) != len(labels):
        raise ValueError("features and labels must have the same length")

    label_list = _unique_labels(labels)

    def make_dt() -> DecisionTreeClassifier:
        return DecisionTreeClassifier(max_depth=8, random_state=42)

    def make_rf() -> RandomForestClassifier:
        return RandomForestClassifier(
            max_depth=12,
            n_estimators=200,
            random_state=42,
            n_jobs=-1,
            class_weight="balanced",
        )

    cv_reports: Dict[str, List[FoldReport]] = {
        "dt": _tscv_reports(make_dt, features, labels, cv_splits, "DT current-regime"),
        "rf": _tscv_reports(make_rf, features, labels, cv_splits, "RF current-regime"),
    }

    models = {
        "dt": make_dt(),
        "rf": make_rf(),
    }
    for name, clf in models.items():
        clf.fit(features, labels)
        log.info(
            "%s — in-sample classification report:\n%s",
            name,
            classification_report(labels, clf.predict(features), zero_division=0),
        )

    return {
        "models": models,
        "cv_reports": cv_reports,
        "labels": label_list,
    }


def train_forward_classifiers(
    features: pd.DataFrame,
    regimes: pd.Series,
    horizons: List[int],
    cv_splits: int = 5,
) -> Dict[int, dict]:
    """
    Train forward regime classifiers for each horizon in `horizons`.

    For each horizon h:
      - Construct targets y_{t+h} via regimes.shift(-h)
      - Drop rows with missing targets so the last h rows are excluded
      - Train DecisionTree + RandomForest models with TimeSeriesSplit CV

    Returns:
        {
            h: {
                "models": {"dt": ..., "rf": ...},
                "cv_reports": {"dt": [FoldReport, ...], "rf": [FoldReport, ...]},
                "class_order": [regime0, regime1, ...],
            },
            ...
        }
    """
    if features.empty:
        raise ValueError("features must be non-empty")
    if len(features) != len(regimes):
        raise ValueError("features and regimes must have the same length")
    if not horizons:
        raise ValueError("horizons must be a non-empty list of integers")

    results: Dict[int, dict] = {}

    for h in horizons:
        if h <= 0:
            raise ValueError(f"horizon must be positive, got {h}")

        y_future = regimes.shift(-h)
        mask = y_future.notna()
        y_h = y_future[mask]
        X_h = features.loc[mask]

        if len(X_h) == 0:
            raise ValueError(f"no samples available for horizon {h}")

        class_order = _unique_labels(y_h)

        def make_dt() -> DecisionTreeClassifier:
            return DecisionTreeClassifier(max_depth=8, random_state=42)

        def make_rf() -> RandomForestClassifier:
            return RandomForestClassifier(
                max_depth=12,
                n_estimators=200,
                random_state=42,
                n_jobs=-1,
                class_weight="balanced",
            )

        cv_reports: Dict[str, List[FoldReport]] = {
            "dt": _tscv_reports(make_dt, X_h, y_h, cv_splits, f"DT forward h={h}"),
            "rf": _tscv_reports(make_rf, X_h, y_h, cv_splits, f"RF forward h={h}"),
        }

        models = {
            "dt": make_dt(),
            "rf": make_rf(),
        }
        for name, clf in models.items():
            clf.fit(X_h, y_h)
            log.info(
                "%s h=%d — in-sample classification report:\n%s",
                name,
                h,
                classification_report(y_h, clf.predict(X_h), zero_division=0),
            )

        results[h] = {
            "models": models,
            "cv_reports": cv_reports,
            "class_order": class_order,
        }

    return results


def _aggregate_classification_reports(
    reports: List[Dict[str, dict]],
) -> dict:
    """
    Aggregate a list of classification_report(output_dict=True) dicts.

    Computes mean accuracy, macro-F1, and weighted-F1 plus per-class metrics.
    """
    if not reports:
        raise ValueError("reports must be non-empty")

    special_keys = {"accuracy", "macro avg", "weighted avg"}
    classes: set[str] = set()
    for rep in reports:
        classes.update(k for k in rep.keys() if k not in special_keys)

    per_model = {
        "overall": {
            "accuracy": float(np.mean([rep.get("accuracy", 0.0) for rep in reports])),
            "macro_f1": float(
                np.mean([rep["macro avg"]["f1-score"] for rep in reports])
            ),
            "weighted_f1": float(
                np.mean([rep["weighted avg"]["f1-score"] for rep in reports])
            ),
        },
        "per_class": {},
    }

    for cls in sorted(classes):
        precisions = []
        recalls = []
        f1s = []
        supports = []
        for rep in reports:
            if cls not in rep:
                continue
            precisions.append(rep[cls]["precision"])
            recalls.append(rep[cls]["recall"])
            f1s.append(rep[cls]["f1-score"])
            supports.append(rep[cls]["support"])

        if not precisions:
            continue

        per_model["per_class"][cls] = {
            "precision": float(np.mean(precisions)),
            "recall": float(np.mean(recalls)),
            "f1": float(np.mean(f1s)),
            "support": float(np.sum(supports)),
        }

    return per_model


def model_metrics_summary(results: dict) -> dict:
    """
    Summarize model metrics from train_current_regime / train_forward_classifiers.

    The function is intentionally tolerant of input shape:
      - If results has top-level "models" / "cv_reports" keys, it is treated as a
        single (current) regime model bundle.
      - Otherwise, results is assumed to be {horizon: {...}} from
        train_forward_classifiers.
    """
    # Single-bundle (current-regime) case
    if "cv_reports" in results and isinstance(results.get("cv_reports"), dict):
        summary = {}
        for model_name, folds in results["cv_reports"].items():
            rep_dicts = [fr.report if isinstance(fr, FoldReport) else fr for fr in folds]
            summary[model_name] = _aggregate_classification_reports(rep_dicts)
        return {"current": summary}

    # Multi-horizon case
    out: Dict[int, dict] = {}
    for horizon, bundle in results.items():
        cv_reports = bundle.get("cv_reports", {})
        model_summaries: Dict[str, dict] = {}
        for model_name, folds in cv_reports.items():
            rep_dicts = [fr.report if isinstance(fr, FoldReport) else fr for fr in folds]
            model_summaries[model_name] = _aggregate_classification_reports(rep_dicts)
        out[horizon] = model_summaries

    return out

