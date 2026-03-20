---
phase: 17-v1-2-expanded-macro-signals
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - config/settings.yaml
  - src/trading_crab_lib/transforms.py
  - pipelines/01_ingest.py
  - run_pipeline.py
  - tests/unit/test_transforms.py
  - tests/unit/test_fred_config.py
  - RUNBOOK.md
  - .planning/phases/17-v1-2-expanded-macro-signals/17-SUMMARY.md
  - .planning/REQUIREMENTS.md
autonomous: true
requirements:
  - DATA-10
user_setup:
  - FRED_API_KEY in .env for integration smoke (optional in CI — mock or skip)
must_haves:
  truths:
    - "Every FRED series declared under config fred.series ingests when the API key is present (failed series logged, pipeline does not crash)."
    - "Yield-curve derived columns from add_yield_curve_features (yc_*) and/or configured FRED spread series are listed in features.initial_features and receive log/derivatives per project conventions."
    - "features.clustering_features includes the new macro inputs agreed in 17-CONTEXT (or an explicit 'supervised-only' subset is documented with REQ waiver in SUMMARY)."
    - "Causal and non-causal feature builds both see the same new columns at the appropriate engineer_all() call sites (step 2 dual outputs unchanged in contract)."
    - "Changing clustering_features triggers a documented post-recluster path: RUNBOOK.md cross-link or checklist line for regime_labels.yaml + steps 3–7."
  artifacts:
    - path: "config/settings.yaml"
      provides: "fred.series complete; features.log_columns / initial_features / clustering_features updated coherently"
    - path: "src/trading_crab_lib/transforms.py"
      provides: "add_yield_curve_features and/or cross-ratio hooks if new derived columns needed beyond existing yc_*"
    - path: "tests/unit/test_transforms.py"
      provides: "Synthetic-frame tests for new columns surviving engineer_all subset"
---

<objective>
Deliver **DATA-10** for milestone v1.2: wire **already-configured** expanded FRED series and yield-curve/spread features into the **feature selection lists** so they flow through gap-fill, derivatives, and (per decision) **PCA/clustering** and supervised artifacts — without breaking checkpoint contracts or causal discipline.

**Non-goals for this plan:** optional external data providers (**DATA-11**, Phase 22); ratio diagnostics layer (**SIGNAL-10**, Phase 18).
</objective>

<execution_context>
@.planning/phases/17-v1-2-expanded-macro-signals/17-CONTEXT.md
@.planning/REQUIREMENTS.md
@.planning/ROADMAP.md
@RUNBOOK.md
@config/settings.yaml
@src/trading_crab_lib/transforms.py
@src/trading_crab_lib/ingestion/fred.py
@pipelines/01_ingest.py
@run_pipeline.py
</execution_context>

<context>
**Inventory before coding:** Print or tabulate `cfg["fred"]["series"]` keys vs `macro_raw` / merged columns after step 1 for a dev run to confirm every series has a column after merge (multpl + FRED join).

**Redundancy:** If both **fred_t10y2y** (FRED) and **yc_10y_2y** (GS10−GS2) exist, prefer **one** for clustering to avoid double-counting the same signal unless a documented rationale says otherwise.

**Clustering:** Adding columns to `clustering_features` changes unsupervised geometry — **regime IDs and `regime_labels.yaml` must be revisited** after re-clustering (see RUNBOOK).
</context>

<tasks>

<task type="auto" tdd="false">
  <name>Task 1 — Audit and lock the column list</name>
  <read_first>
    - config/settings.yaml (fred.series, features.*)
    - src/trading_crab_lib/transforms.py (add_yield_curve_features, engineer_all)
  </read_first>
  <action>
    1. Build a short table (in commit message or `17-CONTEXT.md`): each FRED column name → include in `log_columns`? → `initial_features`? → `clustering_features` (which derivatives)?
    2. Confirm `add_yield_curve_features` runs before `select_features` for `initial_features` (already true in `engineer_all`).
    3. For rates in percent (e.g. fred_gs10, fred_gs2, fred_tb3ms, new fred_*): follow existing pattern (mostly derivatives in clustering, not always raw levels).
  </action>
  <acceptance_criteria>
    - Table exists in `17-CONTEXT.md` or plan appendix with at least one decision on **fred_t10y2y** vs **yc_10y_2y**.
  </acceptance_criteria>
