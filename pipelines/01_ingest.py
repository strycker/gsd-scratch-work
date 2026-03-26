"""
Pipeline step 1 — Data Ingestion (checkpointed)

Thin wrapper around the main pipeline's step-1 ingestion, so that:
- Macro and ETF ingestion are fully config-driven.
- Checkpoints are managed by CheckpointManager.
- Behaviour and logging match `run_pipeline.py --steps 1`.

Run:
    python pipelines/01_ingest.py
    python pipelines/01_ingest.py --refresh
"""

# Step 1 builds the *wide* quarterly macro table + ETF prices. Everything downstream
# assumes a common DatetimeIndex (quarter-end) and honest publication timing on FRED.
#
# Economist view: this step assembles a panel of macro and market state variables
# (growth, inflation, rates, credit, equity valuation) at the same quarterly frequency.
# ETF prices are cached here so step 6 does not re-hit Yahoo unless --refresh-assets.

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running from repo root without installing the package
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import trading_crab_lib as crab

setup_logging = crab.setup_logging
RunConfig = crab.RunConfig
load = crab.load
from run_pipeline import step1_ingest  # reuse the canonical step implementation


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Trading-Crab step 1 — data ingestion (FRED + multpl, with checkpoints)",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Re-scrape multpl.com + re-hit FRED API instead of using fresh checkpoints.",
    )
    parser.add_argument(
        "--plots",
        action="store_true",
        help="Generate and save ingestion QC plots.",
    )
    parser.add_argument(
        "--show-plots",
        action="store_true",
        help="Call plt.show() after each figure (avoid in headless/CI).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Set logging level to DEBUG for this step.",
    )
    parser.add_argument(
        "--market-code",
        type=str,
        default=None,
        metavar="NAME",
        help=(
            "Attach a market_code column using the same semantics as run_pipeline.py: "
            "'grok' loads the Grok pickle; any other value loads checkpoint "
            "'market_code_{NAME}'. Omit to run without market_code."
        ),
    )
    parser.add_argument(
        "--no-drop-tail",
        action="store_true",
        help=(
            "Include the most-recent (potentially incomplete) quarter instead of "
            "dropping it when it contains NaN in any feature column."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    setup_logging()
    run_cfg = RunConfig.from_args(args)
    run_cfg.apply_logging()

    cfg = load()
    step1_ingest(cfg, run_cfg)


if __name__ == "__main__":
    main()
