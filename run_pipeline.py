"""
run_pipeline.py — Master entry point for the Trading-Crab market regime pipeline.

Runs all 9 pipeline steps in order, or any selected subset, with a consistent
RunConfig passed through every module.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 PIPELINE STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1  ingest         Scrape multpl.com (46 series) + FRED API → macro_raw.parquet;
                     also loads ETF prices into ``data/raw/asset_prices.parquet``
                     (same cache step 6 uses unless ``--refresh-assets``).
  2  features       Log transforms, derivatives, gap-fill → features.parquet
  3  cluster        PCA + KMeans → cluster_labels.parquet
  4  regime_label   Statistical profiling + human-readable names → profiles.parquet
  5  predict        Supervised classifiers (current + forward horizons)
  6  asset_returns  ETF returns by regime via yfinance
  7  dashboard      Print dashboard + save outputs/reports/dashboard.csv
  8  diagnostics    Ratio + RRG diagnostics → outputs/reports/diagnostics/
  9  tactics        Per-asset tactics signals → tactics_signals.parquet

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 ALL CLI FLAGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  --refresh            Re-scrape multpl.com + re-hit FRED API (~10 min).
                       Without this flag, steps 1–2 load from cached checkpoints
                       if younger than ``data.checkpoint_max_age_days`` in
                       ``config/settings.yaml`` (default 7; raise to refresh less often).

  --recompute          Recompute derived features (step 2) from cached raw data.
                       Use after editing config/settings.yaml feature lists or
                       transforms.py without wanting to re-scrape.

  --refresh-assets     Re-fetch ETF prices from yfinance (step 6 only).
                       Without this flag, step 6 reuses data/raw/asset_prices.parquet
                       if it already exists. Useful when behind a firewall or when
                       ETF data hasn't changed since the last run.

  --plots              Generate and save matplotlib figures to outputs/plots/.
                       Each step produces its own set of charts.

  --show-plots         Also call plt.show() after each figure.
                       Off by default; do NOT use in CI or headless environments.

  --verbose            Set logging level to DEBUG (very chatty).

  --steps 1,3,5        Run only the listed step numbers (comma-separated integers).
                       Example: --steps 3,4,5,6,7 skips ingestion and features.
                       Valid values: 1 2 3 4 5 6 7 8 9

  --no-constrained     Skip the k-means-constrained package even if installed.
                       Falls back to plain KMeans for balanced clustering.
                       Use if you haven't run: pip install k-means-constrained

  --no-drop-tail       Include the most-recent (potentially incomplete) quarter.
                       By default the trailing row is dropped when it contains NaN
                       in any feature column — a side effect of the centered
                       np.gradient edge window in step 2.

  --market-code NAME   Inject a market_code label column into macro_raw so that
                       downstream models and notebooks can overlay regime labels.
                       NAME must be one of:
                         grok        Load the original Grok AI-generated labels
                                     from data/grok_*.pickle (cached automatically
                                     to market_code_grok checkpoint on first use)
                         clustered   Load labels saved by a prior --save-market-code
                                     run (checkpoint: market_code_clustered)
                         predicted   Load labels auto-saved by step 5 on its last
                                     run (checkpoint: market_code_predicted)
                         <any name>  Load checkpoint "market_code_<NAME>"
                       Omit entirely for a fully data-driven run with no label seed.

  --save-market-code   After step 3 completes, save the balanced_cluster column as
                       the "market_code_clustered" checkpoint.  Use this so future
                       runs can reference these cluster assignments with
                       --market-code clustered.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 AUTO-SAVED CHECKPOINTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Step 5 automatically saves the predicted current-regime labels as the
  "market_code_predicted" checkpoint every time it runs.  No flag needed.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 COMMON WORKFLOWS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 ① FRESH START — scrape everything, seed with Grok labels (recommended first run):
     python run_pipeline.py --refresh --recompute --plots \\
         --market-code grok --save-market-code

 ② FULLY DATA-DRIVEN — no label seed, cluster from data only:
     python run_pipeline.py --refresh --recompute --plots --save-market-code

 ③ FAST RE-RUN — skip scraping, use cached checkpoints, regenerate plots:
     python run_pipeline.py --steps 3,4,5,6,7 --plots

 ④ RE-CLUSTER ONLY — update cluster assignments, save for downstream:
     python run_pipeline.py --steps 3 --save-market-code --plots

 ⑤ DOWNSTREAM WITH NEW CLUSTER LABELS — use labels saved in ④:
     python run_pipeline.py --steps 4,5,6,7 --market-code clustered --plots

 ⑥ DOWNSTREAM WITH GROK SEED — overlay original AI labels:
     python run_pipeline.py --steps 4,5,6,7 --market-code grok --plots

 ⑦ DOWNSTREAM WITH PREDICTED LABELS — use last step-5 predictions:
     python run_pipeline.py --steps 4,5,6,7 --market-code predicted --plots

 ⑧ RECOMPUTE FEATURES WITHOUT RE-SCRAPING (e.g., after editing settings.yaml):
     python run_pipeline.py --recompute --steps 2,3,4,5,6,7 --plots

 ⑨ ETF DATA REFRESH ONLY (no macro re-scrape):
     python run_pipeline.py --steps 6,7 --refresh-assets --plots

 ⑩ DEBUG A SINGLE STEP:
     python run_pipeline.py --steps 3 --verbose --plots --show-plots

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 MARKET CODE EXPLAINED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  The "market_code" is a per-quarter integer label (0-4) that serves as the
  reference regime assignment.  It is attached to macro_raw in step 1 and
  propagated through all downstream steps as an overlay/reference column.

  Four sources are available:
    grok        Original AI-assisted labels (circa 2026-02-16).  Useful as a
                stable reference baseline — these never change.
    clustered   Labels from the most recent --save-market-code run.  Updated
                every time you run step 3 with --save-market-code.
    predicted   Labels from the most recent step 5 run.  Reflects the current
                trained classifier's best guess for historical quarters.
    (omitted)   Run without a market_code column.  Clustering is fully
                data-driven; no external label is injected.

  To list all available market_code checkpoints:
    python -c "
    from trading_crab_lib.io.checkpoints import CheckpointManager
    cm = CheckpointManager()
    mc = [e for e in cm.list() if e['name'].startswith('market_code_')]
    for e in mc: print(e['name'], '—', e.get('rows', '?'), 'rows')
    "
"""

from __future__ import annotations

import argparse
import logging
import shutil
import sys
from datetime import date
from pathlib import Path

# Allow running from repo root without `pip install -e .`
sys.path.insert(0, str(Path(__file__).parent / "src"))

import trading_crab_lib as crab

DATA_DIR = crab.DATA_DIR
OUTPUT_DIR = crab.OUTPUT_DIR
CONFIG_DIR = crab.CONFIG_DIR
load = crab.load
load_portfolio = crab.load_portfolio
setup_logging = crab.setup_logging
RunConfig = crab.RunConfig

