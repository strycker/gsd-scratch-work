"""
Pipeline step 9 — Tactics layer (buy-and-hold / swing-trade / stand-aside).

Reads ETF prices and regime labels, computes per-asset volatility/trend/
correlation metrics, classifies tactics labels, and writes a machine-readable
parquet for the weekly report and downstream use.

Run:
    python pipelines/09_tactics.py
"""

from __future__ import annotations

import logging

import pandas as pd

import trading_crab_lib as crab

DATA_DIR = crab.DATA_DIR
OUTPUT_DIR = crab.OUTPUT_DIR
load = crab.load
setup_logging = crab.setup_logging

from trading_crab_lib.tactics import classify_tactics, compute_tactics_metrics

log = logging.getLogger(__name__)


def main() -> None:
    setup_logging()
    cfg = load()

    prices_path = DATA_DIR / "raw" / "asset_prices.parquet"
    labels_path = DATA_DIR / "regimes" / "cluster_labels.parquet"

    if not prices_path.exists():
        log.warning("ETF prices checkpoint %s not found; skipping tactics step.", prices_path)
        return
    if not labels_path.exists():
        log.warning("Cluster labels %s not found; skipping tactics step.", labels_path)
        return

    prices = pd.read_parquet(prices_path)
    labels = pd.read_parquet(labels_path)["balanced_cluster"]

    metrics = compute_tactics_metrics(prices, labels, cfg)
    tactics_df = classify_tactics(metrics, cfg).reset_index()

    out_dir = OUTPUT_DIR / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "tactics_signals.parquet"
    tactics_df.to_parquet(out_path, index=False)
    print(f"Wrote tactics signals → {out_path}")


if __name__ == "__main__":
    main()
