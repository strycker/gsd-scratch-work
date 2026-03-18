---
phase: 02-regime-clustering-interpretation
plan: 03
type: execute
wave: 3
depends_on:
  - 02-regime-clustering-interpretation-01
  - 02-regime-clustering-interpretation-02
files_modified:
  - src/market_regime/regime.py
  - pipelines/04_regime_label.py
  - tests/unit/test_forward_window_probabilities.py
autonomous: true
requirements:
  - REGIME-02
  - REGIME-03
must_haves:
  truths:
    - Empirical forward-window probabilities are computed deterministically as a Phase 2 diagnostic artifact.
    - The forward-window probabilities use the same canonical regime IDs and horizons as downstream forward models, enabling MODEL-02 comparisons.
    - Downstream code can load the forward-window probabilities from disk without notebooks.
  artifacts:
    - path: data/regimes/forward_window_probabilities.parquet
      provides: "Empirical P(reach to_regime within N quarters | current=from_regime) for N in configured horizons."
    - path: tests/unit/test_forward_window_probabilities.py
      provides: "Unit tests for forward-window probability semantics and determinism."
  key_links:
    - from: pipelines/04_regime_label.py
      to: src/market_regime/regime.py
      via: "build_forward_window_probabilities(labels, horizons)"
      pattern: "build_forward_window_probabilities"
    - from: pipelines/04_regime_label.py
      to: data/regimes/forward_window_probabilities.parquet
      via: "parquet artifact write"
      pattern: "forward_window_probabilities.parquet"

---

<objective>
Add the locked Phase 2 diagnostic: **empirical forward-window regime probabilities** (legacy-style) as a reproducible artifact, wired into the standard regime labeling step and covered by unit tests.

Purpose: Support REGIME-02/03 interpretation and provide a sanity-check baseline for Phase 3 forward transition models (MODEL-02) by persisting empirical “reach within N quarters” probabilities.
Output: A deterministic `forward_window_probabilities.parquet` artifact under `data/regimes/`, produced by `pipelines/04_regime_label.py` and backed by fast unit tests.
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
@pipelines/04_regime_label.py
@config/settings.yaml
</context>

<tasks>