from trading_crab_lib.email import (
    build_weekly_email_body,
    load_email_config,
    send_weekly_email,
)

log = logging.getLogger(__name__)


# ── I/O helpers ───────────────────────────────────────────────────────────────

def _load_parquet(canonical_path: Path, checkpoint_name: str) -> "pd.DataFrame":
    """
    Load a DataFrame from its canonical inter-step path, falling back to the
    CheckpointManager when the file doesn't exist.

    This lets steps 3-7 work even when the upstream step was run on a different
    machine and only its checkpoint was committed to the repo.
    """
    import pandas as pd
    from trading_crab_lib.checkpoints import CheckpointManager

    if canonical_path.exists():
        return pd.read_parquet(canonical_path)

    log.info(
        "%s not found — loading from checkpoint '%s'",
        canonical_path.name, checkpoint_name,
    )
    df = CheckpointManager().load(checkpoint_name)
    # Backfill the canonical file so subsequent reads are fast
    canonical_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(canonical_path)
    return df


def _repair_macro_raw_missing_columns(
    combined: "pd.DataFrame",
    required: set[str],
    cm: "CheckpointManager",
) -> tuple["pd.DataFrame", list[str]]:
    """
    When data/raw/macro_raw.parquet is missing columns (e.g. stale file vs checkpoint),
    copy any available series from the ``macro_raw`` checkpoint so step 2 can run
    without forcing a full --refresh ingest.
    """
    missing = sorted(required - set(combined.columns))
    if not missing:
        return combined, []
    try:
        ck = cm.load("macro_raw")
    except FileNotFoundError:
        return combined, []
    out = combined.copy()
    added: list[str] = []
    for col in missing:
        if col in ck.columns:
            out[col] = ck[col].reindex(out.index)
            added.append(col)
    return out, added


def _checkpoint_ttl_days(cfg: dict) -> float:
    """Max age for macro_raw / features / cluster_labels / asset_prices cache hits."""
    return float(cfg.get("data", {}).get("checkpoint_max_age_days", 7))


def _sync_etf_prices_cache(cfg: dict, run_cfg: RunConfig, cm: "CheckpointManager") -> None:
    """Fetch or reuse ETF prices during step 1 so later steps share one cache path."""
    from trading_crab_lib.ingestion.assets import load_or_fetch_quarterly_prices

    ttl = _checkpoint_ttl_days(cfg)
    prices = load_or_fetch_quarterly_prices(
        cfg,
        data_dir=DATA_DIR,
        refresh=run_cfg.refresh_asset_prices,
        cm=cm,
        max_age_days=ttl,
    )
    if prices is not None and not prices.empty:
        log.info(
            "Step 1: ETF price cache ready (%d quarters × %d tickers)",
            len(prices),
            len(prices.columns),
        )


# ── market_code helpers ───────────────────────────────────────────────────────

def _load_market_code(
    source: str,
    cfg: dict,
) -> "pd.Series | None":
    """
    Load a market_code Series from the specified source.

    Args:
        source: "grok" to load from the grok pickle, or any other string to
                load checkpoint "market_code_{source}".

    Returns:
        pd.Series of integer codes indexed by quarter-end dates, or None on failure.
    """
    import pandas as pd
    from trading_crab_lib.checkpoints import CheckpointManager

    cm = CheckpointManager()

    if source == "grok":
        from trading_crab_lib.ingestion.grok import load_grok_labels
        mc = load_grok_labels(DATA_DIR)
        if mc is not None:
            # Cache so subsequent runs don't need to reload the pickle
            cm.save(mc.to_frame(), "market_code_grok")
        return mc

    # Load from checkpoint
    ckpt_name = f"market_code_{source}"
    try:
        df = cm.load(ckpt_name)
        mc = df.iloc[:, 0]  # single-column DataFrame → Series
        mc.name = "market_code"
        log.info("Loaded market_code from checkpoint: %s (%d rows)", ckpt_name, len(mc))
        return mc
    except FileNotFoundError:
        log.error(
            "market_code checkpoint '%s' not found. "
            "Available checkpoints: %s",
            ckpt_name,
            [e["name"] for e in cm.list() if e["name"].startswith("market_code_")],
        )
        return None


def _save_market_code(labels: "pd.Series", name: str) -> None:
    """Persist a market_code variant (any integer-coded label Series) to a checkpoint."""
    from trading_crab_lib.checkpoints import CheckpointManager
    import pandas as pd

    cm = CheckpointManager()
    ckpt_name = f"market_code_{name}"
    df = labels.rename("market_code").to_frame()
    cm.save(df, ckpt_name)
    log.info("Saved market_code checkpoint: %s (%d rows)", ckpt_name, len(labels))


# ── Step registry ──────────────────────────────────────────────────────────────

