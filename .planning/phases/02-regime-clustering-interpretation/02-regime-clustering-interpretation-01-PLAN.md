---
phase: 02-regime-clustering-interpretation
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - pipelines/03_cluster.py
  - src/market_regime/clustering.py
  - tests/unit/test_clustering.py
autonomous: true
requirements:
  - REGIME-01
must_haves:
  truths:
    - Historical quarters are assigned to a manageable number of regimes (target ~4–7) using the Phase 1 feature set and PCA + clustering.
    - Re-running the clustering step with the same configuration and input features produces identical regime labels for all quarters.
    - Reclustering does not happen implicitly on every run; it occurs only when inputs/config intentionally change (or when explicitly forced).
    - The clustering step writes regime artifacts under data/regimes/ that downstream steps and notebooks can reload without ad-hoc logic.
  artifacts:
    - path: data/regimes/cluster_labels.parquet
      provides: "Quarter-level regime labels with both cluster and balanced_cluster and optional market_code."
    - path: data/regimes/pca_components.parquet
      provides: "Quarter-level PCA components (PC1…PCn) used for clustering and diagnostics."
    - path: data/regimes/kmeans_scores.parquet
      provides: "k-sweep evaluation table (k, inertia, silhouette, calinski, davies_bouldin) used to select best_k."
    - path: data/regimes/clustering_manifest.json
      provides: "Deterministic fingerprint of clustering inputs (feature schema/date window) + clustering config; used to enforce the 'recluster only on intentional change' policy."
  key_links:
    - from: pipelines/03_cluster.py
      to: src/market_regime/clustering.py
      via: "reduce_pca, evaluate_kmeans, pick_best_k, fit_clusters"
      pattern: "from market_regime.clustering import"
    - from: pipelines/03_cluster.py
      to: data/regimes/clustering_manifest.json
      via: "manifest comparison to skip unintentional reclustering"
      pattern: "clustering_manifest.json"
    - from: tests/unit/test_clustering.py
      to: src/market_regime/clustering.py
      via: "direct imports of reduce_pca/evaluate_kmeans/fit_clusters and synthetic data fixtures"
      pattern: "from market_regime.clustering import"
---

<objective>
Harden the unsupervised clustering step so that it produces deterministic, reproducible regime labels and core regime artifacts under data/regimes/, and enforces the Phase 2 locked policy: **recluster only on intentional change**.

Purpose: Satisfy REGIME-01 by ensuring that quarter-level regime assignments are stable, interpretable, and wired through the canonical clustering stack, while avoiding label churn from accidental/clandestine reclustering.
Output: Updated clustering pipeline and tests that reliably write cluster artifacts and a manifest (`clustering_manifest.json`) used to skip recomputation when inputs are unchanged.
</objective>

<execution_context>
@.planning/ROADMAP.md
@.planning/REQUIREMENTS.md
@.planning/phases/02-regime-clustering-interpretation/02-CONTEXT.md
@.planning/phases/02-regime-clustering-interpretation/02-RESEARCH.md
@CLAUDE.md
</execution_context>

<context>
@pipelines/03_cluster.py
@src/market_regime/clustering.py
@tests/unit/test_clustering.py
</context>

<tasks>

