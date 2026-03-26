"""
Pipeline step 8 — Diagnostics (ratios + RRG-style rotation view).

This step is intentionally conservative: it only reads existing checkpoints
and ETF prices to compute diagnostic artifacts. It does not alter regimes,
features, or recommendations.

RRG-style output places each ETF vs a benchmark in momentum/value space — common in relative-rotation analysis.

Run:
    python pipelines/08_diagnostics.py
"""

# No mutation of training data — pure reporting layer on top of cached prices.

from __future__ import annotations

import logging
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import trading_crab_lib as crab

DATA_DIR = crab.DATA_DIR
OUTPUT_DIR = crab.OUTPUT_DIR
load = crab.load
setup_logging = crab.setup_logging
RunConfig = crab.RunConfig
plotting = crab.plotting

from trading_crab_lib.diagnostics import compute_ratios_diagnostics, rrg_for_benchmark  # noqa: E402

log = logging.getLogger(__name__)


def _load_etf_prices(cfg: dict) -> pd.DataFrame:
    """Load ETF price history from the existing checkpoint (no network)."""
    prices_path = DATA_DIR / "raw" / "asset_prices.parquet"
    if not prices_path.exists():
        log.warning("ETF prices checkpoint not found at %s", prices_path)
        return pd.DataFrame()
    prices = pd.read_parquet(prices_path)
    tickers = cfg.get("assets", {}).get("etfs") or list(prices.columns)
    cols = [t for t in tickers if t in prices.columns]
    if not cols:
        return pd.DataFrame()
    return prices[cols]


def main() -> None:
    setup_logging()
    cfg = load()
    run_cfg = RunConfig(generate_plots=True, save_plots=True)

    prices = _load_etf_prices(cfg)
    if prices.empty:
        print("No ETF prices available for diagnostics; skipping step 8.")
        return

    diag_dir = OUTPUT_DIR / "reports" / "diagnostics"
    diag_dir.mkdir(parents=True, exist_ok=True)

    ratios_df = compute_ratios_diagnostics(prices, cfg)
    if not ratios_df.empty:
        out_ratios = diag_dir / "ratios_current.parquet"
        ratios_df.to_parquet(out_ratios, index=False)
        print(f"Wrote ratio diagnostics → {out_ratios}")

    diag = cfg.get("diagnostics") or {}
    lookback = int(diag.get("rrg_lookback") or 52)
    benchmarks = diag.get("rrg_benchmarks") or ["SPY"]
    all_rrg: list[pd.DataFrame] = []
    for bench in benchmarks:
        df_b = rrg_for_benchmark(prices, bench, lookback=lookback)
        if not df_b.empty:
            all_rrg.append(df_b)
    rrg_combined = pd.concat(all_rrg, ignore_index=True) if all_rrg else pd.DataFrame()
    if not rrg_combined.empty:
        out_rrg = diag_dir / "rrg_current.parquet"
        rrg_combined.to_parquet(out_rrg, index=False)
        print(f"Wrote RRG diagnostics → {out_rrg}")

    if run_cfg.generate_plots:
        plotting.plot_diagnostics_ratios_summary(ratios_df, run_cfg)
        plotting.plot_diagnostics_rrg(rrg_combined, run_cfg)


if __name__ == "__main__":
    main()
