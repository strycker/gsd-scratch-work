"""
Pipeline step 7 — Stoplight Dashboard + Portfolio Recommendations

Loads all previously computed artifacts and prints a concise summary:
  - Current predicted regime
  - Asset stoplight signals (GREEN / YELLOW / RED)
  - Forward transition probabilities
  - Portfolio weights (simple + blended)
  - BUY / SELL / HOLD trade recommendations vs all-cash baseline

Features are read from features_supervised.parquet (causal/backward rolling
windows — consistent with how the model was trained in step 5).

Saves to outputs/reports/:
  dashboard.csv              — asset signals
  portfolio_simple.csv       — equal-weight top-3 assets for current regime
  portfolio_blended.csv      — probability-weighted allocation across all regimes
  trade_recommendations.csv  — BUY/SELL/HOLD vs current portfolio (config/portfolio.yaml)
  recommendation_bundle.parquet — Phase 5: regime, probs, digest (holdings + strong green), top/bottom 5
  weekly_report.md           — Phase 5: regime summary, BUY/SELL bullets, risk/transition note

Run:
    python pipelines/07_dashboard.py
"""

import sys
import pickle
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import trading_crab_lib as crab

DATA_DIR = crab.DATA_DIR
CONFIG_DIR = crab.CONFIG_DIR
OUTPUT_DIR = crab.OUTPUT_DIR
load = crab.load
load_portfolio = crab.load_portfolio
setup_logging = crab.setup_logging

from trading_crab_lib.prediction import predict_current
from trading_crab_lib.asset_returns import rank_assets_by_regime
from trading_crab_lib.reporting import (
    asset_signals,
    print_dashboard,
    save_dashboard_csv,
    simple_regime_portfolio,
    blended_regime_portfolio,
    generate_recommendation,
    build_recommendation_digest,
    save_recommendation_bundle,
    write_weekly_report_md,
)

import pandas as pd
import yaml


def load_regime_names() -> dict[int, str]:
    """
    Hybrid naming governance:
    - Start from auto-suggested names written by step 4
    - Overlay any pinned IDs from config/regime_labels.yaml

    This ensures that IDs intentionally left unpinned still get human-readable
    names instead of falling back to `Unknown`.
    """
    suggested_path = DATA_DIR / "regimes" / "regime_names_suggested.yaml"
    overrides_path = CONFIG_DIR / "regime_labels.yaml"

    suggested: dict[int, str] = {}
    if suggested_path.exists():
        with open(suggested_path) as f:
            raw = yaml.safe_load(f) or {}
        suggested = {int(k): v for k, v in raw.items() if not str(k).startswith("#")}

    overrides: dict[int, str] = {}
    if overrides_path.exists():
        with open(overrides_path) as f:
            raw = yaml.safe_load(f) or {}
        overrides = {int(k): v for k, v in raw.items() if not str(k).startswith("#")}

    return {**suggested, **overrides}


def main() -> None:
    setup_logging()
    cfg = load()

    # Load current-regime model
    model_dir = OUTPUT_DIR / "models"
    with open(model_dir / "current_regime.pkl", "rb") as f:
        current_model = pickle.load(f)

    # Use causal features for live scoring — same as training in step 5
    sup_path = DATA_DIR / "processed" / "features_supervised.parquet"
    feat_path = sup_path if sup_path.exists() else DATA_DIR / "processed" / "features.parquet"
    if not sup_path.exists():
        print(
            "WARNING: features_supervised.parquet not found — falling back to features.parquet.\n"
            "Re-run step 2 to generate causal features."
        )
    features = pd.read_parquet(feat_path)
    X = features.drop(columns=["market_code"], errors="ignore")
    if hasattr(current_model, "feature_names_in_"):
        X = X[current_model.feature_names_in_]
    else:
        X = X.dropna(axis=1, how="any")
    prediction = predict_current(current_model, X)

    # Load supporting data
    tm = pd.read_parquet(DATA_DIR / "regimes" / "transition_matrix.parquet")
    regime_names = load_regime_names()
    thresholds = cfg.get("dashboard", {}).get("signal_thresholds", None)

    # ── Asset signals ──────────────────────────────────────────────────────
    asset_signals_df = pd.DataFrame()
    profile_path = DATA_DIR / "regimes" / "asset_return_profile.parquet"
    profile: pd.DataFrame | None = None
    if profile_path.exists():
        profile = pd.read_parquet(profile_path)
        ranked = rank_assets_by_regime(profile)
        asset_signals_df = asset_signals(ranked, prediction["regime"], thresholds=thresholds)

    print_dashboard(prediction, regime_names, asset_signals_df, tm)

    report_dir = OUTPUT_DIR / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    if not asset_signals_df.empty:
        save_dashboard_csv(asset_signals_df, report_dir)

    # ── Portfolio construction ─────────────────────────────────────────────
    if profile is not None and not profile.empty:
        current_regime = prediction["regime"]
        probs = prediction["probabilities"]
        rec_threshold = cfg.get("dashboard", {}).get("recommendation_threshold", 0.03)

        simple_weights = simple_regime_portfolio(profile, current_regime, top_n=3)
        blended_weights = blended_regime_portfolio(profile, probs, top_n=3)

        # Phase 5: current portfolio from config/portfolio.yaml
        portfolio_weights = load_portfolio()
        current_weights = pd.Series(portfolio_weights) if portfolio_weights else None
        recommendations = generate_recommendation(
            blended_weights, current_weights=current_weights, threshold=rec_threshold
        )

        print("\n── Simple portfolio (top-3 for current regime) ──")
        for asset, w in simple_weights.items():
            print(f"  {asset:<12s}  {w:.1%}")

        print("\n── Blended portfolio (probability-weighted) ──")
        for asset, w in blended_weights.items():
            print(f"  {asset:<12s}  {w:.1%}")

        print("\n── Trade recommendations (blended vs current portfolio, %.0f%% threshold) ──" % (rec_threshold * 100))
        print(recommendations.to_string())

        if not simple_weights.empty:
            simple_weights.to_frame("weight").to_csv(report_dir / "portfolio_simple.csv")
        if not blended_weights.empty:
            blended_weights.to_frame("weight").to_csv(report_dir / "portfolio_blended.csv")
        if not recommendations.empty:
            recommendations.to_csv(report_dir / "trade_recommendations.csv")

        # Phase 5: recommendation bundle (holdings + strong green) + weekly report
        behavior_path = DATA_DIR / "regimes" / "etf_behavior_by_regime.parquet"
        if behavior_path.exists():
            behavior_df = pd.read_parquet(behavior_path)
            digest = build_recommendation_digest(
                behavior_df, current_regime, current_weights, blended_weights,
                recommendations if not recommendations.empty else pd.DataFrame(),
                top_n=5,
            )
            if not digest.empty:
                save_recommendation_bundle(
                    digest,
                    current_regime,
                    regime_names.get(current_regime, "Unknown"),
                    probs,
                    report_dir / "recommendation_bundle.parquet",
                )
        # Weekly report: always write when we have prediction + recommendations
        write_weekly_report_md(
            current_regime,
            regime_names.get(current_regime, "Unknown"),
            probs,
            recommendations,
            tm.loc[current_regime] if current_regime in tm.index else None,
            report_dir / "weekly_report.md",
        )
        print(f"\nReports saved to {report_dir}")


if __name__ == "__main__":
    main()