def step1_ingest(cfg: dict, run_cfg: RunConfig) -> None:
    """Ingest macro + ETF prices → ``data/raw/``.

    Writes ``macro_raw.parquet`` (FRED + multpl) and ``asset_prices.parquet`` (or
    restores ETF data from checkpoint) so all network-heavy loading happens here.
    Optionally attaches ``market_code`` from the configured source."""
    from trading_crab_lib.ingestion import fred as fred_module
    from trading_crab_lib.ingestion import multpl as multpl_module
    from trading_crab_lib.ingestion.macro_partial import merge_missing_macro_columns
    from trading_crab_lib.checkpoints import CheckpointManager
    from trading_crab_lib import plotting
    import pandas as pd

    cm = CheckpointManager()
    ttl = _checkpoint_ttl_days(cfg)
    required_for_step2 = {
        # Needed by transforms.add_cross_ratios() (cross-asset ratios)
        "dividend",
        "sp500",
        "gdp",
        "fred_gdp",
        "fred_gnp",
        "div_yield",
        "fred_baa",
        "fred_aaa",
        "cpi",
        "fred_cpi",
        "sp500_adj",
    }

    raw_path = DATA_DIR / "raw" / "macro_raw.parquet"

    if (
        not run_cfg.refresh_source_datasets
        and cm.is_fresh("macro_raw", max_age_days=ttl, require_config_match=True)
        and raw_path.exists()
    ):
        combined = pd.read_parquet(raw_path)

        missing = sorted(required_for_step2 - set(combined.columns))
        repaired_cols: list[str] = []
        dirty = False
        if missing:
            combined, repaired_cols = _repair_macro_raw_missing_columns(
                combined, required_for_step2, cm
            )
            if repaired_cols:
                log.info(
                    "Step 1: restored %d macro_raw column(s) from checkpoint: %s",
                    len(repaired_cols),
                    repaired_cols,
                )
                dirty = True
            missing = sorted(required_for_step2 - set(combined.columns))

        if missing:
            log.info(
                "Step 1: cached macro_raw missing %d column(s); trying partial FRED/multpl merge: %s",
                len(missing),
                missing,
            )
            try:
                before = set(combined.columns)
                combined = merge_missing_macro_columns(combined, set(missing), cfg)
                if set(combined.columns) != before:
                    dirty = True
            except Exception as exc:
                log.warning("Step 1: partial macro ingest failed (%s)", exc)
            missing = sorted(required_for_step2 - set(combined.columns))

        if not missing:
            log.info("Step 1: using cached macro_raw checkpoint")
            if run_cfg.market_code_source:
                mc = _load_market_code(run_cfg.market_code_source, cfg)
                if mc is not None:
                    combined["market_code"] = mc.reindex(combined.index)
                    dirty = True
                    log.info(
                        "Step 1: refreshed market_code=%s in cached macro_raw",
                        run_cfg.market_code_source,
                    )
            if dirty:
                combined.to_parquet(raw_path)
                cm.save(combined, "macro_raw")
                log.info("Step 1: wrote updated macro_raw → %s", raw_path)
            _sync_etf_prices_cache(cfg, run_cfg, cm)
            return

        log.warning(
            "Step 1: macro_raw still missing required columns (%d) after partial merge — "
            "full FRED + multpl fetch. Missing: %s",
            len(missing),
            missing,
        )
    elif not raw_path.exists():
        log.info("Step 1: macro_raw.parquet missing — recomputing ingestion")

    log.info("Step 1: fetching FRED data …")
    fred_df = fred_module.fetch_all(cfg)

    log.info(
        "Step 1: scraping multpl.com (%d series) …",
        len(cfg["multpl"]["datasets"]),
    )
    multpl_df = multpl_module.fetch_all(cfg)

    combined = fred_df.join(multpl_df, how="outer") if not multpl_df.empty else fred_df
    start = cfg["data"]["start_date"]
    combined = combined[combined.index >= start]

    if run_cfg.market_code_source:
        mc = _load_market_code(run_cfg.market_code_source, cfg)
        if mc is not None:
            combined["market_code"] = mc.reindex(combined.index)
            log.info(
                "Step 1: attached market_code (%s), %d/%d rows have labels",
                run_cfg.market_code_source,
                combined["market_code"].notna().sum(),
                len(combined),
            )

    raw_dir = DATA_DIR / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    combined.to_parquet(raw_dir / "macro_raw.parquet")
    cm.save(combined, "macro_raw")

    _sync_etf_prices_cache(cfg, run_cfg, cm)

    if run_cfg.generate_plots:
        plotting.plot_raw_series_coverage(combined, run_cfg)
        sample_series = [
            c
            for c in [
                "sp500",
                "fred_gdp",
                "us_infl",
                "10yr_ustreas",
                "div_yield",
                "fred_baa",
            ]
            if c in combined.columns
        ]
        if sample_series:
            plotting.plot_raw_series_sample(combined, sample_series, run_cfg)

    log.info("Step 1 done: %d rows × %d cols", len(combined), len(combined.columns))


def step2_features(cfg: dict, run_cfg: RunConfig) -> None:
    """Engineer features from macro_raw → data/processed/features.parquet"""
    engineer_all = crab.transforms.engineer_all
    CheckpointManager = crab.checkpoints.CheckpointManager
    plotting = crab.plotting
    import pandas as pd

    cm = CheckpointManager()
    feats_path = DATA_DIR / "processed" / "features.parquet"
    sup_path = DATA_DIR / "processed" / "features_supervised.parquet"
    ttl = _checkpoint_ttl_days(cfg)

    if not run_cfg.recompute_derived_datasets and cm.is_fresh(
        "features", max_age_days=ttl, require_config_match=True
    ):
        have_files = feats_path.exists() and sup_path.exists()
        if not have_files:
            try:
                f_df = cm.load("features")
                fs_df = cm.load("features_supervised")
            except FileNotFoundError:
                f_df = fs_df = None
            if f_df is not None and fs_df is not None:
                feats_path.parent.mkdir(parents=True, exist_ok=True)
                f_df.to_parquet(feats_path)
                fs_df.to_parquet(sup_path)
                log.info(
                    "Step 2: materialized %s + %s from checkpoints",
                    feats_path.name,
                    sup_path.name,
                )
                have_files = True
        if have_files:
            log.info("Step 2: using cached features checkpoint")
            return

    raw = _load_parquet(DATA_DIR / "raw" / "macro_raw.parquet", "macro_raw")

    log.info("Step 2: engineering features from %d × %d raw data …",
             len(raw), len(raw.columns))

    # Centered features (forward + backward window) — used for clustering (steps 3-4)
    features = engineer_all(raw, cfg, causal=False)
    out_dir = DATA_DIR / "processed"
    out_dir.mkdir(parents=True, exist_ok=True)
    features.to_parquet(out_dir / "features.parquet")
    cm.save(features, "features")

    # Causal features (backward-only window) — used for supervised learning (steps 5-7).
    # Identical column names to features.parquet but no look-ahead in any derivative.
    features_sup = engineer_all(raw, cfg, causal=True)
    features_sup.to_parquet(out_dir / "features_supervised.parquet")
    cm.save(features_sup, "features_supervised")

    # Backwards-compatible aliases for plan-level artifact names.
    # These mirror the non-causal and causal feature sets produced above so
    # downstream plans can reference features_noncausal / features_causal
    # explicitly without changing the core pipeline semantics.
    cm.save(features, "features_noncausal")
    cm.save(features_sup, "features_causal")
    log.info(
        "Step 2: wrote features.parquet (centered) and features_supervised.parquet (causal)"
    )

    if run_cfg.generate_plots:
        feat_only = features.drop(columns=["market_code"], errors="ignore")
        plotting.plot_feature_distributions(feat_only, run_cfg)
        plotting.plot_feature_correlations(feat_only, run_cfg)

    log.info("Step 2 done: %d rows × %d feature cols", len(features), len(features.columns))


