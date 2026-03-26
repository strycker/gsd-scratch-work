"""
Pipeline step 2 — Feature Engineering

Thin wrapper around run_pipeline.step2_features so there is a single source
of truth for how features are engineered and checkpointed.

Run:
    python pipelines/02_features.py
"""

# Writes two parquets: centered features (clustering) and causal features (ML).
# Centered smoothing uses past and future quarters — valid for unsupervised history, not for live trading features.
# Causal smoothing uses only past quarters in rolling windows — required so step 5/7 match information available at quarter-end.

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import trading_crab_lib as crab

load = crab.load
setup_logging = crab.setup_logging
RunConfig = crab.RunConfig

from run_pipeline import step2_features


def main() -> None:
    """Entry point for standalone step-02 execution."""
    setup_logging()
    cfg = load()

    # For a direct step-02 run we always recompute features from the latest
    # macro_raw checkpoint and skip plotting. Other flags use RunConfig defaults.
    run_cfg = RunConfig(
        recompute_derived_datasets=True,
        generate_plots=False,
    )

    step2_features(cfg, run_cfg)


if __name__ == "__main__":
    main()
