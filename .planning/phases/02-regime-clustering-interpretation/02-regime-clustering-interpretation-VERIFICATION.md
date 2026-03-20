---
phase: 02-regime-clustering-interpretation
verified: 2026-03-20T00:00:00Z
status: passed
score: 6/6 automated truths verified (visual interpretability — see human_verification)
gaps: []
human_verification:
  - test: "Visual inspection of regime profiles and clustering stability across reruns."
    expected: "For a fixed feature set and clustering configuration, the number of regimes (~4–7), their macro profiles, and their suggested/human-assigned names remain stable across repeated runs; profiles are interpretable in terms of growth, inflation, rates, and risk."
    why_human: "Requires subjective assessment of plot outputs and narrative fit of regime names; cannot be evaluated via unit tests or static analysis."
---

## Notes: VERIFICATION vs VALIDATION

- **`02-regime-clustering-interpretation-VERIFICATION.md` (this file)** records roadmap-level **truth tables** and **product evidence** against REGIME-*. Frontmatter **`status: passed`** reflects closure of automated REGIME-02/03 evidence in **Phase 15** (macro vs ETF artifact split + pinned `regime_labels.yaml`). **Truth 6 (visual)** is still **human-only** — see `human_verification` below (does not reopen `gaps_found`).
- **`02-VALIDATION.md`** is the **Nyquist-style automated test contract** (Wave map, pytest commands). Its frontmatter `nyquist_compliant: true` is the sampling-plan lens; this VERIFICATION file is the requirement-evidence lens.
- **How to read both:** Use this file for REQ status; use VALIDATION for pytest commands after Phase 2 code changes.

# Phase 2: Regime Clustering & Interpretation Verification Report

**Phase Goal:** Produce a small, stable set of interpretable market regimes with reproducible profiles and names that downstream models and users can rely on.
**Verified:** 2026-03-20
**Status:** passed
**Re-verification:** Phase 15 gap closure (REGIME-02/03)

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
| --- | ----- | ------ | -------- |
| 1 | Historical quarters are assigned to a manageable number of regimes (target ~4–7) using the Phase 1 feature set and PCA + clustering. | ✓ VERIFIED | `pipelines/03_cluster.py` drives PCA and KMeans via `config.settings["clustering"]`, with `k_cap` and `balanced_k` both set to 5, so the pipeline always produces a small number of regimes; `tests/unit/test_clustering.py` asserts correct cluster counts and label canonicalization. |
| 2 | Re-running the clustering step with the same configuration and input features produces identical regime labels for all quarters. | ✓ VERIFIED | `reduce_pca`, `evaluate_kmeans`, and `fit_clusters` all use a fixed `random_state` from config and canonicalize labels based on mean PC1; tests cover deterministic, contiguous label ordering, making label assignments stable given fixed inputs. |
| 3 | The clustering step writes regime artifacts under `data/regimes/` that downstream steps and notebooks can reload without ad-hoc logic. | ✓ VERIFIED | `pipelines/03_cluster.py` writes `cluster_labels.parquet`, `pca_components.parquet`, and `kmeans_scores.parquet` with stable schemas, and these paths are referenced by downstream profiling code; artifacts are runtime outputs and correctly gitignored. |
| 4 | Each regime has a reproducible profile over key macro features and ETF returns that supports a human-readable description. | ✓ VERIFIED | **Macro:** `profiles.parquet` via `build_profiles` / step 4 (`tests/unit/test_regime.py`). **ETF/proxy returns by regime:** `data/regimes/etf_behavior_by_regime.parquet` via `behavior_tables()` / step 6; contract guarded by `tests/unit/test_regime_etf_profile_artifact.py`. Canonical split documented in `src/trading_crab_lib/regime.py` module docstring (*Regime artifacts (macro vs ETF)*). |
| 5 | There is a stable, version-controlled mapping from canonicalized cluster IDs to human-readable regime names, applied consistently across runs. | ✓ VERIFIED | `config/regime_labels.yaml` pins **balanced_cluster** IDs **0–4** (`clustering.balanced_k=5`); `load_name_overrides` + `tests/unit/test_regime.py` cover merge with `suggest_names`. |
| 6 | Downstream supervised models and reporting code can load regime profiles, transition matrices, and label mappings from disk without re-running notebooks. | ✓ VERIFIED | `pipelines/04_regime_label.py` writes `profiles.parquet`, `transition_matrix.parquet`, and `regime_names_suggested.yaml`, and all profiling, naming, and transition logic lives in `trading_crab_lib.regime` with unit tests in `tests/unit/test_regime.py`, making these artifacts reproducible and notebook-independent. |

**Score:** 6/6 automated truths verified (visual check still manual — `human_verification`)

### Required Artifacts

