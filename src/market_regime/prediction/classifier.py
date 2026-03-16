from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Callable, Dict, Hashable, Iterable, List, Tuple
import copy

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
    # On very small datasets, full TimeSeriesSplit is not feasible.
    # If we have fewer than 3 samples, skip CV entirely and return no reports.
    if len(X) < 3:
        log.warning(
            "%s: not enough samples (%d) for TimeSeriesSplit CV; skipping CV reports.",
            label,
            len(X),
        )
        return []

    # Guard against requesting more splits than samples — this can happen when
    # running on trimmed feature sets. TimeSeriesSplit requires n_splits < n_samples.
    max_splits = min(max(n_splits, 2), len(X) - 1)
    tscv = TimeSeriesSplit(n_splits=max_splits)
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
            max_splits,
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
            log.warning(
                "train_forward_classifiers: no samples available for horizon %d; "
                "skipping this horizon.",
                h,
            )
            continue

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

    IMPORTANT: This function must not mutate `results`.
    """
    # Work on a deep copy so we never mutate the caller's object.
    data = copy.deepcopy(results)

    # Single-bundle (current-regime) case
    if "cv_reports" in data and isinstance(data.get("cv_reports"), dict):
        summary: Dict[str, dict] = {}
        for model_name, folds in data["cv_reports"].items():
            rep_dicts = [fr.report if isinstance(fr, FoldReport) else fr for fr in folds]
            summary[model_name] = _aggregate_classification_reports(rep_dicts)
        return {"current": summary}

    # Combined regime + behavior metrics case:
    # results = {"regime": [...], "behavior": [...]}, where each inner list
    # contains pre-aggregated metric rows (as dicts). We flatten these into
    # a single rows list with a `family` tag.
    if "regime" in data and "behavior" in data:
        rows: list[dict] = []
        for fam in ("regime", "behavior"):
            for row in data.get(fam, []):
                r = dict(row)
                r["family"] = fam
                rows.append(r)
        return {"rows": rows}

    # Multi-horizon case
    out: Dict[int, dict] = {}
    for horizon, bundle in data.items():
        cv_reports = bundle.get("cv_reports", {})
        model_summaries: Dict[str, dict] = {}
        for model_name, folds in cv_reports.items():
            rep_dicts = [fr.report if isinstance(fr, FoldReport) else fr for fr in folds]
            model_summaries[model_name] = _aggregate_classification_reports(rep_dicts)
        out[horizon] = model_summaries

    return out


def make_behavior_labels(
    returns: pd.Series,
    horizon: int,
    up_threshold: float,
    down_threshold: float,
) -> pd.Series:
    """
    Label forward returns as 'up' / 'flat' / 'down' for a single asset.

    The label at time t is based on the return between t and t+horizon. The last
    `horizon` periods are dropped so that every label corresponds to a full
    forward window.
    """
    if horizon <= 0:
        raise ValueError(f"horizon must be positive, got {horizon}")

    fwd = returns.shift(-horizon)
    mask = fwd.notna()
    fwd = fwd[mask]

    # Start with all 'flat', then override up/down with strict inequalities.
    labels = pd.Series("flat", index=fwd.index, dtype=object)
    labels[fwd > up_threshold] = "up"
    labels[fwd < down_threshold] = "down"

    return labels


def train_forward_behavior_models(
    features: pd.DataFrame,
    regimes: pd.Series,
    returns: pd.DataFrame,
    horizons: List[int],
    cv_splits: int = 3,
) -> Dict[str, Dict[int, RandomForestClassifier]]:
    """
    Train per-asset, per-horizon behavior classifiers using features + regimes.

    For each asset column in `returns` and each horizon in `horizons`, this
    function:
      - Builds behavior labels via make_behavior_labels()
      - Intersects indices of features / regimes / labels
      - Trains a RandomForestClassifier on [features, regime] → behavior_label

    Returns:
        {
          "models": {asset: {h: RandomForestClassifier, ...}, ...},
          "cv_reports": {}   # reserved for future extension
        }
    """
    if features.empty:
        raise ValueError("features must be non-empty")
    if not horizons:
        raise ValueError("horizons must be a non-empty list of integers")

    models: Dict[str, Dict[int, RandomForestClassifier]] = {}

    for asset in returns.columns:
        asset_models: Dict[int, RandomForestClassifier] = {}
        for h in horizons:
            if h <= 0:
                raise ValueError(f"horizon must be positive, got {h}")

            labels = make_behavior_labels(
                returns[asset],
                horizon=h,
                up_threshold=0.0,
                down_threshold=0.0,
            )
            idx_joint = (
                labels.index.intersection(features.index).intersection(regimes.index)
            )
            if idx_joint.empty:
                continue

            X_joint = features.loc[idx_joint].copy()
            X_joint["regime"] = regimes.loc[idx_joint].astype(int)
            y_joint = labels.loc[idx_joint]

            clf = RandomForestClassifier(
                max_depth=8,
                n_estimators=100,
                random_state=42,
                n_jobs=-1,
                class_weight="balanced",
            )
            clf.fit(X_joint, y_joint)
            asset_models[h] = clf

        if asset_models:
            models[asset] = asset_models

    return {
        "models": models,
        "cv_reports": {},
    }

