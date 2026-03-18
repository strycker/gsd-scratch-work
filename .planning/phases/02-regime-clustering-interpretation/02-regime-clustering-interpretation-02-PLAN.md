---
phase: 02-regime-clustering-interpretation
plan: 02
type: execute
wave: 2
depends_on:
  - 02-regime-clustering-interpretation-01
files_modified:
  - src/market_regime/regime.py
  - config/regime_labels.yaml
  - tests/unit/test_regime.py
autonomous: true
requirements:
  - REGIME-02
  - REGIME-03
must_haves:
  truths:
    - Each regime has a reproducible macro profile over key features that supports a human-readable description.
    - There is a stable, version-controlled mapping from canonicalized cluster IDs to human-readable regime names, applied consistently across runs.
    - Downstream supervised models and reporting code can load regime profiles, transition matrices, and label mappings from disk without re-running notebooks.
  artifacts:
    - path: data/regimes/profiles.parquet
      provides: "Per-regime descriptive statistics over the Phase 1 feature set (macro/engineered features only)."
    - path: data/regimes/transition_matrix.parquet
      provides: "Empirical one-step transition probabilities P(next=j | current=i) between regimes."
    - path: data/regimes/regime_names_suggested.yaml
      provides: "Auto-suggested regime names (after applying overrides) for human review."
    - path: config/regime_labels.yaml
      provides: "Hybrid pinning: version-controlled overrides for only stable/obvious regimes; unpinned regimes remain auto-suggested."
    - path: tests/unit/test_regime.py
      provides: "Unit tests covering build_profiles, suggest_names, build_transition_matrix, and load_name_overrides behavior required for REGIME-02 and REGIME-03."
  key_links:
    - from: pipelines/04_regime_label.py
      to: src/market_regime/regime.py
      via: "build_profiles, suggest_names, build_transition_matrix, load_name_overrides"
      pattern: "from market_regime.regime import"
    - from: pipelines/04_regime_label.py
      to: config/regime_labels.yaml
      via: "load_name_overrides + merge overrides into suggested names"
      pattern: "regime_labels.yaml"
    - from: tests/unit/test_regime.py
      to: src/market_regime/regime.py
      via: "direct imports and synthetic data fixtures for profiles, names, and transitions"
      pattern: "from market_regime.regime import"
---

<objective>
Implement and validate regime profiling, **hybrid naming governance**, and transition-matrix logic so each regime has a reproducible **macro** profile and stable human-readable names (pinned only when intentionally promoted).

Purpose: Satisfy REGIME-02 and REGIME-03 by turning canonical cluster labels into interpretable, stable regimes with a clear governance boundary:
- `profiles.parquet` remains macro-feature-focused (ETF return stats are separate artifacts from later steps).
- `config/regime_labels.yaml` uses hybrid pinning (only stable regimes are pinned; others remain auto-suggested).
Output: Updates to config/tests and any necessary small library adjustments to keep profiling/naming/transitions deterministic and policy-compliant.
</objective>

<execution_context>
@.planning/ROADMAP.md
@.planning/REQUIREMENTS.md
@.planning/phases/02-regime-clustering-interpretation/02-CONTEXT.md
@.planning/phases/02-regime-clustering-interpretation/02-RESEARCH.md
@CLAUDE.md
</execution_context>

<context>
@src/market_regime/regime.py
@config/regime_labels.yaml
@data/regimes/cluster_labels.parquet
</context>

<tasks>

<task type="auto">
  <name>Task 1: Hybrid regime pinning governance + macro-only profiling boundary</name>
  <files>config/regime_labels.yaml, src/market_regime/regime.py, tests/unit/test_regime.py</files>
  <read_first>
  - .planning/phases/02-regime-clustering-interpretation/02-CONTEXT.md (hybrid pinning; macro vs ETF separation)
  - config/regime_labels.yaml (current contents)
  - src/market_regime/regime.py (load_name_overrides + suggest_names)
  - tests/unit/test_regime.py (existing behaviors)
  </read_first>
  <action>
  Enforce the locked Phase 2 governance policies as explicit, tested contracts:

  1) Hybrid pinning (REGIME-03).
     - Update config/regime_labels.yaml so it is a real override map (not commented-only), but ONLY pins stable/obvious regimes.
     - Leave at least one regime intentionally unpinned to preserve the “hybrid” nature.
     - Keep the file shape as a plain YAML mapping: {cluster_id: "Human Name"}.

  2) Macro-only profiling boundary (REGIME-02).
     - Ensure build_profiles continues to describe only macro/engineered features (no ETF returns).
     - Ensure docstrings/messaging do not imply ETF-return statistics are incorporated into profiles.parquet.

  3) Tests (tight and fast).
     - Extend tests/unit/test_regime.py to assert hybrid behavior:
       - Partial overrides replace only the specified IDs; other IDs remain auto-suggested.
       - Missing override file yields {}.
  </action>
  <acceptance_criteria>
  - config/regime_labels.yaml contains at least one real pinned mapping while leaving some regimes intentionally unpinned.
  - `pytest tests/unit/test_regime.py -q` passes and includes an explicit hybrid-pinning assertion.
  - `python pipelines/03_cluster.py --force && python pipelines/04_regime_label.py` produces `data/regimes/regime_names_suggested.yaml` with pinned overrides applied and auto-suggestions present for unpinned regimes.
  </acceptance_criteria>
  <verify>
  <automated>pytest tests/unit/test_regime.py -q</automated>
  <automated>python pipelines/03_cluster.py --force && python pipelines/04_regime_label.py</automated>
  </verify>
  <done>
  - `config/regime_labels.yaml` contains at least one active mapping `{int: str}` and at least one regime is intentionally left unpinned.
  - `data/regimes/regime_names_suggested.yaml` contains pinned names for overridden IDs and auto-suggested names for at least one unpinned ID.
  - `pytest tests/unit/test_regime.py -q` passes and includes an assertion that partial overrides do not replace non-overridden regime names.
  </done>
</task>

</tasks>

<verification>
- pytest tests/unit/test_regime.py -q passes, providing coverage for build_profiles, suggest_names, build_transition_matrix, and load_name_overrides on synthetic data.
- Running python pipelines/03_cluster.py &amp;&amp; python pipelines/04_regime_label.py on the Phase 1 outputs writes profiles.parquet, transition_matrix.parquet, and regime_names_suggested.yaml under data/regimes/ without errors.
- Inspecting regime_names_suggested.yaml and config/regime_labels.yaml shows a stable mapping from canonical regime IDs to human-readable names, and transition_matrix.parquet rows sum to 1 within numerical tolerance.
</verification>

<success_criteria>
- REGIME-02 is satisfied: every regime has a reproducible MACRO profile and transition structure encoded in profiles.parquet and transition_matrix.parquet.
- REGIME-03 is satisfied: a version-controlled config/regime_labels.yaml supports HYBRID pinning (partial overrides) and deterministic naming across runs with the same data and configuration.
- Downstream phases (supervised models, portfolio analysis, recommendations) can rely on these artifacts as stable interfaces to regime semantics.
</success_criteria>

<output>
After completion, this plan will be executed as part of /gsd:execute-phase 2, producing regime profiles, transitions, and a stable naming configuration. No additional documentation beyond the standard Phase 2 SUMMARY files is required unless new gaps are discovered during execution.
</output>