def step3_cluster(cfg: dict, run_cfg: RunConfig, save_market_code: bool = False) -> None:
    """PCA + KMeans clustering → data/regimes/cluster_labels.parquet.
    When save_market_code=True, also checkpoints balanced_cluster as market_code_clustered."""
    reduce_pca = crab.clustering.reduce_pca
    evaluate_kmeans = crab.clustering.evaluate_kmeans
    pick_best_k = crab.clustering.pick_best_k
    fit_clusters = crab.clustering.fit_clusters
    build_clustering_manifest = crab.clustering.build_clustering_manifest
    clustering_manifest_matches = crab.clustering.clustering_manifest_matches
    write_clustering_manifest = crab.clustering.write_clustering_manifest
    is_constrained_kmeans_available = crab.clustering.is_constrained_kmeans_available
    CheckpointManager = crab.checkpoints.CheckpointManager
    plotting = crab.plotting
    from sklearn.preprocessing import StandardScaler
    import pandas as pd

    cm = CheckpointManager()
    clust_cfg = cfg["clustering"]
    ttl = _checkpoint_ttl_days(cfg)

    features = _load_parquet(DATA_DIR / "processed" / "features.parquet", "features")
    X = features.drop(columns=["market_code"], errors="ignore").dropna()
    n_dropped = len(features) - len(X)
    if n_dropped:
        log.info(
            "Step 3: dropped %d quarter(s) with NaN features before PCA "
            "(expected when market_code source doesn't cover all dates)",
            n_dropped,
        )

    out_dir = DATA_DIR / "regimes"
    manifest_path = out_dir / "clustering_manifest.json"
    labels_path = out_dir / "cluster_labels.parquet"
    pca_path = out_dir / "pca_components.parquet"
    scores_path = out_dir / "kmeans_scores.parquet"

    constrained_available = is_constrained_kmeans_available()
    new_manifest = build_clustering_manifest(
        features,
        clust_cfg,
        use_constrained_requested=run_cfg.use_constrained_kmeans,
        constrained_available=constrained_available,
    )

    # Enforce "recluster only on intentional change" via manifest match.
    if (
        not run_cfg.recompute_derived_datasets
        and manifest_path.exists()
        and clustering_manifest_matches(manifest_path, new_manifest)
        and labels_path.exists()
        and pca_path.exists()
        and scores_path.exists()
    ):
        log.info("Step 3: inputs/config unchanged — skipping reclustering (use --recompute to override).")

        # Ensure checkpoints exist for downstream step runners.
        if labels_path.exists():
            df_labels = pd.read_parquet(labels_path)
            label_cols = [c for c in ["cluster", "balanced_cluster", "market_code"] if c in df_labels.columns]
            cm.save(df_labels[label_cols], "cluster_labels")
        if pca_path.exists():
            cm.save(pd.read_parquet(pca_path), "pca_components")

        if save_market_code and labels_path.exists():
            df_labels = pd.read_parquet(labels_path)
            if "balanced_cluster" in df_labels.columns:
                _save_market_code(df_labels["balanced_cluster"], "clustered")

        return

    # Backfill fallback caching (age-based) when manifest doesn't exist (older runs).
    if (
        not run_cfg.recompute_derived_datasets
        and cm.is_fresh("cluster_labels", max_age_days=ttl, require_config_match=True)
    ):
        log.info("Step 3: using cached cluster_labels checkpoint (age/config ok)")
        return

    pca_df, pca_model, scaler = reduce_pca(
        X,
        n_components=clust_cfg["n_pca_components"],
        random_state=clust_cfg["random_state"],
    )

    X_scaled = StandardScaler().fit_transform(pca_df.values)
    scores = evaluate_kmeans(
        X_scaled,
        k_range=range(2, clust_cfg["n_clusters_search"] + 1),
        random_state=clust_cfg["random_state"],
    )
    best_k = pick_best_k(scores, k_cap=clust_cfg["k_cap"])

    log.info("K-sweep: chose k=%d  (cap=%d)", best_k, clust_cfg["k_cap"])

    clustered = fit_clusters(
        pca_df,
        best_k=best_k,
        balanced_k=clust_cfg["balanced_k"],
        random_state=clust_cfg["random_state"],
        use_constrained=run_cfg.use_constrained_kmeans,
    )

    if "market_code" in features.columns:
        clustered["market_code"] = features["market_code"]

    out_dir = DATA_DIR / "regimes"
    out_dir.mkdir(parents=True, exist_ok=True)

    label_cols = ["cluster", "balanced_cluster"] + (
        ["market_code"] if "market_code" in clustered.columns else []
    )
    clustered[label_cols].to_parquet(out_dir / "cluster_labels.parquet")
    clustered.drop(columns=label_cols, errors="ignore").to_parquet(
        out_dir / "pca_components.parquet"
    )
    scores.to_parquet(out_dir / "kmeans_scores.parquet", index=False)

    cm.save(clustered[label_cols], "cluster_labels")
    cm.save(pca_df, "pca_components")

    # Write/refresh clustering manifest after successful clustering.
    write_clustering_manifest(manifest_path, new_manifest)

    # Optionally save balanced_cluster as a market_code checkpoint
    if save_market_code:
        _save_market_code(clustered["balanced_cluster"], "clustered")
        log.info(
            "Step 3: saved balanced_cluster as market_code_clustered checkpoint "
            "(use --market-code clustered on future runs)"
        )

    if run_cfg.generate_plots:
        regime_names: dict[int, str] = {}  # populated in step 4; use IDs for now
        plotting.plot_pca_scatter(pca_df, clustered["balanced_cluster"], regime_names, run_cfg)
        plotting.plot_elbow_curve(scores, best_k, run_cfg)
        plotting.plot_cluster_sizes(clustered["balanced_cluster"], regime_names, run_cfg)

    log.info("Step 3 done: balanced_k=%d", clust_cfg["balanced_k"])


def step4_regime_label(cfg: dict, run_cfg: RunConfig) -> None:
    """Profile clusters → data/regimes/profiles.parquet + transition_matrix.parquet"""
    build_profiles = crab.regime.build_profiles
    suggest_names = crab.regime.suggest_names
    build_transition_matrix = crab.regime.build_transition_matrix
    load_name_overrides = crab.regime.load_name_overrides
    CheckpointManager = crab.checkpoints.CheckpointManager
    plotting = crab.plotting
    import pandas as pd
    import yaml

    labels_path = DATA_DIR / "regimes" / "cluster_labels.parquet"
    cm = CheckpointManager()
    if not labels_path.exists() and not (cm.dir / "cluster_labels.parquet").exists():
        raise FileNotFoundError(
            "cluster_labels.parquet not found and no cluster_labels checkpoint. "
            "Run step 3 first: python run_pipeline.py --steps 3"
        )

    features = _load_parquet(DATA_DIR / "processed" / "features.parquet", "features")
    labels = _load_parquet(labels_path, "cluster_labels")["balanced_cluster"]

    common = features.index.intersection(labels.index)
    features = features.loc[common]
    labels = labels.loc[common]

    profile = build_profiles(features, labels)
    profile.to_parquet(DATA_DIR / "regimes" / "profiles.parquet")

    auto_names = suggest_names(features, labels)
    overrides = load_name_overrides(CONFIG_DIR)
    regime_names = {**auto_names, **overrides}

    suggestions_path = DATA_DIR / "regimes" / "regime_names_suggested.yaml"
    with open(suggestions_path, "w") as f:
        yaml.dump(regime_names, f, default_flow_style=False)

    tm = build_transition_matrix(labels)
    tm.to_parquet(DATA_DIR / "regimes" / "transition_matrix.parquet")

    if run_cfg.generate_plots:
        plotting.plot_transition_matrix(tm, regime_names, run_cfg)
        plotting.plot_regime_timeline(labels, regime_names, run_cfg)
        key_cols = [
            c for c in [
                "us_infl", "gdp_growth", "credit_spread", "sp500_pe",
                "log_cpi_d1", "10yr_ustreas_d1", "log_earn_d1",
            ] if c in features.columns
        ]
        if key_cols:
            plotting.plot_regime_profiles(features, labels, regime_names, key_cols, run_cfg)

    for rid, name in sorted(regime_names.items()):
        n = (labels == rid).sum()
        log.info("Cluster %d: %r  (%d quarters)", rid, name, n)

    log.info("Step 4 done")


