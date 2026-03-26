"""
Pipeline step 6 — Asset Returns by Regime

Fetches ETF price history via yfinance (SPY, GLD, TLT, USO, QQQ, IWM, VNQ, AGG),
computes quarterly returns, and profiles median return per regime.

Fallback: when yfinance is unavailable (SSL failure, network outage, or no cached
prices), derives proxy returns directly from macro columns already present in
data/raw/macro_raw.parquet (sp500, sp500_adj, 10yr_ustreas, gdp_growth, us_infl,
credit_spread).  Coverage extends back to ~1950, so every historical regime is
represented even without ETF data.

Priority order:
  1. yfinance (real ETF data — most accurate for recent periods)
     Only used when --refresh-assets is passed OR no cache exists.
  2. Cached asset_prices.parquet (if yfinance is temporarily unavailable)
  3. Macro-data proxy returns (fallback for SSL/network failures or back-history)

SSL note:
  Behind a corporate firewall with HTTPS inspection?  See the message printed
  by fetch_all() for remediation steps.  The simplest workaround:
    export CURL_CA_BUNDLE=""
    export REQUESTS_CA_BUNDLE=""
  Or run without --refresh-assets to skip yfinance and use the checkpoint.

Writes data/regimes/asset_return_profile.parquet

Run:
    python pipelines/06_asset_returns.py                  # use cache if available
    python pipelines/06_asset_returns.py --refresh-assets  # force re-fetch yfinance
"""

# Answers: "which ETFs did well in which regime historically?" — inputs to portfolio UX.
# Medians summarize typical experience; hit_rate flags how often returns were positive — risk-aware reporting uses full stats when needed.

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import trading_crab_lib as crab

DATA_DIR = crab.DATA_DIR
load = crab.load
setup_logging = crab.setup_logging

import pandas as pd

from trading_crab_lib.asset_returns import (
    behavior_tables,
    compute_proxy_returns,
    compute_quarterly_returns,
    compute_template_returns,
    rank_assets_by_regime,
    returns_by_regime,
)

log = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Step 6 — Asset returns by regime")
    parser.add_argument(
        "--refresh-assets",
        action="store_true",
        help=(
            "Force re-fetch ETF prices from yfinance even if a cached "
            "data/raw/asset_prices.parquet already exists.  "
            "Without this flag, the cached file is used (useful when behind a firewall)."
        ),
    )
    args = parser.parse_args()
    refresh_assets: bool = args.refresh_assets

    setup_logging()
    cfg = load()

    labels = pd.read_parquet(DATA_DIR / "regimes" / "cluster_labels.parquet")["balanced_cluster"]

    from trading_crab_lib.checkpoints import CheckpointManager
    from trading_crab_lib.ingestion.assets import load_or_fetch_quarterly_prices

    cm = CheckpointManager()
    ttl = float(cfg.get("data", {}).get("checkpoint_max_age_days", 7))
    prices = load_or_fetch_quarterly_prices(
        cfg,
        data_dir=DATA_DIR,
        refresh=refresh_assets,
        cm=cm,
        max_age_days=ttl,
    )
    if prices is not None and not prices.empty:
        print(f"ETF prices ready: {prices.shape} (use --refresh-assets to re-fetch)")

    # ── 3. Compute returns ─────────────────────────────────────────────────────
    returns: pd.DataFrame | None = None
    if prices is not None and not prices.empty:
        returns = compute_quarterly_returns(prices)
        print(f"ETF quarterly returns: {returns.shape}")
    else:
        print("No ETF price data — computing proxy returns from macro data …")
        macro_path = DATA_DIR / "raw" / "macro_raw.parquet"
        if macro_path.exists():
            macro_df = pd.read_parquet(macro_path)
            returns = compute_proxy_returns(macro_df)
            if returns.empty:
                print("Proxy returns also empty — skipping step 6.")
                return
            print(f"Proxy returns: {returns.shape}")
        else:
            print(f"macro_raw.parquet not found at {macro_path} — skipping step 6.")
            return

    common = returns.index.intersection(labels.index)
    returns_aligned = returns.loc[common]
    labels_aligned = labels.loc[common]
    profile = returns_by_regime(returns_aligned, labels_aligned)
    ranked = rank_assets_by_regime(profile)

    out_dir = DATA_DIR / "regimes"
    out_dir.mkdir(parents=True, exist_ok=True)
    profile.to_parquet(out_dir / "asset_return_profile.parquet")
    print(f"Wrote asset return profile → {out_dir / 'asset_return_profile.parquet'}")

    # Phase 4: behavior tables (median, IQR, stoplights, scores) for ETFs
    behavior_thresholds = cfg.get("dashboard", {}).get("behavior_thresholds") or {}
    etf_behavior = behavior_tables(returns_aligned, labels_aligned, thresholds=behavior_thresholds)
    etf_behavior.to_parquet(out_dir / "etf_behavior_by_regime.parquet", index=False)
    print(f"Wrote ETF behavior by regime → {out_dir / 'etf_behavior_by_regime.parquet'}")

    # Phase 4: template returns and behavior (if config has portfolio_templates)
    templates = cfg.get("assets", {}).get("portfolio_templates") or []
    if templates:
        template_returns = compute_template_returns(returns_aligned, templates)
        if not template_returns.empty:
            template_behavior = behavior_tables(
                template_returns, labels_aligned, thresholds=behavior_thresholds
            )
            template_behavior.to_parquet(
                out_dir / "template_behavior_by_regime.parquet", index=False
            )
            print(
                f"Wrote template behavior by regime → {out_dir / 'template_behavior_by_regime.parquet'}"
            )

    print("\nTop assets per regime (by median quarterly return):")
    print(ranked.to_string(index=False))


if __name__ == "__main__":
    main()