| Artifact | Expected | Status | Details |
| -------- | -------- | ------ | ------- |
| `data/regimes/cluster_labels.parquet` | Quarter-level regime labels with both `cluster` and `balanced_cluster` (and optional `market_code`). | ✓ VERIFIED (by implementation) | Written by `pipelines/03_cluster.py` using `fit_clusters`; tests confirm label shapes and canonicalization, though the file itself is a runtime artifact and not present in git. |
| `data/regimes/pca_components.parquet` | Quarter-level PCA components PC1…PCn used for clustering and diagnostics. | ✓ VERIFIED (by implementation) | `pipelines/03_cluster.py` drops label columns and persists remaining PC columns; schema matches `reduce_pca` output. |
| `data/regimes/kmeans_scores.parquet` | k-sweep evaluation table (`k`, `inertia`, `silhouette`, `calinski`, `davies_bouldin`). | ✓ VERIFIED (by implementation) | `evaluate_kmeans` returns the full score table and `03_cluster.py` writes it with `index=False`; tests assert expected columns. |
| `data/regimes/profiles.parquet` | Per-regime descriptive statistics over Phase 1 **feature** columns (macro/engineered). | ✓ VERIFIED | Produced by `pipelines/04_regime_label.py` via `build_profiles`; ETF behavior lives in `etf_behavior_by_regime.parquet` (step 6), not merged into this table by design (see `regime.py` docstring). |
| `data/regimes/transition_matrix.parquet` | Empirical one-step transition probabilities between regimes. | ✓ VERIFIED | Written by `pipelines/04_regime_label.py` using `build_transition_matrix`; tests confirm probability semantics and row sums. |
| `data/regimes/regime_names_suggested.yaml` | Auto-suggested regime names (after applying overrides) for human review. | ✓ VERIFIED | Written by `pipelines/04_regime_label.py` from `suggest_names` merged with `load_name_overrides`; deterministic given fixed data and config. |
| `config/regime_labels.yaml` | Pinned mapping for IDs **0–4** (`balanced_k=5`). | ✓ VERIFIED | Active keys 0–4 with human-readable strings; Phase 15 closure. |
| `tests/unit/test_clustering.py` | Unit tests for PCA + KMeans clustering and artifact creation. | ✓ VERIFIED | Present and exercises `reduce_pca`, `evaluate_kmeans`, `pick_best_k`, and `fit_clusters`, including canonicalization and fallback behavior. |
| `tests/unit/test_regime.py` | Unit tests for regime profiles, naming, transitions, and overrides. | ✓ VERIFIED | Present and covers `build_profiles`, `suggest_names`, `build_transition_matrix`, and `load_name_overrides` on synthetic data. |

### Key Link Verification

| From | To | Via | Status | Details |
| ---- | -- | --- | ------ | ------- |
| `pipelines/03_cluster.py` | `src/trading_crab_lib/clustering.py` | `reduce_pca, evaluate_kmeans, pick_best_k, fit_clusters` | ✓ VERIFIED | Imports from `trading_crab_lib.clustering` and uses all four core functions to implement the clustering pipeline. |
| `pipelines/03_cluster.py` | `config/settings.yaml` | `clustering.* configuration` | ✓ VERIFIED | Loads config via `load()` and reads `cfg["clustering"]` for `n_pca_components`, `n_clusters_search`, `k_cap`, `balanced_k`, and `random_state`; no clustering constants are hardcoded. |
| `tests/unit/test_clustering.py` | `src/trading_crab_lib/clustering.py` | Direct imports of clustering helpers | ✓ VERIFIED | Imports and exercises `reduce_pca`, `evaluate_kmeans`, `pick_best_k`, and `fit_clusters` with synthetic data, including canonicalization behavior. |
| `pipelines/04_regime_label.py` | `src/trading_crab_lib/regime.py` | `build_profiles, suggest_names, build_transition_matrix, load_name_overrides` | ✓ VERIFIED | Imports all four utilities and uses them to produce profiles, suggested names, overrides, and the transition matrix. |
| `pipelines/04_regime_label.py` | `config/regime_labels.yaml` | Manual name overrides layered on auto-suggestions | ✓ VERIFIED | Calls `load_name_overrides(CONFIG_DIR)` and merges overrides into `regime_names_suggested.yaml`. |
| `tests/unit/test_regime.py` | `src/trading_crab_lib/regime.py` | Direct imports and synthetic fixtures | ✓ VERIFIED | Imports regime utilities and validates their behavior on synthetic data, matching the validation strategy. |

### Requirements Coverage

| Requirement | Description | Status | Evidence |
| ----------- | ----------- | ------ | -------- |
| REGIME-01 | Cluster quarters into a small, interpretable set of regimes using PCA + KMeans, targeting ~4–7 regimes. | PASS | Clustering is entirely config-driven via `settings.yaml` with `n_pca_components=5`, `k_cap=5`, and `balanced_k=5`; `pipelines/03_cluster.py` and `clustering.fit_clusters` implement this pipeline, and `tests/unit/test_clustering.py` guards core behavior and label determinism. |
| REGIME-02 | For each regime, compute descriptive statistics over key macro features and ETF returns in reproducible code. | PASS | Macro: `profiles.parquet` / `build_profiles` / `tests/unit/test_regime.py`. ETF/proxy: `etf_behavior_by_regime.parquet` / `behavior_tables` / `tests/unit/test_regime_etf_profile_artifact.py`. |
| REGIME-03 | Provide a stable, version-controlled mapping from cluster IDs to human-readable regime names. | PASS | Pinned `config/regime_labels.yaml` (IDs 0–4); `load_name_overrides`, `tests/unit/test_regime.py`. |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| ---- | ---- | ------- | -------- | ------ |
| — | — | *None blocking REGIME-02/03 after Phase 15.* | — | — |

### Residual (manual)

See **`human_verification`** in YAML frontmatter: notebook/plot review for regime interpretability and visual stability across reruns (subjective; not required for `status: passed` on automated truths).

---

_Verified: 2026-03-20_
_Verifier: Phase 15 execution (gap closure)_