def step5_predict(cfg: dict, run_cfg: RunConfig) -> None:
    """Train supervised classifiers → outputs/models/"""
    from trading_crab_lib.asset_returns import compute_proxy_returns, compute_quarterly_returns
    from trading_crab_lib.prediction.classifier import (
        train_current_regime,
        train_forward_classifiers,
        train_forward_behavior_models,
        train_interpretability_tree,
    )
    from trading_crab_lib.prediction.feature_gating import select_step5_feature_path
    from trading_crab_lib.prediction.model_metrics_artifacts import write_model_metrics_artifacts
    from trading_crab_lib import plotting
    from sklearn.tree import export_text
    import pandas as pd
    import pickle

    feature_path, feature_source, noncausal_used = select_step5_feature_path(
        DATA_DIR / "processed",
        allow_noncausal_features=run_cfg.allow_noncausal_features,
    )
    features = _load_parquet(feature_path, feature_source)

    labels = _load_parquet(
        DATA_DIR / "regimes" / "cluster_labels.parquet", "cluster_labels"
    )["balanced_cluster"]

    common = features.index.intersection(labels.index)
    X = features.loc[common].drop(columns=["market_code"], errors="ignore").dropna(axis=1, how="any")
    y = labels.loc[common]

    # Regime-model horizons / CV
    cv_splits = int(cfg.get("prediction", {}).get("cv_splits", 5))
    forward_horizons = cfg.get("prediction", {}).get("forward_horizons_quarters", [1, 2, 4, 8])
    behavior_horizons = cfg.get("prediction", {}).get("behavior_horizons_quarters", [1])

    # ── Regime: current + forward CV bundles ────────────────────────────────
    current_bundle = train_current_regime(X, y, cv_splits=cv_splits)
    rf_model = current_bundle["models"]["rf"]
    dt_model = current_bundle["models"]["dt"]

    # Latest quarter prediction (rf_model gives proba)
    latest_proba = rf_model.predict_proba(X.iloc[[-1]])[0]
    classes = rf_model.classes_
    prob_by_class = {int(c): float(p) for c, p in zip(classes, latest_proba)}
    latest_regime = max(prob_by_class.items(), key=lambda kv: kv[1])[0]

    log.info("Latest quarter → regime %d", latest_regime)
    for r, p in sorted(prob_by_class.items(), key=lambda x: -x[1]):
        log.info("  Regime %d: %.1f%%", r, p * 100)

    forward_models = train_forward_classifiers(
        X, y, horizons=forward_horizons, cv_splits=cv_splits
    )

    model_dir = OUTPUT_DIR / "models"
    model_dir.mkdir(parents=True, exist_ok=True)

    with open(model_dir / "current_regime.pkl", "wb") as f:
        pickle.dump(rf_model, f)
    with open(model_dir / "decision_tree.pkl", "wb") as f:
        pickle.dump(dt_model, f)
    if "gb" in current_bundle["models"]:
        with open(model_dir / "current_regime_gb.pkl", "wb") as f:
            pickle.dump(current_bundle["models"]["gb"], f)
        log.info("Step 5: saved gradient boosting model → current_regime_gb.pkl")
    with open(model_dir / "forward_classifiers.pkl", "wb") as f:
        pickle.dump(forward_models, f)

    # Optionally save predicted labels as a market_code checkpoint
    predicted_labels = pd.Series(
        rf_model.predict(X), index=X.index, name="market_code"
    ).astype(int)
    _save_market_code(predicted_labels, "predicted")
    log.info(
        "Step 5: saved predicted regime labels as market_code_predicted checkpoint "
        "(use --market-code predicted on future runs)"
    )

    # ── Behavior: train per-asset up/flat/down models ─────────────────────
    raw_dir = DATA_DIR / "raw"
    asset_prices_path = raw_dir / "asset_prices.parquet"
    macro_raw_path = raw_dir / "macro_raw.parquet"

    returns: pd.DataFrame | None = None
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

    with open(model_dir / "behavior_models.pkl", "wb") as f:
        pickle.dump(behavior_bundle, f)

    # ── Metrics artifacts (MODEL-04) ───────────────────────────────────────
    metrics_dir = OUTPUT_DIR / "reports" / "model_metrics"
    write_model_metrics_artifacts(
        output_dir=metrics_dir,
        feature_source=feature_source,
        noncausal_used=noncausal_used,
        regime_current_bundle=current_bundle,
        forward_models=forward_models,
        behavior_bundle=behavior_bundle,
    )

    if run_cfg.generate_plots:
        try:
            regime_names_path = DATA_DIR / "regimes" / "regime_names_suggested.yaml"
            import yaml
            regime_names = {}
            if regime_names_path.exists():
                with open(regime_names_path) as f:
                    regime_names = yaml.safe_load(f) or {}
                regime_names = {int(k): v for k, v in regime_names.items()}
            plotting.plot_feature_importance(rf_model, X.columns.tolist(), run_cfg)
            plotting.plot_forward_probabilities(
                {"regime": latest_regime, "probabilities": prob_by_class},
                regime_names,
                run_cfg,
            )
            plotting.plot_predicted_vs_actual(X, y, rf_model, regime_names, run_cfg)
        except Exception as exc:
            log.warning("Could not generate prediction plots: %s", exc)

    # ── Interpretability tree (Phase 9) — RF top features ─────────────────────
    report_dir = OUTPUT_DIR / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    try:
        tree_model, tree_features = train_interpretability_tree(rf_model, X, y, cfg)
        tree_txt = export_text(tree_model, feature_names=tree_features)
        tree_path = report_dir / "current_regime_tree.txt"
        tree_path.write_text(tree_txt, encoding="utf-8")
        log.info("Wrote interpretability tree → %s", tree_path)
    except Exception as exc:  # pragma: no cover - defensive
        log.warning("Could not generate interpretability tree: %s", exc)

    # ── Interpretability tree on gradient boosting (Phase 19 / MODEL-11) ─────
    pred_cfg = cfg.get("prediction", {})
    if (
        "gb" in current_bundle["models"]
        and pred_cfg.get("interpret_tree_on_boosted", True)
    ):
        try:
            gb_model = current_bundle["models"]["gb"]
            tree_gb, tree_features_gb = train_interpretability_tree(gb_model, X, y, cfg)
            tree_txt_gb = export_text(tree_gb, feature_names=tree_features_gb)
            tree_path_gb = report_dir / "current_regime_tree_gb.txt"
            tree_path_gb.write_text(tree_txt_gb, encoding="utf-8")
            log.info("Wrote GB interpretability tree → %s", tree_path_gb)
        except Exception as exc:  # pragma: no cover - defensive
            log.warning("Could not generate GB interpretability tree: %s", exc)

    log.info("Step 5 done — models saved to %s", model_dir)


