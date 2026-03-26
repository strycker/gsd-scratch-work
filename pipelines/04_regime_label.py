"""
Pipeline step 4 — Regime Profiling & Labeling

Reads cluster_labels + raw features, computes per-cluster statistics,
suggests human-readable names, and writes:
  data/regimes/profiles.parquet
  data/regimes/transition_matrix.parquet
  data/regimes/forward_window_probabilities.parquet
  data/regimes/regime_names_suggested.yaml   — auto-suggested (edit manually)
  (ETF/proxy return statistics by regime → data/regimes/etf_behavior_by_regime.parquet from step 6.)

Run:
    python pipelines/04_regime_label.py
"""

# Connects machine IDs to human language (stagflation, etc.) — edit regime_labels.yaml after review.
# Transition and forward-window tables are *empirical* Markov-style summaries — not model-based forecasts.

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import trading_crab_lib as crab

DATA_DIR = crab.DATA_DIR
CONFIG_DIR = crab.CONFIG_DIR
load = crab.load
setup_logging = crab.setup_logging

import pandas as pd
import yaml

from trading_crab_lib.regime import (
    build_forward_window_probabilities,
    build_profiles,
    build_transition_matrix,
    load_name_overrides,
    suggest_names,
)


def main() -> None:
    setup_logging()
    cfg = load()

    labels_path = DATA_DIR / "regimes" / "cluster_labels.parquet"
    if not labels_path.exists():
        raise FileNotFoundError(
            f"{labels_path} not found. Run step 3 (cluster) first, e.g.:\n"
            "  python run_pipeline.py --steps 3\n"
            "or run the full pipeline so step 2 and 3 complete before step 4."
        )

    features = pd.read_parquet(DATA_DIR / "processed" / "features.parquet")
    labels = pd.read_parquet(labels_path)["balanced_cluster"]

    # Align index (features may have more rows if gap-filled beyond label dates)
    common = features.index.intersection(labels.index)
    features = features.loc[common]
    labels = labels.loc[common]

    # Profile
    profile = build_profiles(features, labels)
    profile.to_parquet(DATA_DIR / "regimes" / "profiles.parquet")

    # Auto-suggest names from raw features + labels, then apply manual overrides
    auto_names = suggest_names(features, labels)
    overrides = load_name_overrides(CONFIG_DIR)
    regime_names = {**auto_names, **overrides}

    # Save auto-suggestions so user can review / edit config/regime_labels.yaml
    suggestions_path = DATA_DIR / "regimes" / "regime_names_suggested.yaml"
    with open(suggestions_path, "w") as f:
        yaml.dump(regime_names, f, default_flow_style=False)
    print(f"Regime name suggestions → {suggestions_path}")

    # Transition matrix
    tm = build_transition_matrix(labels)
    tm.to_parquet(DATA_DIR / "regimes" / "transition_matrix.parquet")

    # Forward-window empirical probabilities (same horizons as Phase 3 classifiers)
    horizons = cfg.get("prediction", {}).get("forward_horizons_quarters") or [1, 2, 4, 8]
    forward_probs = build_forward_window_probabilities(labels, horizons)
    fwp_path = DATA_DIR / "regimes" / "forward_window_probabilities.parquet"
    forward_probs.to_parquet(fwp_path)
    print(f"Forward-window probabilities → {fwp_path}")

    # Diagnostic excerpt: horizon=1 and horizon=max
    if not forward_probs.empty and len(horizons) > 0:
        h1 = forward_probs[forward_probs["horizon_quarters"] == horizons[0]]
        h_max = forward_probs[forward_probs["horizon_quarters"] == max(horizons)]
        print("\nForward-window P(reach j | current i) — horizon=1 (excerpt):")
        print(h1.head(12).round(3).to_string(index=False))
        print("\nForward-window — horizon=max (excerpt):")
        print(h_max.head(12).round(3).to_string(index=False))

    print("\nRegime summary:")
    for rid, name in sorted(regime_names.items()):
        n = (labels == rid).sum()
        print(f"  Cluster {rid}: {name!r}  ({n} quarters)")

    print("\nTransition matrix (row=from, col=to):")
    print(tm.round(2).to_string())


if __name__ == "__main__":
    main()
