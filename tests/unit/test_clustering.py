"""Unit tests for src/trading_crab_lib/clustering/kmeans.py"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from trading_crab_lib.clustering import (
    build_clustering_manifest,
    evaluate_kmeans,
    fit_clusters,
    pick_best_k,
    reduce_pca,
)


@pytest.fixture
def feature_df(quarterly_index):
    """70-quarter, 10-column feature matrix (no NaNs) for clustering tests."""
    rng = np.random.default_rng(42)
    n = 70
    index = pd.date_range("2000-03-31", periods=n, freq="QE")
    return pd.DataFrame(
        rng.standard_normal((n, 10)),
        index=index,
        columns=[f"f{i}" for i in range(10)],
    )


# ── reduce_pca ─────────────────────────────────────────────────────────────


class TestReducePca:
    def test_output_shape(self, feature_df):
        pca_df, pca, scaler = reduce_pca(feature_df, n_components=5)
        assert pca_df.shape == (len(feature_df), 5)

    def test_column_names(self, feature_df):
        pca_df, _, _ = reduce_pca(feature_df, n_components=3)
        assert list(pca_df.columns) == ["PC1", "PC2", "PC3"]

    def test_index_preserved(self, feature_df):
        pca_df, _, _ = reduce_pca(feature_df, n_components=5)
        pd.testing.assert_index_equal(pca_df.index, feature_df.index)

    def test_no_nans_in_output(self, feature_df):
        pca_df, _, _ = reduce_pca(feature_df, n_components=5)
        assert not pca_df.isna().any().any()

    def test_returns_fitted_objects(self, feature_df):
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler

        _, pca, scaler = reduce_pca(feature_df, n_components=5)
        assert isinstance(pca, PCA)
        assert isinstance(scaler, StandardScaler)


# ── evaluate_kmeans ────────────────────────────────────────────────────────


class TestEvaluateKmeans:
    def test_returns_dataframe_with_expected_cols(self, feature_df):
        pca_df, _, _ = reduce_pca(feature_df, n_components=3)
        scores = evaluate_kmeans(pca_df.values, k_range=range(2, 5), n_init=5)
        assert set(scores.columns) >= {"k", "silhouette", "calinski", "davies_bouldin", "inertia"}

    def test_one_row_per_k(self, feature_df):
        pca_df, _, _ = reduce_pca(feature_df, n_components=3)
        scores = evaluate_kmeans(pca_df.values, k_range=range(2, 6), n_init=5)
        assert len(scores) == 4

    def test_silhouette_between_neg1_and_1(self, feature_df):
        pca_df, _, _ = reduce_pca(feature_df, n_components=3)
        scores = evaluate_kmeans(pca_df.values, k_range=range(2, 5), n_init=5)
        assert (scores["silhouette"] >= -1).all()
        assert (scores["silhouette"] <= 1).all()


# ── pick_best_k ────────────────────────────────────────────────────────────


class TestPickBestK:
    def test_returns_highest_silhouette(self):
        scores = pd.DataFrame(
            {
                "k": [2, 3, 4, 5],
                "silhouette": [0.2, 0.5, 0.4, 0.3],
            }
        )
        assert pick_best_k(scores, k_cap=10) == 3

    def test_cap_applied(self):
        scores = pd.DataFrame(
            {
                "k": [2, 3, 4, 5, 6, 7],
                "silhouette": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
            }
        )
        assert pick_best_k(scores, k_cap=5) == 5

    def test_cap_not_applied_when_best_below_cap(self):
        scores = pd.DataFrame(
            {
                "k": [2, 3, 4],
                "silhouette": [0.1, 0.5, 0.2],
            }
        )
        assert pick_best_k(scores, k_cap=5) == 3


# ── fit_clusters ───────────────────────────────────────────────────────────


class TestFitClusters:
    def test_both_columns_present(self, feature_df):
        pca_df, _, _ = reduce_pca(feature_df, n_components=5)
        result = fit_clusters(pca_df, best_k=3, balanced_k=5, use_constrained=False)
        assert "cluster" in result.columns
        assert "balanced_cluster" in result.columns

    def test_cluster_values_are_integers(self, feature_df):
        pca_df, _, _ = reduce_pca(feature_df, n_components=5)
        result = fit_clusters(pca_df, best_k=3, balanced_k=5, use_constrained=False)
        assert np.issubdtype(result["cluster"].dtype, np.integer)
        assert np.issubdtype(result["balanced_cluster"].dtype, np.integer)

    def test_correct_number_of_unique_clusters(self, feature_df):
        pca_df, _, _ = reduce_pca(feature_df, n_components=5)
        result = fit_clusters(pca_df, best_k=3, balanced_k=4, use_constrained=False)
        assert result["cluster"].nunique() == 3
        assert result["balanced_cluster"].nunique() == 4

    def test_index_preserved(self, feature_df):
        pca_df, _, _ = reduce_pca(feature_df, n_components=5)
        result = fit_clusters(pca_df, best_k=3, balanced_k=5, use_constrained=False)
        pd.testing.assert_index_equal(result.index, pca_df.index)

    def test_canonicalization_produces_contiguous_and_ordered_labels(self, feature_df):
        """Cluster IDs should be contiguous [0..k-1] and ordered by mean PC1."""
        pca_df, _, _ = reduce_pca(feature_df, n_components=3)
        result = fit_clusters(pca_df, best_k=3, balanced_k=3, use_constrained=False)

        for col in ["cluster", "balanced_cluster"]:
            labels = result[col]
            # Contiguous integer labels starting at 0
            assert labels.min() == 0
            assert labels.max() == labels.nunique() - 1

            # Label order should match ascending mean PC1
            means = result.groupby(col)["PC1"].mean()
            ordered_means = means.loc[sorted(means.index)]
            assert ordered_means.is_monotonic_increasing

    def test_balanced_cluster_fallback_logs_warning_and_still_creates_column(
        self, feature_df, caplog
    ):
        """When constrained KMeans is disabled, fallback still produces balanced_cluster."""
        pca_df, _, _ = reduce_pca(feature_df, n_components=5)
        with caplog.at_level("WARNING"):
            result = fit_clusters(pca_df, best_k=3, balanced_k=5, use_constrained=False)

        assert "balanced_cluster uses plain KMeans" in "\n".join(caplog.messages)
        assert "balanced_cluster" in result.columns


class TestClusteringManifest:
    def _clust_cfg(self) -> dict:
        return {
            "n_pca_components": 5,
            "n_clusters_search": 12,
            "k_cap": 5,
            "balanced_k": 5,
            "random_state": 42,
        }

    def test_manifest_is_deterministic_for_same_input(self, feature_df):
        features = feature_df.copy()
        # Ensure market_code is ignored in the manifest feature schema.
        features["market_code"] = 0

        m1 = build_clustering_manifest(
            features,
            self._clust_cfg(),
            use_constrained_requested=True,
            constrained_available=False,
        )
        m2 = build_clustering_manifest(
            features,
            self._clust_cfg(),
            use_constrained_requested=True,
            constrained_available=False,
        )

        assert m1 == m2
        assert m1["feature_columns"] == sorted([c for c in feature_df.columns])

    def test_manifest_changes_when_feature_schema_changes(self, feature_df):
        features = feature_df.copy()
        features["market_code"] = 0

        m1 = build_clustering_manifest(
            features,
            self._clust_cfg(),
            use_constrained_requested=True,
            constrained_available=False,
        )

        # Add a new feature column (no NaNs) — manifest feature_columns must change.
        features2 = features.copy()
        features2["extra_feature"] = 1.0
        m2 = build_clustering_manifest(
            features2,
            self._clust_cfg(),
            use_constrained_requested=True,
            constrained_available=False,
        )

        assert m1 != m2
        assert "extra_feature" in m2["feature_columns"]

    def test_manifest_changes_when_clustering_config_changes(self, feature_df):
        features = feature_df.copy()
        features["market_code"] = 0

        cfg1 = self._clust_cfg()
        cfg2 = dict(cfg1)
        cfg2["balanced_k"] = 4

        m1 = build_clustering_manifest(
            features,
            cfg1,
            use_constrained_requested=True,
            constrained_available=False,
        )
        m2 = build_clustering_manifest(
            features,
            cfg2,
            use_constrained_requested=True,
            constrained_available=False,
        )

        assert m1 != m2
        assert m1["clustering_config"]["balanced_k"] == 5
        assert m2["clustering_config"]["balanced_k"] == 4