def step6_asset_returns(cfg: dict, run_cfg: RunConfig) -> None:
    """Compute ETF / proxy returns by regime → ``data/regimes/asset_return_profile.parquet``.

    ETF prices are normally loaded in step 1; this step reuses
    ``data/raw/asset_prices.parquet`` unless ``--refresh-assets`` is set."""
    from trading_crab_lib.ingestion.assets import load_or_fetch_quarterly_prices
    from trading_crab_lib.asset_returns import (
        behavior_tables,
        compute_quarterly_returns,
        compute_proxy_returns,
        compute_template_returns,
        returns_by_regime,
        rank_assets_by_regime,
    )
    from trading_crab_lib.checkpoints import CheckpointManager
    from trading_crab_lib import plotting
    import pandas as pd

    cm = CheckpointManager()
    ttl = _checkpoint_ttl_days(cfg)

    labels = _load_parquet(DATA_DIR / "regimes" / "cluster_labels.parquet", "cluster_labels")["balanced_cluster"]

    prices = load_or_fetch_quarterly_prices(
        cfg,
        data_dir=DATA_DIR,
        refresh=run_cfg.refresh_asset_prices,
        cm=cm,
        max_age_days=ttl,
    )

    # Compute returns: use real ETF prices when available, macro proxies otherwise
    returns: pd.DataFrame | None = None
    if prices is not None and not prices.empty:
        returns = compute_quarterly_returns(prices)
        log.info("Step 6: using ETF price data (%d tickers)", len(returns.columns))
    else:
        log.warning(
            "Step 6: no ETF price data available — computing proxy returns from macro data"
        )
        macro_path = DATA_DIR / "raw" / "macro_raw.parquet"
        if macro_path.exists():
            macro_df = pd.read_parquet(macro_path)
            returns = compute_proxy_returns(macro_df)
            if returns.empty:
                log.warning("Step 6: proxy returns also empty — skipping")
                return
            log.info(
                "Step 6: proxy returns computed (%d quarters × %d assets)",
                len(returns), len(returns.columns),
            )
        else:
            log.warning("Step 6: macro_raw.parquet not found — skipping")
            return

    common = returns.index.intersection(labels.index)
    returns_aligned = returns.loc[common]
    labels_aligned = labels.loc[common]

    # profile: regime × ticker DataFrame of median returns
    profile = returns_by_regime(returns_aligned, labels_aligned)

    out_dir = DATA_DIR / "regimes"
    out_dir.mkdir(parents=True, exist_ok=True)
    profile.to_parquet(out_dir / "asset_return_profile.parquet")

    # Parity with pipelines/06_asset_returns.py: ETF behavior + optional template portfolios
    behavior_thresholds = cfg.get("dashboard", {}).get("behavior_thresholds") or {}
    etf_behavior = behavior_tables(returns_aligned, labels_aligned, thresholds=behavior_thresholds)
    etf_behavior.to_parquet(out_dir / "etf_behavior_by_regime.parquet", index=False)
    log.info("Step 6: wrote ETF behavior by regime → %s", out_dir / "etf_behavior_by_regime.parquet")

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
            log.info(
                "Step 6: wrote template behavior by regime → %s",
                out_dir / "template_behavior_by_regime.parquet",
            )

    if run_cfg.generate_plots:
        try:
            regime_names_path = DATA_DIR / "regimes" / "regime_names_suggested.yaml"
            import yaml
            regime_names = {}
            if regime_names_path.exists():
                with open(regime_names_path) as f:
                    regime_names = yaml.safe_load(f) or {}
                regime_names = {int(k): v for k, v in regime_names.items()}
            plotting.plot_asset_returns_by_regime(profile, regime_names, run_cfg)
            plotting.plot_asset_heatmap(profile, regime_names, run_cfg)
        except Exception as exc:
            log.warning("Could not generate asset plots: %s", exc)

    log.info("Step 6 done — asset return profile written")


