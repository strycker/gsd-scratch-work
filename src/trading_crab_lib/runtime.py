"""
RunConfig — global runtime flags for the pipeline.

Mirrors the top-of-script flags in ``legacy/unified_script.py`` (verbose, plot
generation, refresh/recompute, optional pairplot/scatter_matrix). Construct one
:class:`RunConfig` at the entry point (``run_pipeline.py`` or a pipeline script)
and pass it through so behavior stays consistent and testable.

**Why a dataclass:** CLI flags and notebook parameters map 1:1 to fields;
:meth:`RunConfig.from_args` binds :mod:`argparse` without ad-hoc globals.
"""

# Financial modeling: "refresh" vs "recompute" separates expensive network I/O
# (scraping macro sites) from CPU-only recomputation from cached raw parquet.

from __future__ import annotations

import logging
from dataclasses import dataclass


@dataclass
class RunConfig:
    # ── verbosity ─────────────────────────────────────────────────────────
    verbose: bool = False  # DEBUG logging if True

    # ── plotting ──────────────────────────────────────────────────────────
    generate_plots: bool = False  # produce matplotlib figures
    generate_pairplot: bool = False  # seaborn pairplot (slow, optional)
    generate_scatter_matrix: bool = False  # pandas scatter_matrix (slow, optional)
    save_plots: bool = True  # write PNGs to outputs/plots/
    show_plots: bool = False  # plt.show() — False for headless/CI

    # ── data refresh ──────────────────────────────────────────────────────
    refresh_source_datasets: bool = False  # re-scrape multpl + re-hit FRED
    recompute_derived_datasets: bool = False  # recompute features from cached raw
    refresh_asset_prices: bool = False  # re-fetch yfinance ETF prices (step 6)

    # ── misc ──────────────────────────────────────────────────────────────
    use_constrained_kmeans: bool = True  # attempt k-means-constrained

    # Step 5 leakage guardrail (supervised learning):
    # Centered (non-causal) features use future quarters in smoothing windows — fine
    # for clustering, invalid for "what would we have known at quarter-end" prediction.
    # - default: require features_supervised.parquet (causal features)
    # - opt-in : allow fallback to features.parquet (non-causal), with a loud warning
    allow_noncausal_features: bool = False

    # Overwrite preservation secondaries (macro_raw_secondary, features_secondary, …)
    # even if they already exist. Default: only create/update when missing or when
    # --refresh / --recompute would update the corresponding primary checkpoint.
    refresh_preservation_checkpoints: bool = False

    # Drop trailing quarters with NaN features before training / predicting.
    # Mirrors config setting data.drop_incomplete_tail (CLI: --no-drop-tail).
    # The most-recent quarter typically has NaN in derivative columns because
    # centered np.gradient cannot compute edge values; removing it is safer
    # than forward-filling or column-dropping.
    drop_incomplete_tail: bool = True

    # ── market_code ───────────────────────────────────────────────────────
    # market_code: optional *overlay* regime label per quarter for comparison plots
    # or alternate training labels — not the same as cluster IDs from step 3 unless
    # you saved balanced_cluster via --save-market-code.
    # Special value "grok"       → load from grok pickle via ingestion/grok.py
    # Any other string "foo"     → load checkpoint named "market_code_foo"
    # None                       → no market_code (fully data-driven)
    market_code_source: str | None = None

    @classmethod
    def from_args(cls, args) -> RunConfig:
        """Build a :class:`RunConfig` from a parsed :class:`argparse.Namespace`.

        Args:
            args: Namespace from ``run_pipeline.py`` (``dest`` names match field names).

        Returns:
            Populated :class:`RunConfig` instance.
        """
        return cls(
            verbose=getattr(args, "verbose", False),
            generate_plots=getattr(args, "plots", False),
            generate_pairplot=getattr(args, "pairplot", False),
            generate_scatter_matrix=getattr(args, "scatter_matrix", False),
            save_plots=not getattr(args, "no_save_plots", False),
            show_plots=getattr(args, "show_plots", False),
            refresh_source_datasets=getattr(args, "refresh", False),
            recompute_derived_datasets=getattr(args, "recompute", False),
            refresh_asset_prices=getattr(args, "refresh_assets", False),
            use_constrained_kmeans=not getattr(args, "no_constrained", False),
            allow_noncausal_features=getattr(args, "allow_noncausal_features", False),
            market_code_source=getattr(args, "market_code", None),
            drop_incomplete_tail=not getattr(args, "no_drop_tail", False),
            refresh_preservation_checkpoints=getattr(args, "refresh_preservation", False),
        )

    def apply_logging(self) -> None:
        """Set root logger to DEBUG if verbose, else leave at INFO."""
        if self.verbose:
            logging.getLogger().setLevel(logging.DEBUG)

    def __str__(self) -> str:
        flags = []
        if self.verbose:
            flags.append("verbose")
        if self.generate_plots:
            flags.append("plots")
        if self.generate_pairplot:
            flags.append("pairplot")
        if self.refresh_source_datasets:
            flags.append("refresh")
        if self.recompute_derived_datasets:
            flags.append("recompute")
        if self.refresh_asset_prices:
            flags.append("refresh-assets")
        if self.allow_noncausal_features:
            flags.append("allow-noncausal-features")
        if self.refresh_preservation_checkpoints:
            flags.append("refresh-preservation")
        if self.market_code_source:
            flags.append(f"market_code={self.market_code_source}")
        return f"RunConfig({', '.join(flags) or 'defaults'})"
