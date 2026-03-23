---
phase: 20-v1-2-tactics-layer
plan: 01
type: execute
wave: 1
depends_on:
  - 19-v1-2-boosted-models
files_modified:
  - config/settings.yaml
  - src/trading_crab_lib/tactics.py
  - src/trading_crab_lib/reporting.py
  - pipelines/09_tactics.py
  - run_pipeline.py
  - tests/test_tactics.py
  - RUNBOOK.md
  - .planning/REQUIREMENTS.md
  - .planning/phases/20-v1-2-tactics-layer/20-SUMMARY.md
autonomous: true
requirements:
  - TACTICS-10
user_setup:
  - Checkpoints from steps 3 and 6 for optional full step-9 smoke; unit tests use synthetic prices only
must_haves:
  truths:
    - "tactics_signals.parquet includes as_of (and quarter identifier) plus existing per-asset metrics; rows remain one per asset per run keyed by asset + snapshot time."
    - "classify_tactics uses a configurable multi-horizon volatility aggregate (e.g. max across vol_*) instead of only the middle vol column; behavior documented in settings.yaml."
    - "entry_bias_score (or equivalent) and soft_stop_z (rolling-mean z-score proxy) columns exist when enabled in tactics config; no broker execution."
    - "write_weekly_report_md surfaces enriched tactics bullets when configured and parquet columns exist."
    - "pytest tests/test_tactics.py passes with synthetic fixtures covering new label/column logic."
  artifacts:
    - path: "config/settings.yaml"
      provides: "tactics multi_horizon vol_agg entry_bias soft_stop_proxy classification_version"
    - path: "src/trading_crab_lib/tactics.py"
      provides: "as_of quarter_end entry_bias_score soft_stop_z multi-horizon classify"
    - path: "src/trading_crab_lib/reporting.py"
      provides: "optional Tactics subsection for bias / soft-stop summary"
    - path: "tests/test_tactics.py"
      provides: "deterministic tests for v1_2 classification paths"
---

<objective>
Close **TACTICS-10** for v1.2: enrich the existing step-9 tactics layer with **multi-horizon** classification, **weekly-entry bias** and **soft-stop proxy** columns, **as-of / quarter** snapshot metadata, **weekly report** hooks, and **unit tests** — without adding auto-execution or a new pipeline step number.
</objective>

**Non-goals:** Real anchored VWAP with intraday volume; changing step index; broker APIs.

<execution_context>
@.planning/phases/20-v1-2-tactics-layer/20-CONTEXT.md
@.planning/REQUIREMENTS.md
@.planning/ROADMAP.md
@RUNBOOK.md
@config/settings.yaml
@src/trading_crab_lib/tactics.py
@src/trading_crab_lib/reporting.py
@pipelines/09_tactics.py
@run_pipeline.py
@tests/test_tactics.py
</execution_context>

<context>
**Regression guard:** Run `PYTHONPATH=src python -m pytest tests/test_tactics.py -q` after each task cluster.

**Compatibility:** Default `classification_version: "v1"` preserves current labels; set `"v1_2"` in YAML to activate multi-horizon classification — document any bucket shifts in `20-SUMMARY.md`.
</context>

<tasks>

<task type="auto" tdd="true">
  <name>Task 1 — Config + metrics: as_of, quarter, soft-stop proxy, entry inputs</name>
  <read_first>
    - config/settings.yaml (tactics block ~line 520)
    - src/trading_crab_lib/tactics.py (full file)
    - pipelines/09_tactics.py (how prices index is used)
  </read_first>
  <action>
    1. Under `tactics:` add YAML keys with documented defaults:
       - `classification_version: "v1"` (default — preserves legacy behavior); set `"v1_2"` to enable multi-horizon aggregate + new columns in classification.
       - `vol_aggregate: "max"` — one of `max`, `median`, `mean` — used to combine `vol_*` for band logic in v1_2.
       - `entry_bias: { short_slope_window: 5, long_slope_window: 20 }` — windows must exist in `trend_windows` or add **5** to default `trend_windows` list `[5, 20, 60]` for tactics only.
       - `soft_stop_proxy: { enabled: true, window: 20 }` — z-score of last close vs rolling mean of close over `window` (per asset).
    2. In `compute_tactics_metrics`, capture `as_of` = `prices.index.max()` (normalize to `pd.Timestamp`); `quarter_end` = that timestamp normalized to period-Q end (`as_of` + `to_period('Q').end_time` or equivalent).
    3. Add per-row columns: `as_of`, `quarter_end` (ISO date string or datetime64), `last_price` = last valid close, `soft_stop_z` = z-score when `soft_stop_proxy.enabled` else NaN.
    4. Compute `entry_bias_score` in `[-1, 1]` as `np.tanh(slope_short - slope_long)` using `_trend_slope` for `short_slope_window` and `long_slope_window` columns (add `slope_5` etc. by ensuring those windows are in `trend_windows`).
  </action>
  <acceptance_criteria>
    - `config/settings.yaml` contains `classification_version`, `vol_aggregate`, `entry_bias`, `soft_stop_proxy` under `tactics:`.
    - `src/trading_crab_lib/tactics.py` defines `as_of` / `quarter_end` / `last_price` / `soft_stop_z` / `entry_bias_score` on the metrics DataFrame rows (or merged before classify).
    - `python -c "from trading_crab_lib.config import load; load()"` exits 0.
  </acceptance_criteria>
