# Phase 2: Regime Clustering & Interpretation - Context

**Gathered:** 2026-03-18  
**Status:** Ready for planning / execution updates

<domain>
## Phase Boundary

Phase 2 hardens and interprets the **quarterly market regime labels** produced from the Phase 1 feature set:

- Deterministic PCA + clustering (including balanced clustering) and stable quarter → regime assignments
- Reproducible regime profiling and transitions
- Stable, human-meaningful regime naming via pinned overrides

</domain>

<decisions>
## Implementation Decisions

### Reclustering policy (label stability)
- **Recluster only on intentional change** (recommended/locked):
  - Recompute regimes only when the **feature schema**, **date window**, or **clustering configuration** changes.
  - Do **not** treat reclustering as an automatic “fresh data every run” behavior.
- When reclustering happens, treat any regime ID/name drift as a **deliberate change** that should be reflected in:
  - updated artifacts under `data/regimes/`
  - and, when needed, updated pinned names in `config/regime_labels.yaml`

### Regime naming governance (`config/regime_labels.yaml`)
- **Hybrid pinning policy**:
  - Pin **only the stable/obvious regimes** into `config/regime_labels.yaml`.
  - Allow remaining regimes to remain auto-suggested (from `suggest_names()`), with the expectation that they may later be pinned once stable.
- Any rename of a pinned regime is an explicit, reviewable change (PR-level intent), not an incidental refactor.

### Empirical forward-window probabilities (legacy-style diagnostic)
- **Yes: implement and persist empirical forward-window probabilities in Phase 2** as a diagnostic artifact.
- This is in addition to the existing 1-step `transition_matrix.parquet`.
- Intended meaning: empirical probability of **reaching regime j within N quarters** given current regime i.

### Profiles artifact contract (`profiles.parquet`)
- **Keep macro profiles and ETF-return stats as separate artifacts**:
  - `data/regimes/profiles.parquet` remains macro-feature-focused.
  - ETF-return-by-regime stays in its own artifact(s) (e.g. `data/regimes/asset_return_profile.parquet` from the assets step).

### Claude’s discretion
- Exact set of horizons (N quarters) for forward-window empirical probabilities, as long as it’s consistent with the rest of the pipeline (typical: 1/4/8Q) and is clearly named in outputs.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing Phase 2 changes.**

### Planning + requirements
- `.planning/ROADMAP.md` — Phase boundary + REGIME-* success criteria
- `.planning/REQUIREMENTS.md` — `REGIME-01`, `REGIME-02`, `REGIME-03` definitions
- `.planning/phases/02-regime-clustering-interpretation/02-RESEARCH.md` — Phase 2 research + pitfalls
- `.planning/phases/02-regime-clustering-interpretation/02-regime-clustering-interpretation-01-PLAN.md` — clustering artifacts + determinism plan
- `.planning/phases/02-regime-clustering-interpretation/02-regime-clustering-interpretation-02-PLAN.md` — profiling/naming/transitions plan

### Code + config (authoritative)
- `src/market_regime/clustering.py` — PCA, k-sweep, `fit_clusters`, canonicalization
- `pipelines/03_cluster.py` — writes `cluster_labels.parquet`, `pca_components.parquet`, `kmeans_scores.parquet`
- `src/market_regime/regime.py` and `src/market_regime/regime/` — profiles, naming, transitions (and future forward-window probabilities)
- `pipelines/04_regime_label.py` — writes `profiles.parquet`, `transition_matrix.parquet`, `regime_names_suggested.yaml`
- `config/settings.yaml` — `clustering.*` and feature lists (`initial_features`, `clustering_features`)
- `config/regime_labels.yaml` — pinned regime name overrides
- `CLAUDE.md` — invariants (PCA=5, balanced clustering default, feature pipeline order)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable assets
- Clustering core: `reduce_pca`, `evaluate_kmeans`, `pick_best_k`, `fit_clusters` in `src/market_regime/clustering.py`
- Regime semantics: `build_profiles`, `suggest_names`, `build_transition_matrix`, `load_name_overrides` in `src/market_regime/regime.py`

### Established patterns
- Artifacts are written under `data/regimes/` and treated as stable contracts for downstream steps.
- Cluster IDs are canonicalized (mean PC1 ordering) so IDs are stable across reruns with identical inputs/config.

### Integration points
- Forward-window empirical probabilities should integrate naturally alongside:
  - `transition_matrix.parquet` (1-step)
  - and saved diagnostics under `data/regimes/` (new forward-prob artifacts)

</code_context>

<specifics>
## Specific Ideas

- Use forward-window empirical probabilities as a **sanity-check diagnostic** alongside supervised forward classifiers (Phase 3), not as a replacement.

</specifics>

<deferred>
## Deferred Ideas

- None raised during Phase 2 discussion that require a separate new capability phase.

</deferred>

---

*Phase: 02-regime-clustering-interpretation*  
*Context gathered: 2026-03-18*