<task type="auto" tdd="true">
  <name>Task 1: Implement empirical forward-window probabilities (reach-within-N)</name>
  <files>src/market_regime/regime.py, tests/unit/test_forward_window_probabilities.py</files>
  <read_first>
  - .planning/phases/02-regime-clustering-interpretation/02-CONTEXT.md (locked requirement to implement this artifact in Phase 2)
  - src/market_regime/regime.py (existing build_transition_matrix conventions and label semantics)
  </read_first>
  <action>
  Add a new function to src/market_regime/regime.py with concrete semantics and a stable output shape:

  - Function name: build_forward_window_probabilities
  - Signature: build_forward_window_probabilities(cluster_labels: pd.Series, horizons: list[int]) -> pd.DataFrame
  - Input:
    - cluster_labels: integer Series of canonical regime IDs, time-ordered (dropna() before use)
    - horizons: list of positive ints (quarters) such as [1, 2, 4, 8]
  - Definition (legacy-style “reach within N”):
    - For each time t with current regime i = labels[t], and for each horizon N:
      - Look at labels[t+1 : t+N] (up to series end)
      - Mark every regime j that appears at least once in that window as “reached”
    - Probability output:
      - P(reach j within N | current i) = (# times j is reached within N when current=i) / (# valid times current=i)
    - Note: by this definition, i can be “reached” within N if the regime persists/reappears within the next N quarters.

  - Output shape (long format, stable for parquet + easy joins):
    - Columns: from_regime (int), to_regime (int), horizon_quarters (int), prob (float)
    - Include all pairs (i, j) for all observed regimes, for each horizon, even if prob=0.0.
    - Deterministic ordering: sort by horizon_quarters, then from_regime, then to_regime.

  Add new tests in tests/unit/test_forward_window_probabilities.py:
  - Build a tiny synthetic label sequence with known reachability within 1 and 2 quarters, e.g. labels = [0, 1, 1, 2, 0].
  - Assert:
    - Output contains expected rows and columns
    - Probabilities match hand calculations for at least one (from,to,horizon) triple
    - All prob values are within [0, 1]
    - Determinism: calling twice yields identical DataFrame (after sorting)
  </action>
  <acceptance_criteria>
  - src/market_regime/regime.py exports build_forward_window_probabilities with the exact semantics above.
  - tests/unit/test_forward_window_probabilities.py passes and validates reach-within-N probabilities for a known toy sequence.
  - `pytest tests/unit/test_forward_window_probabilities.py -q` passes.
  </acceptance_criteria>
  <verify>
  <automated>pytest tests/unit/test_forward_window_probabilities.py -q</automated>
  </verify>
  <done>
  - `build_forward_window_probabilities(cluster_labels, horizons)` exists in `src/market_regime/regime.py` and returns a long-format DataFrame with columns: `from_regime`, `to_regime`, `horizon_quarters`, `prob`.
  - For a fixed synthetic label sequence, the unit test asserts at least one hand-computed probability for a specific (from,to,horizon) triple.
  - All returned probabilities are within \([0, 1]\) and output ordering is deterministic after sorting by horizon, from_regime, to_regime.
  </done>
</task>

<task type="auto">
  <name>Task 2: Wire the forward-window probabilities artifact into step 04</name>
  <files>pipelines/04_regime_label.py</files>
  <read_first>
  - pipelines/04_regime_label.py (current artifacts written)
  - config/settings.yaml (source of forward horizons; use the same horizons as Phase 3 classifiers)
  </read_first>
  <action>
  Extend pipelines/04_regime_label.py to compute and persist the forward-window probabilities artifact:

  - Import build_forward_window_probabilities from market_regime.regime.
  - Determine horizons from config, using this precedence:
    1) cfg["prediction"]["forward_horizons_quarters"] if present (preferred: aligns with MODEL-02 horizons)
    2) Fallback default: [1, 2, 4, 8]
  - After writing transition_matrix.parquet, compute:
    forward_probs = build_forward_window_probabilities(labels, horizons)
  - Write:
    data/regimes/forward_window_probabilities.parquet
  - Print/log a small diagnostic excerpt (e.g. for horizon=1 and horizon=max) to make the artifact discoverable in CLI runs.

  Do NOT merge ETF return statistics into profiles.parquet here (locked boundary: macro profiles separate).
  </action>
  <acceptance_criteria>
  - Running `python pipelines/03_cluster.py --force && python pipelines/04_regime_label.py` creates `data/regimes/forward_window_probabilities.parquet`.
  - The horizons used match cfg["prediction"]["forward_horizons_quarters"] when present.
  - The artifact uses canonical regime IDs (same IDs as balanced_cluster) and is deterministic across reruns with unchanged labels.
  </acceptance_criteria>
  <verify>
  <automated>python pipelines/03_cluster.py --force && python pipelines/04_regime_label.py</automated>
  <automated>pytest tests/unit/test_forward_window_probabilities.py -q</automated>
  </verify>
  <done>
  - `pipelines/04_regime_label.py` imports and calls `build_forward_window_probabilities` and writes `data/regimes/forward_window_probabilities.parquet`.
  - The horizons used equal `cfg[\"prediction\"][\"forward_horizons_quarters\"]` when that key exists; otherwise it uses the fallback list documented in the task action.
  - Re-running step 04 with unchanged labels produces identical forward-window probabilities (deterministic artifact given deterministic inputs).
  </done>
</task>

</tasks>

<verification>
- `pytest tests/unit/test_forward_window_probabilities.py -q` passes.
- `python pipelines/03_cluster.py --force && python pipelines/04_regime_label.py` produces `data/regimes/forward_window_probabilities.parquet` alongside existing Phase 2 regime artifacts.
- Re-running step 04 without changes yields identical forward-window probabilities (deterministic artifact given deterministic labels).
</verification>

<success_criteria>
- Phase 2 produces a diagnostic empirical forward-window probability artifact usable as a baseline sanity check for Phase 3 MODEL-02 transition classifiers.
- The artifact is stable, deterministic, and uses the same regime IDs and horizons as downstream modeling code.
</success_criteria>

<output>
After completion, create `.planning/phases/02-regime-clustering-interpretation/02-regime-clustering-interpretation-03-SUMMARY.md`.
</output>