def step7_dashboard(cfg: dict, run_cfg: RunConfig) -> None:
    """Print + save stoplight dashboard → outputs/reports/dashboard.csv
    Also computes portfolio weights and BUY/SELL/HOLD trade recommendations."""
    from trading_crab_lib.prediction import predict_current
    from trading_crab_lib.asset_returns import rank_assets_by_regime
    from trading_crab_lib.reporting import (
        asset_signals,
        blended_regime_portfolio,
        build_recommendation_digest,
        generate_recommendation,
        print_dashboard,
        save_dashboard_csv,
        save_recommendation_bundle,
        simple_regime_portfolio,
        write_weekly_report_md,
    )
    import pandas as pd
    import pickle
    import yaml

    model_dir = OUTPUT_DIR / "models"
    current_model_path = model_dir / "current_regime.pkl"
    if not current_model_path.exists():
        log.warning("Step 7: current_regime.pkl not found — run step 5 first")
        return

    with open(current_model_path, "rb") as f:
        current_model = pickle.load(f)

    # Step 7 uses causal features for live scoring — same as step 5 training data.
    # Falls back to centered features.parquet when supervised file is absent.
    sup_path = DATA_DIR / "processed" / "features_supervised.parquet"
    feat_path = sup_path if sup_path.exists() else DATA_DIR / "processed" / "features.parquet"
    if not sup_path.exists():
        log.warning(
            "Step 7: features_supervised.parquet not found — falling back to features.parquet. "
            "Re-run step 2 to generate causal features."
        )
    features = _load_parquet(feat_path, "features_supervised")
    X = features.drop(columns=["market_code"], errors="ignore")
    # Align to the exact feature set the model was trained on
    if hasattr(current_model, "feature_names_in_"):
        X = X[current_model.feature_names_in_]
    else:
        X = X.dropna(axis=1, how="any")
    prediction = predict_current(current_model, X)

    tm = _load_parquet(DATA_DIR / "regimes" / "transition_matrix.parquet", "transition_matrix")

    # Hybrid naming governance:
    # - Start from step-4 auto-suggestions
    # - Overlay any pinned IDs from config/regime_labels.yaml
    suggested_path = DATA_DIR / "regimes" / "regime_names_suggested.yaml"
    overrides_path = CONFIG_DIR / "regime_labels.yaml"

    suggested_names: dict[int, str] = {}
    if suggested_path.exists():
        with open(suggested_path) as f:
            raw = yaml.safe_load(f) or {}
        suggested_names = {int(k): v for k, v in raw.items() if not str(k).startswith("#")}

    overrides: dict[int, str] = {}
    if overrides_path.exists():
        with open(overrides_path) as f:
            raw = yaml.safe_load(f) or {}
        overrides = {int(k): v for k, v in raw.items() if not str(k).startswith("#")}

    regime_names = {**suggested_names, **overrides}

    # Load signal thresholds from config
    thresholds = cfg.get("dashboard", {}).get("signal_thresholds", None)

    asset_signals_df = pd.DataFrame()
    profile_path = DATA_DIR / "regimes" / "asset_return_profile.parquet"
    if profile_path.exists():
        # profile is regime × ticker; rank_assets_by_regime produces the flat form
        profile = pd.read_parquet(profile_path)
        ranked = rank_assets_by_regime(profile)
        asset_signals_df = asset_signals(ranked, prediction["regime"], thresholds=thresholds)

    print_dashboard(prediction, regime_names, asset_signals_df, tm)

    if not asset_signals_df.empty:
        save_dashboard_csv(asset_signals_df, OUTPUT_DIR / "reports")

    # ── Portfolio construction and trade recommendations ─────────────────────
    if profile_path.exists():
        profile = pd.read_parquet(profile_path)
        current_regime = prediction["regime"]
        probs = prediction["probabilities"]

        log.info("── Simple portfolio (top-3, regime %d) ──", current_regime)
        simple_weights = simple_regime_portfolio(profile, current_regime, top_n=3)

        log.info("── Blended portfolio (probability-weighted) ──")
        blended_weights = blended_regime_portfolio(profile, probs, top_n=3)

        rec_threshold = cfg.get("dashboard", {}).get("recommendation_threshold", 0.03)
        portfolio_weights = load_portfolio()
        current_weights = pd.Series(portfolio_weights) if portfolio_weights else None
        log.info(
            "── Trade recommendations (blended vs portfolio, %.0f%% threshold) ──",
            rec_threshold * 100,
        )
        recommendations = generate_recommendation(
            blended_weights, current_weights=current_weights, threshold=rec_threshold
        )

        report_dir = OUTPUT_DIR / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)

        if not simple_weights.empty:
            simple_weights.to_frame("weight").to_csv(report_dir / "portfolio_simple.csv")
        if not blended_weights.empty:
            blended_weights.to_frame("weight").to_csv(report_dir / "portfolio_blended.csv")
        if not recommendations.empty:
            recommendations.to_csv(report_dir / "trade_recommendations.csv")
            log.info(
                "Trade recommendations saved to %s",
                report_dir / "trade_recommendations.csv",
            )

        # Machine-readable bundle (parity with pipelines/07_dashboard.py)
        behavior_path = DATA_DIR / "regimes" / "etf_behavior_by_regime.parquet"
        if behavior_path.exists() and not recommendations.empty:
            behavior_df = pd.read_parquet(behavior_path)
            digest = build_recommendation_digest(
                behavior_df,
                current_regime,
                current_weights,  # None => all-cash baseline (same as pipelines/07_dashboard.py)
                blended_weights,
                recommendations,
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

        if not recommendations.empty:
            try:
                weekly_out = report_dir / "weekly_report.md"
                weekly_out.parent.mkdir(parents=True, exist_ok=True)
                transition_row = (
                    tm.loc[current_regime]
                    if current_regime in tm.index
                    else None
                )
                write_weekly_report_md(
                    current_regime=current_regime,
                    regime_name=regime_names.get(current_regime, "Unknown"),
                    regime_probabilities=probs,
                    rec_df=recommendations,
                    transition_row=transition_row,
                    output_path=weekly_out,
                    cfg=cfg,
                )
                log.info("Weekly report saved to %s", weekly_out)
            except Exception as exc:
                log.warning("Could not write weekly_report.md: %s", exc)

    log.info("Step 7 done")


# ── Step 8: Diagnostics ───────────────────────────────────────────────────────

def step8_diagnostics(cfg: dict, run_cfg: RunConfig) -> None:
    """Compute ratio and RRG diagnostics from ETF prices → outputs/reports/diagnostics/."""
    from trading_crab_lib import plotting
    from trading_crab_lib.diagnostics import compute_ratios_diagnostics, rrg_for_benchmark

    import pandas as pd

    prices_path = DATA_DIR / "raw" / "asset_prices.parquet"
    if not prices_path.exists():
        log.warning("Step 8: ETF prices %s not found; skipping diagnostics.", prices_path)
        return

    prices = pd.read_parquet(prices_path)
    tickers = cfg.get("assets", {}).get("etfs") or list(prices.columns)
    cols = [t for t in tickers if t in prices.columns]
    if not cols:
        log.warning("Step 8: no configured ETF columns in prices; skipping diagnostics.")
        return
    prices = prices[cols]

    diag_dir = OUTPUT_DIR / "reports" / "diagnostics"
    diag_dir.mkdir(parents=True, exist_ok=True)

    ratios_df = compute_ratios_diagnostics(prices, cfg)
    if not ratios_df.empty:
        ratios_df.to_parquet(diag_dir / "ratios_current.parquet", index=False)
        log.info("Step 8: wrote ratio diagnostics to %s", diag_dir / "ratios_current.parquet")

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
        rrg_path = diag_dir / "rrg_current.parquet"
        rrg_combined.to_parquet(rrg_path, index=False)
        log.info("Step 8: wrote RRG diagnostics to %s", rrg_path)

    if run_cfg.generate_plots:
        plotting.plot_diagnostics_ratios_summary(ratios_df, run_cfg)
        plotting.plot_diagnostics_rrg(rrg_combined, run_cfg)

    log.info("Step 8 done")


# ── Step dispatch table ────────────────────────────────────────────────────────

from trading_crab_lib.tactics import compute_tactics_metrics, classify_tactics


def step9_tactics(cfg: dict, run_cfg: RunConfig) -> None:
    """Compute per-asset tactics signals and write tactics_signals.parquet."""
    import pandas as pd

    prices_path = DATA_DIR / "raw" / "asset_prices.parquet"
    labels_path = DATA_DIR / "regimes" / "cluster_labels.parquet"

    if not prices_path.exists():
        log.warning("Step 9: ETF prices checkpoint %s not found; skipping tactics.", prices_path)
        return
    if not labels_path.exists():
        log.warning("Step 9: cluster labels %s not found; skipping tactics.", labels_path)
        return

    prices = pd.read_parquet(prices_path)
    labels = pd.read_parquet(labels_path)["balanced_cluster"]

    metrics = compute_tactics_metrics(prices, labels, cfg)
    tactics_df = classify_tactics(metrics, cfg).reset_index()

    out_dir = OUTPUT_DIR / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "tactics_signals.parquet"
    tactics_df.to_parquet(out_path, index=False)
    log.info("Step 9: tactics signals written to %s", out_path)


STEPS: dict[int, tuple[str, callable]] = {
    1: ("Ingest macro data",            step1_ingest),
    2: ("Engineer features",            step2_features),
    3: ("PCA + clustering",             step3_cluster),
    4: ("Regime profiling + labeling",  step4_regime_label),
    5: ("Supervised prediction",        step5_predict),
    6: ("Asset returns",                step6_asset_returns),
    7: ("Dashboard",                    step7_dashboard),
    8: ("Diagnostics (ratios + RRG)",    step8_diagnostics),
    9: ("Tactics signals",              step9_tactics),
}


# ── Weekly report helpers (archive + email) ────────────────────────────────────

def archive_weekly_report(reports_dir: Path | None = None) -> None:
    """
    Copy weekly_report.md to weekly_YYYY-MM-DD.md and write email_body.txt.

    No-op if weekly_report.md does not exist. This mirrors the behaviour of
    scripts/run_weekly_report.py so that the full weekly flow can be driven
    directly via run_pipeline.
    """
    reports = reports_dir or (OUTPUT_DIR / "reports")
    report_path = reports / "weekly_report.md"
    if not report_path.exists():
        print(f"No weekly_report.md at {report_path} — skip archive/email body.")
        return

    today = date.today().isoformat()
    stamped = reports / f"weekly_{today}.md"
    stamped.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(report_path, stamped)
    print(f"Archived report → {stamped}")

    email_body_path = reports / "email_body.txt"
    body = report_path.read_text(encoding="utf-8")
    email_body_path.write_text(body, encoding="utf-8")
    print(f"Email body → {email_body_path}")


# ── CLI ────────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Trading-Crab market regime pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--refresh", action="store_true",
                   help="Re-scrape multpl.com + re-hit FRED API")
    p.add_argument("--recompute", action="store_true",
                   help="Recompute features from cached raw data")
    p.add_argument("--refresh-assets", action="store_true",
                   help=(
                       "Re-fetch ETF prices from yfinance (step 6). "
                       "Without this flag, step 6 loads from the cached "
                       "data/raw/asset_prices.parquet if it exists. "
                       "Useful behind firewalls: omit this flag to reuse "
                       "previously fetched prices without hitting the network."
                   ))
    p.add_argument("--plots", action="store_true",
                   help="Generate and save matplotlib figures")
    p.add_argument("--show-plots", action="store_true",
                   help="Call plt.show() after each figure")
    p.add_argument("--verbose", action="store_true",
                   help="Set logging to DEBUG")
    p.add_argument("--steps", type=str, default=None,
                   help="Comma-separated step numbers to run, e.g. 1,3,5")
    p.add_argument("--no-constrained", action="store_true",
                   help="Skip k-means-constrained (if package not installed)")
    p.add_argument("--no-drop-tail", action="store_true",
                   help=(
                       "Include the most-recent (potentially incomplete) quarter "
                       "in training and prediction rather than trimming it. "
                       "By default the trailing row is dropped when it contains "
                       "NaN in any feature column (centered np.gradient edge effect)."
                   ))
    p.add_argument(
        "--allow-noncausal-features",
        action="store_true",
        help=(
            "Allow step 5 to fall back to data/processed/features.parquet "
            "when data/processed/features_supervised.parquet is missing. "
            "This bypasses the causal-feature leakage guardrail, so it is "
            "disabled by default and emits an unmissable warning."
        ),
    )
    p.add_argument("--market-code", type=str, default=None, metavar="NAME",
                   help=(
                       "Load market_code from this source. "
                       "'grok' loads the grok pickle; any other value loads "
                       "checkpoint 'market_code_{NAME}'. Omit to run without market_code."
                   ))
    p.add_argument("--save-market-code", action="store_true",
                   help=(
                       "After step 3, save balanced_cluster labels as the "
                       "'market_code_clustered' checkpoint for future use with "
                       "--market-code clustered."
                   ))
    p.add_argument(
        "--weekly-report",
        action="store_true",
        help=(
            "After running the selected steps, archive outputs/reports/weekly_report.md "
            "to a dated copy and write outputs/reports/email_body.txt."
        ),
    )
    p.add_argument(
        "--send-email",
        action="store_true",
        help=(
            "After weekly-report post-processing, send the weekly report email via "
            "config/email.local.yaml (see config/email.example.yaml)."
        ),
    )
    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    setup_logging()
    run_cfg = RunConfig.from_args(args)
    run_cfg.apply_logging()

    cfg = load()

    # Determine which steps to run
    if args.steps:
        try:
            requested = {int(s.strip()) for s in args.steps.split(",")}
        except ValueError:
            parser.error("--steps must be comma-separated integers, e.g. 1,3,5")
    else:
        requested = set(STEPS.keys())

    invalid = requested - set(STEPS.keys())
    if invalid:
        parser.error(f"Unknown step numbers: {invalid}. Valid: {sorted(STEPS.keys())}")

    save_market_code = getattr(args, "save_market_code", False)

    print(f"\nTrading-Crab pipeline  [{run_cfg}]")
    print(f"Steps to run: {sorted(requested)}")
    if run_cfg.market_code_source:
        print(f"market_code source: {run_cfg.market_code_source}")
    print()

    # Ensure output dirs exist
    (OUTPUT_DIR / "plots").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "models").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "reports").mkdir(parents=True, exist_ok=True)

    for step_num in sorted(requested):
        label, fn = STEPS[step_num]
        print(f"── Step {step_num}: {label} ──")
        try:
            # step3 needs the save_market_code flag
            if step_num == 3:
                fn(cfg, run_cfg, save_market_code=save_market_code)
            else:
                fn(cfg, run_cfg)
            print(f"   ✓ done\n")
        except Exception as exc:
            log.exception("Step %d failed: %s", step_num, exc)
            print(f"   ✗ FAILED: {exc}\n")
            sys.exit(1)

    # Optional weekly-report archive + email sending
    if getattr(args, "weekly_report", False) or getattr(args, "send_email", False):
        archive_weekly_report()

    if getattr(args, "send_email", False):
        email_cfg = load_email_config()
        if not email_cfg:
            print("Email config not found or invalid; skipping send.")
        else:
            subject, body = build_weekly_email_body()
            ok = send_weekly_email(email_cfg, subject, body)
            if ok:
                print("Weekly report email sent.")
            else:
                print("Weekly report email failed to send (see logs).")

    print("Pipeline complete.")


if __name__ == "__main__":
    main()