<task type="auto">
  <name>Task 1: Deterministic clustering artifacts + intentional recluster policy</name>
  <files>pipelines/03_cluster.py, src/market_regime/clustering.py, tests/unit/test_clustering.py</files>
  <read_first>
  - .planning/phases/02-regime-clustering-interpretation/02-CONTEXT.md (locked reclustering policy)
  - pipelines/03_cluster.py (current behavior always reclusters)
  - src/market_regime/clustering.py (canonicalization + determinism)
  </read_first>
  <action>
  Implement the locked policy “recluster only on intentional change” without changing the underlying clustering math:

  1) Add a deterministic clustering-input fingerprint + manifest writer.
     - In src/market_regime/clustering.py add a helper function:
       - Name: build_clustering_manifest(...)
       - Output: dict[str, object] that includes:
         - features schema: sorted column list (excluding market_code), dtypes as strings
         - features index start/end as strings (PeriodIndex should stringify cleanly)
         - row count
         - clustering config subset used: n_pca_components, n_clusters_search, k_cap, balanced_k, random_state
         - settings hash: md5(settings.yaml)[:8]
     - Write this dict to data/regimes/clustering_manifest.json (sorted keys; stable formatting).

  2) Skip unintentional reclustering in pipelines/03_cluster.py.
     - Add argparse with:
       - --force (default false): recompute even if manifest matches
     - Before PCA:
       - Compute current manifest from the loaded features DF + cfg["clustering"] subset.
       - If NOT --force and all outputs exist (cluster_labels.parquet, pca_components.parquet, kmeans_scores.parquet) and clustering_manifest.json exists and equals current manifest:
         - Print a single-line message explaining the skip and how to force.
         - Exit 0.
     - After writing parquet artifacts:
       - Write/update clustering_manifest.json to reflect the run inputs/config.

  3) Extend unit tests to cover the manifest function (pure, fast).
     - In tests/unit/test_clustering.py add:
       - Determinism: two calls on same synthetic inputs produce identical dicts.
       - Sensitivity: changing a single config field or adding a column changes the dict.
     - Keep tests independent of real data files and independent of filesystem.
  </action>
  <acceptance_criteria>
  - `python pipelines/03_cluster.py` run twice in a row with unchanged inputs/config clusters only on the first run; the second run skips reclustering unless `--force` is provided.
  - The manifest changes when (and only when) the feature schema/date range changes or clustering config changes.
  - `pytest tests/unit/test_clustering.py -q` passes.
  </acceptance_criteria>
  <verify>
  <automated>pytest tests/unit/test_clustering.py -q</automated>
  <automated>python pipelines/03_cluster.py</automated>
  <automated>python pipelines/03_cluster.py</automated>
  <automated>python pipelines/03_cluster.py --force</automated>
  </verify>
  <done>
  - `data/regimes/clustering_manifest.json` is written and includes: sorted feature column list (excluding `market_code`), index start/end, row count, clustering config subset, and an 8-char settings hash.
  - A second run of `python pipelines/03_cluster.py` with unchanged inputs prints a skip message and exits 0 without rewriting parquet outputs unless `--force` is provided.
  - `pytest tests/unit/test_clustering.py -q` passes and includes at least one test that changes a single config field or adds a column and observes a manifest change.
  </done>
</task>

</tasks>

<verification>
- Running pytest tests/unit/test_clustering.py -q passes, confirming that PCA reduction, k-sweep scoring, and clustering functions behave as expected for synthetic data and edge cases.
- Running python pipelines/03_cluster.py on the Phase 1 feature checkpoints completes without error and produces cluster_labels.parquet, pca_components.parquet, and kmeans_scores.parquet in data/regimes/.
- Re-running python pipelines/03_cluster.py without changes skips reclustering, preventing unintentional label drift.
</verification>

<success_criteria>
- REGIME-01 is supported by a deterministic, config-driven clustering pipeline that can be re-run safely as data or configuration evolves.
- The Phase 2 locked reclustering policy is enforced: labels only change when inputs/config intentionally change (or when forced).
- All downstream steps that rely on data/regimes/cluster_labels.parquet, data/regimes/pca_components.parquet, and data/regimes/kmeans_scores.parquet can treat these files as stable interfaces.
- Clustering behavior (number of regimes, label stability, artifact shapes) is guarded by unit tests and a simple pipeline run rather than implicit assumptions in notebooks.
</success_criteria>

<output>
After completion, leave this plan file in place and rely on /gsd:execute-phase 2 to run it as part of the Phase 2 execution wave. No additional SUMMARY file is required beyond the standard execute-phase summaries.
</output>

