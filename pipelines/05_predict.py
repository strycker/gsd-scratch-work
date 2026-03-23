"""
Pipeline step 5 — Supervised Regime Prediction

Trains:
  1. RandomForestClassifier  — high accuracy; used for production predictions.
  2. DecisionTreeClassifier  — shallow (max_depth=8); human-readable rules and
                               fast feature-importance inspection.
  3. Forward-looking binary classifiers for each regime × horizon pair.

All models use TimeSeriesSplit walk-forward cross-validation so CV accuracy
estimates reflect genuine out-of-sample performance.

Features are read from features_supervised.parquet (causal/backward rolling
windows — no future data leaks into any feature value).

Saves fitted models to outputs/models/.

Run:
    python pipelines/05_predict.py
"""

import argparse
import sys
import pickle
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import numpy as np
import pandas as pd

import trading_crab_lib as crab

DATA_DIR = crab.DATA_DIR
OUTPUT_DIR = crab.OUTPUT_DIR
load = crab.load
setup_logging = crab.setup_logging

from sklearn.tree import export_text

from trading_crab_lib.prediction.classifier import (
    train_current_regime,
    train_forward_classifiers,
    train_forward_behavior_models,
    train_interpretability_tree,
)
from trading_crab_lib.prediction.feature_gating import select_step5_feature_path
from trading_crab_lib.prediction.model_metrics_artifacts import write_model_metrics_artifacts
from trading_crab_lib.asset_returns import compute_proxy_returns, compute_quarterly_returns
from trading_crab_lib.transforms import trim_incomplete_tail


def main() -> None:
    parser = argparse.ArgumentParser(description="Step 5 — supervised regime + behavior prediction")
    parser.add_argument(
        "--allow-noncausal-features",
        action="store_true",
        help="Allow falling back to data/processed/features.parquet when features_supervised.parquet is missing.",
    )
    args = parser.parse_args()

    setup_logging()
    cfg = load()

    feature_path, feature_source, noncausal_used = select_step5_feature_path(
        DATA_DIR / "processed",
        allow_noncausal_features=args.allow_noncausal_features,
    )

    features = pd.read_parquet(feature_path)
    labels = pd.read_parquet(DATA_DIR / "regimes" / "cluster_labels.parquet")["balanced_cluster"]

    common = features.index.intersection(labels.index)
    drop_tail: bool = cfg.get("data", {}).get("drop_incomplete_tail", True)
    X_raw = features.loc[common].drop(columns=["market_code"], errors="ignore")
    # trim_incomplete_tail removes the trailing quarter(s) where centered
    # np.gradient leaves NaN in derivative columns (edge effect).
    # dropna(axis=0) removes any remaining rows with interior NaN.
    X = trim_incomplete_tail(X_raw, enabled=drop_tail).dropna(axis=0, how="any")
    y = labels.loc[X.index]

    cv_splits = cfg.get("prediction", {}).get("cv_splits", 5)
    current_bundle = train_current_regime(X, y, cfg, cv_splits=cv_splits)

    models = current_bundle["models"]

    # Use the RandomForest as the primary production model.
    rf = models["rf"]
    dt_model = models["dt"]
    latest_X = X.iloc[[-1]]
    proba = rf.predict_proba(latest_X)[0]
    classes = rf.classes_

    # Map class → probability and pick argmax as current regime.
    prob_by_class = dict(zip(classes, proba))
    best_regime = max(prob_by_class.items(), key=lambda kv: kv[1])[0]

    print(f"\nLatest quarter prediction: regime {best_regime}")
    for r, p in sorted(prob_by_class.items(), key=lambda x: -x[1]):
        print(f"  Regime {r}: {p:.1%}")

    horizons = cfg.get("prediction", {}).get("forward_horizons_quarters", [1, 2, 4, 8])
    forward_models = train_forward_classifiers(
        X, y, horizons=horizons, cfg=cfg, cv_splits=cv_splits
    )

    # ── Behavior models (per-asset up/flat/down) ─────────────────────────
    behavior_horizons = cfg.get("prediction", {}).get("behavior_horizons_quarters", [1])

    asset_prices_path = DATA_DIR / "raw" / "asset_prices.parquet"
    macro_raw_path = DATA_DIR / "raw" / "macro_raw.parquet"

    returns = None
    if asset_prices_path.exists():
        prices = pd.read_parquet(asset_prices_path)
        if not prices.empty:
            returns = compute_quarterly_returns(prices)

    if returns is None or returns.empty:
        if not macro_raw_path.exists():
            raise FileNotFoundError(
                "Step 5 behavior models require returns input.\n"
                f"Neither {asset_prices_path} nor {macro_raw_path} was found."
            )
        macro_df = pd.read_parquet(macro_raw_path)
        returns = compute_proxy_returns(macro_df)

    common_ret = returns.index.intersection(X.index)
    returns_aligned = returns.loc[common_ret]

    behavior_bundle = train_forward_behavior_models(
        X,
        y,
        returns_aligned,
        horizons=behavior_horizons,
        cv_splits=cv_splits,
    )

    # ── Persist models ────────────────────────────────────────────────────
    model_dir = OUTPUT_DIR / "models"
    model_dir.mkdir(parents=True, exist_ok=True)

    with open(model_dir / "current_regime.pkl", "wb") as f:
        pickle.dump(rf, f)
    with open(model_dir / "decision_tree.pkl", "wb") as f:
        pickle.dump(dt_model, f)
    if "gb" in models:
        with open(model_dir / "current_regime_gb.pkl", "wb") as f:
            pickle.dump(models["gb"], f)
    with open(model_dir / "forward_classifiers.pkl", "wb") as f:
        pickle.dump(forward_models, f)
    with open(model_dir / "behavior_models.pkl", "wb") as f:
        pickle.dump(behavior_bundle, f)

    # ── Metrics artifacts (MODEL-04) ─────────────────────────────────────
    metrics_dir = OUTPUT_DIR / "reports" / "model_metrics"
    write_model_metrics_artifacts(
        output_dir=metrics_dir,
        feature_source=feature_source,
        noncausal_used=noncausal_used,
        regime_current_bundle=current_bundle,
        forward_models=forward_models,
        behavior_bundle=behavior_bundle,
    )

    report_dir = OUTPUT_DIR / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    try:
        tree_model, tree_features = train_interpretability_tree(rf, X, y, cfg)
        (report_dir / "current_regime_tree.txt").write_text(
            export_text(tree_model, feature_names=tree_features), encoding="utf-8"
        )
    except Exception:
        pass
    if "gb" in models and cfg.get("prediction", {}).get("interpret_tree_on_boosted", True):
        try:
            tree_gb, tree_features_gb = train_interpretability_tree(models["gb"], X, y, cfg)
            (report_dir / "current_regime_tree_gb.txt").write_text(
                export_text(tree_gb, feature_names=tree_features_gb), encoding="utf-8"
            )
        except Exception:
            pass

    print(f"\nModels saved to {model_dir}")


if __name__ == "__main__":
    main()