</task>

<task type="auto" tdd="true">
  <name>Task 2 — Update settings.yaml feature lists</name>
  <read_first>
    - config/settings.yaml
  </read_first>
  <action>
    1. Add new columns to `features.log_columns` where log transform is appropriate (mirror similar series — e.g. positive levels).
    2. Add the same columns to `initial_features` so they survive step 3 of `engineer_all`.
    3. Add corresponding `*_d1`, `*_d2` (and `*_d3` only where project convention applies — see existing `clustering_features` for sp500) to `clustering_features` for selected macro signals.
    4. If any new column is **supervised-only** (not in clustering), document in `17-CONTEXT.md` and ensure it still appears in **features_supervised** path when causal=True.
  </action>
  <acceptance_criteria>
    - `python -c "from trading_crab_lib.config import load; c=load(); print(len(c['features']['clustering_features']))"` runs without error (see `trading_crab_lib/config.py`).
    - No duplicate logical spread in `clustering_features` without comment in YAML.
  </acceptance_criteria>
</task>

<task type="auto" tdd="true">
  <name>Task 3 — Unit tests: transforms + synthetic macro frame</name>
  <read_first>
    - tests/unit/test_transforms.py (if exists; else create minimal)
    - src/trading_crab_lib/transforms.py
  </read_first>
  <action>
    1. Add or extend tests that build a small quarterly DataFrame with required multpl + FRED columns + **new** columns, then run `engineer_all` with a **minimal** config fragment (or full `load()` with test overrides) and assert:
       - No exception.
       - New clustering feature names exist in output columns when present in cfg.
    2. Add a focused test for `add_yield_curve_features` when `fred_gs10`, `fred_gs2`, `fred_tb3ms` present (already partially covered — extend if new branches).
  </action>
  <acceptance_criteria>
    - `pytest tests/unit/test_transforms.py -q` passes (or new file `tests/unit/test_engineer_all_v12_macro.py`).
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 4 — Ingest + smoke (optional)</name>
  <read_first>
    - src/trading_crab_lib/ingestion/fred.py
  </read_first>
  <action>
    1. If `tests/test_fred.py` or similar exists, add a test that **mocks** `fredapi` and asserts `fetch_all` requests each series ID in config.
    2. Otherwise document manual smoke: `python run_pipeline.py --steps 1,2 --recompute` with `FRED_API_KEY` set.
  </action>
  <acceptance_criteria>
    - At least one of: new mock test **or** manual smoke note in `17-SUMMARY.md`.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 5 — RUNBOOK + traceability</name>
  <read_first>
    - RUNBOOK.md
    - .planning/REQUIREMENTS.md
  </read_first>
  <action>
    1. Add a short subsection or bullet under **Checkpoint hygiene** / **After re-clustering** that expanding **FRED / clustering_features** requires the same **steps 3–7 + regime_labels** discipline as other feature changes.
    2. Update **REQUIREMENTS.md** traceability row for **DATA-10**: Phase 17 → **Complete** when this plan is executed.
  </action>
  <acceptance_criteria>
    - `grep -n "clustering_features\\|regime_labels" RUNBOOK.md` shows new or updated line.
  </acceptance_criteria>
</task>

</tasks>

<verification>

## Automated

- `pytest tests/unit/test_transforms.py tests/unit/test_regime.py -q` (adjust paths to actual new tests)
- `python -c "from trading_crab_lib.config import load; load()"`

## Manual

- With API key: `python run_pipeline.py --steps 1,2 --recompute` and inspect `data/processed/features.parquet` (or checkpoints) for new columns.
- If **clustering_features** changed: run steps **3–7** and refresh **`config/regime_labels.yaml`** per RUNBOOK.

</verification>