</task>

<task type="auto" tdd="true">
  <name>Task 2 — Multi-horizon classification (v1_2) + parity path (v1)</name>
  <read_first>
    - src/trading_crab_lib/tactics.py (`classify_tactics`)
    - config/settings.yaml (tactics.vol_bands)
  </read_first>
  <action>
    1. Refactor `classify_tactics(metrics, cfg)`:
       - If `classification_version == "v1"`, keep existing behavior (mid vol column + first slope column).
       - If `"v1_2"`, compute `vol_eff = aggregate(vol_cols, vol_aggregate)` and use **first** slope column for primary trend (or document use of shortest trend window column for entry-friendly trend).
       - Optional config `min_corr_spy: null` — if non-null, force `stand_aside` when `corr_spy` is below that threshold (skip if null).
    2. Ensure output DataFrame still has `tactics_label` with values in `buy_hold`, `swing`, `stand_aside`.
    3. `pipelines/09_tactics.py` and `run_pipeline.step9_tactics` need no path change if API unchanged; if function signatures gain optional args, update calls.
  </action>
  <acceptance_criteria>
    - `grep -n classification_version src/trading_crab_lib/tactics.py` returns at least one match.
    - `grep -n vol_aggregate src/trading_crab_lib/tactics.py` returns at least one match.
    - `pytest tests/test_tactics.py -q` passes (tests updated in Task 3 may assert v1 vs v1_2 — if Task 3 not run yet, existing tests must still pass with defaults).
  </acceptance_criteria>
</task>

<task type="auto" tdd="true">
  <name>Task 3 — Unit tests + reporting + RUNBOOK</name>
  <read_first>
    - tests/test_tactics.py
    - src/trading_crab_lib/reporting.py (`tactics_path` block ~475)
    - RUNBOOK.md (step 9 / tactics)
  </read_first>
  <action>
    1. Extend `tests/test_tactics.py`:
       - Fixture asserting `as_of` / `quarter_end` present on output after `compute_tactics_metrics`.
       - Assert `vol_aggregate: "max"` makes a high short-window vol asset `stand_aside` when v1 would not (or document expected behavior with explicit numbers).
       - Assert `entry_bias_score` in [-1, 1] on synthetic data.
    2. In `reporting.py`, when parquet has columns `entry_bias_score` and/or `soft_stop_z`, append optional bullets under **## Tactics** (e.g. top 3 assets by entry_bias_score) guarded by `tactics.weekly_report_enrich: true` in cfg (add key default false if minimal surface).
    3. Update **RUNBOOK.md** step 9 table: new columns + `classification_version` + pytest command.
  </action>
  <acceptance_criteria>
    - `pytest tests/test_tactics.py -q` exits 0.
    - `grep -n weekly_report_enrich config/settings.yaml` OR `grep -n entry_bias_score src/trading_crab_lib/reporting.py` shows enrichment path.
    - `grep -n tactics_signals RUNBOOK.md` matches updated documentation.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 4 — REQUIREMENTS, SUMMARY, traceability</name>
  <read_first>
    - .planning/REQUIREMENTS.md
  </read_first>
  <action>
    1. Mark **TACTICS-10** checkbox complete with one-line pointer to `tactics.py` + `tactics_signals.parquet` schema note.
    2. Update traceability table: Phase 20 — Complete (after execution).
    3. Write `.planning/phases/20-v1-2-tactics-layer/20-SUMMARY.md` on execute-phase completion (shipped vs deferred).
  </action>
  <acceptance_criteria>
    - `grep -A2 TACTICS-10 .planning/REQUIREMENTS.md` shows `[x]` or **Complete** for TACTICS-10.
  </acceptance_criteria>
</task>

</tasks>

<verification>

## Automated

- `PYTHONPATH=src python -m pytest tests/test_tactics.py -q`
- `PYTHONPATH=src python -c "from trading_crab_lib.config import load; load()"`

## Manual

- `python run_pipeline.py --steps 9` with real `data/raw/asset_prices.parquet` and cluster labels; confirm `outputs/reports/tactics_signals.parquet` has new columns.
- Regenerate weekly report (step 7) and confirm **Tactics** section when enrichment enabled.

</verification>

---

## PLANNING COMPLETE
