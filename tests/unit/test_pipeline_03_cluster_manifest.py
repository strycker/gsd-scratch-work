import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import importlib.util


def _load_module_from_path(module_name: str, file_path: Path):
    """Load a non-package python file as a module via importlib."""
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:  # pragma: no cover
        raise RuntimeError(f"Could not load module {module_name} from {file_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _write_minimal_step3_artifacts(regimes_dir: Path, *, index: pd.DatetimeIndex) -> None:
    regimes_dir.mkdir(parents=True, exist_ok=True)
    labels = pd.DataFrame(
        {
            "cluster": [0] * len(index),
            "balanced_cluster": [0] * len(index),
        },
        index=index,
    )
    labels.to_parquet(regimes_dir / "cluster_labels.parquet")

    pca = pd.DataFrame({"PC1": [0.0] * len(index)}, index=index)
    pca.to_parquet(regimes_dir / "pca_components.parquet")

    scores = pd.DataFrame(
        {
            "k": [2, 3],
            "inertia": [1.0, 0.5],
            "silhouette": [0.1, 0.2],
            "calinski": [10.0, 12.0],
            "davies_bouldin": [1.2, 1.1],
        }
    )
    scores.to_parquet(regimes_dir / "kmeans_scores.parquet", index=False)


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_step3_pipeline_skips_when_manifest_matches(tmp_path, monkeypatch):
    """
    Behavioral check for Phase 2 REGIME-01 locked policy:
    - When clustering artifacts exist AND clustering_manifest.json matches, step 3 should skip
      unless --force is provided.
    """
    from market_regime import clustering as clustering_mod

    repo_root = Path(__file__).resolve().parents[2]
    step3_path = repo_root / "pipelines" / "03_cluster.py"
    step3 = _load_module_from_path("step3_cluster_mod_skip", step3_path)

    data_dir = tmp_path / "data"
    processed = data_dir / "processed"
    regimes = data_dir / "regimes"
    processed.mkdir(parents=True, exist_ok=True)

    idx = pd.date_range("2000-03-31", periods=12, freq="QE")
    features = pd.DataFrame(
        {
            "f1": range(len(idx)),
            "f2": range(len(idx)),
            "market_code": [0] * len(idx),
        },
        index=idx,
    )
    features.to_parquet(processed / "features.parquet")

    _write_minimal_step3_artifacts(regimes, index=idx)

    clust_cfg = {
        "n_pca_components": 5,
        "n_clusters_search": 12,
        "k_cap": 5,
        "balanced_k": 5,
        "random_state": 42,
    }

    manifest = clustering_mod.build_clustering_manifest(
        features,
        clust_cfg,
        use_constrained_requested=True,
        constrained_available=False,
    )
    clustering_mod.write_clustering_manifest(regimes / "clustering_manifest.json", manifest)

    # Patch DATA_DIR references used by the pipeline module.
    monkeypatch.setattr(step3, "DATA_DIR", data_dir)
    monkeypatch.setattr(step3, "setup_logging", lambda: None)
    monkeypatch.setattr(step3, "load", lambda: {"clustering": clust_cfg})
    monkeypatch.setattr(step3, "is_constrained_kmeans_available", lambda: False)

    labels_path = regimes / "cluster_labels.parquet"
    pca_path = regimes / "pca_components.parquet"
    scores_path = regimes / "kmeans_scores.parquet"
    before = (
        labels_path.stat().st_mtime_ns,
        pca_path.stat().st_mtime_ns,
        scores_path.stat().st_mtime_ns,
    )

    # Run with no args => skip branch should trigger.
    monkeypatch.setattr(sys, "argv", ["pipelines/03_cluster.py"])
    step3.main()

    after = (
        labels_path.stat().st_mtime_ns,
        pca_path.stat().st_mtime_ns,
        scores_path.stat().st_mtime_ns,
    )
    assert after == before


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_step3_pipeline_force_reclusters_even_when_manifest_matches(tmp_path, monkeypatch):
    from market_regime import clustering as clustering_mod

    repo_root = Path(__file__).resolve().parents[2]
    step3_path = repo_root / "pipelines" / "03_cluster.py"
    step3 = _load_module_from_path("step3_cluster_mod_force", step3_path)

    data_dir = tmp_path / "data"
    processed = data_dir / "processed"
    regimes = data_dir / "regimes"
    processed.mkdir(parents=True, exist_ok=True)

    idx = pd.date_range("2000-03-31", periods=30, freq="QE")
    features = pd.DataFrame(
        {
            "f1": range(len(idx)),
            "f2": range(len(idx)),
            "f3": range(len(idx)),
        },
        index=idx,
    )
    features.to_parquet(processed / "features.parquet")

    _write_minimal_step3_artifacts(regimes, index=idx[:12])

    clust_cfg = {
        "n_pca_components": 2,
        "n_clusters_search": 4,
        "k_cap": 3,
        "balanced_k": 3,
        "random_state": 42,
    }
    manifest = clustering_mod.build_clustering_manifest(
        features,
        clust_cfg,
        use_constrained_requested=True,
        constrained_available=False,
    )
    clustering_mod.write_clustering_manifest(regimes / "clustering_manifest.json", manifest)

    monkeypatch.setattr(step3, "DATA_DIR", data_dir)
    monkeypatch.setattr(step3, "setup_logging", lambda: None)
    monkeypatch.setattr(step3, "load", lambda: {"clustering": clust_cfg})
    monkeypatch.setattr(step3, "is_constrained_kmeans_available", lambda: False)

    labels_path = regimes / "cluster_labels.parquet"
    before = labels_path.stat().st_mtime_ns

    monkeypatch.setattr(sys, "argv", ["pipelines/03_cluster.py", "--force"])
    step3.main()

    after = labels_path.stat().st_mtime_ns
    assert after != before
