---
phase: 18-v1-2-signal-diagnostics
plan: 01
type: execute
wave: 1
depends_on:
  - 17-v1-2-expanded-macro-signals
files_modified:
  - config/settings.yaml
  - src/trading_crab_lib/diagnostics.py
  - src/trading_crab_lib/plotting.py
  - src/trading_crab_lib/reporting.py
  - pipelines/08_diagnostics.py
  - run_pipeline.py
  - notebooks/08_diagnostics.ipynb
  - tests/unit/test_diagnostics_rrg.py
  - tests/unit/test_diagnostics_ratios.py
  - tests/unit/test_weekly_report_diagnostics.py
  - RUNBOOK.md
  - .planning/REQUIREMENTS.md
  - .planning/phases/18-v1-2-signal-diagnostics/18-SUMMARY.md
autonomous: true
requirements:
  - SIGNAL-10
  - SIGNAL-11
user_setup:
  - ETF price checkpoint `data/raw/asset_prices.parquet` for local smoke (from step 6 or cached run)
must_haves:
  truths:
    - "Config-driven ratio definitions in settings.yaml produce stable parquet under outputs/reports/diagnostics/ including optional trigger columns derived from z-score/percentile rules."
    - "RRG-style RS-ratio / RS-momentum outputs remain machine-readable (rrg_current.parquet) for each configured benchmark and cover ETFs present in prices vs benchmark."
    - "When diagnostics artifacts exist and diagnostics.weekly_report_include is true, weekly_report.md includes a Diagnostics section built from those parquets (no crash if files missing)."
    - "Step 8 can save at least one plot per category (ratios + RRG) to outputs/plots/ when RunConfig.save_plots is true, matching project plotting conventions."
    - "notebooks/08_diagnostics.ipynb documents how to load diagnostics parquets and locate plot outputs."
  artifacts:
    - path: "config/settings.yaml"
      provides: "diagnostics.ratios unchanged or extended; new diagnostics.trigger_defaults and/or per-ratio overrides; diagnostics.weekly_report_include; optional diagnostics.rrg_lookback"
    - path: "src/trading_crab_lib/diagnostics.py"
      provides: "evaluate_ratio_triggers() or equivalent pure helpers for trigger labels from latest z/pct + rules"
    - path: "pipelines/08_diagnostics.py"
      provides: "writes enriched ratios_current.parquet; invokes plotting when run_cfg.generate_plots/save_plots"
    - path: "src/trading_crab_lib/reporting.py"
      provides: "write_weekly_report_md optional Diagnostics section"
    - path: "notebooks/08_diagnostics.ipynb"
      provides: "report/notebook hook for SIGNAL-11"
---

<objective>
Close **SIGNAL-10** and **SIGNAL-11** for milestone v1.2 by **hardening and productizing** the existing diagnostics step (**step 8**): add **trigger-style** ratio signals, **saved plots**, **weekly report** and **notebook** hooks, and **tests** — without changing regime clustering or supervised feature matrices unless explicitly documented as out of scope.
</objective>

**Non-goals:** New ML models (**MODEL-10**, Phase 19); tactics labels (**TACTICS-10**, Phase 20); adding diagnostics columns to **`features.parquet`** / **`clustering_features`**; exact vendor RRG replication.

<execution_context>
@.planning/phases/18-v1-2-signal-diagnostics/18-CONTEXT.md
@.planning/REQUIREMENTS.md
@.planning/ROADMAP.md
@RUNBOOK.md
@config/settings.yaml
@src/trading_crab_lib/diagnostics.py
@src/trading_crab_lib/plotting.py
@src/trading_crab_lib/reporting.py
@pipelines/08_diagnostics.py
@run_pipeline.py
</execution_context>

<context>
**Pre-flight:** Confirm `pipelines/08_diagnostics.py` and `diagnostics.*` config match the brownfield summary in **`18-CONTEXT.md`**.

**Checkpoint contract:** Step 8 only **reads** `asset_prices.parquet` (and config). It must not require network or alter steps 1–7 checkpoints.

**Trigger semantics:** Implement **clear, documented** rules (e.g. `|z| >= z_extreme` → `"stretched"`, percentile above/below configurable bands). Avoid magic numbers in Python — **YAML-first**.
</context>

<tasks>

<task type="auto" tdd="false">
  <name>Task 1 — Audit + config schema</name>
  <read_first>
    - .planning/phases/18-v1-2-signal-diagnostics/18-CONTEXT.md
    - config/settings.yaml (diagnostics section)
  </read_first>
  <action>
    1. Finalize YAML shape for **trigger defaults** (e.g. `diagnostics.trigger_defaults: { z_abs_min: null, percentile_high: 0.9, ... }`) and optional **per-ratio overrides** under each ratio entry or a parallel map — pick one approach and document in `18-CONTEXT.md` §Locked decisions if adjusted.
    2. Add `diagnostics.weekly_report_include: true` and optional `diagnostics.rrg_lookback` (defaulting to current behavior in code if omitted).
  </action>
  <acceptance_criteria>
    - `python -c "from trading_crab_lib.config import load; load()"` succeeds after YAML edit.
  </acceptance_criteria>
</task>

<task type="auto" tdd="true">
  <name>Task 2 — Triggers + enriched ratio parquet</name>
  <read_first>
    - src/trading_crab_lib/diagnostics.py
    - pipelines/08_diagnostics.py
  </read_first>
  <action>
    1. Implement pure helper(s) to classify each ratio row given `latest_zscore`, `percentile`, and trigger config (return string columns e.g. `trigger`, `trigger_detail`).
    2. Extend `_compute_ratios` (or equivalent) to attach these columns before writing **`ratios_current.parquet`**.
    3. Keep backward compatibility: if trigger config absent, omit new columns or set `"neutral"` — document choice in module docstring.
  </action>
  <acceptance_criteria>
    - New unit tests in `tests/unit/test_diagnostics_ratios.py` (or extended `test_diagnostics_rrg.py`) using synthetic price DataFrame covering at least one fired trigger and one neutral case.
  </acceptance_criteria>
</task>

<task type="auto" tdd="true">
  <name>Task 3 — Plots (SIGNAL-10 / roadmap)</name>
  <read_first>
    - src/trading_crab_lib/plotting.py (existing RunConfig / save_plots patterns)
  </read_first>
  <action>
    1. Add plotting helpers that accept `run_cfg: RunConfig` and save under `outputs/plots/` with **`08_` prefix** (e.g. ratio bar or table heatmap; RRG scatter of rs_ratio vs rs_momentum for one benchmark).
    2. Wire **`pipelines/08_diagnostics.py`** `main()` (or shared runner invoked by `run_pipeline` step 8) to call these when `run_cfg.generate_plots` / `save_plots` align with other pipeline steps.
  </action>
  <acceptance_criteria>
    - With synthetic data in tests, call plotting functions with `RunConfig(save_plots=False)` to avoid filesystem when appropriate, **or** use `tmp_path` for output assertions.
  </acceptance_criteria>
</task>

<task type="auto" tdd="true">
  <name>Task 4 — Weekly report hook</name>
  <read_first>
    - src/trading_crab_lib/reporting.py (`write_weekly_report_md`)
  </read_first>
  <action>
    1. After the optional Tactics block (or before Risk), add **## Diagnostics** when `diagnostics.weekly_report_include` is true and at least one of `outputs/reports/diagnostics/ratios_current.parquet` / `rrg_current.parquet` exists.
    2. Keep output concise: top ratios by `|latest_zscore|` or trigger status + one-line RRG quadrant counts per benchmark; **never** fail report generation if parquet is malformed — catch and skip section.
    3. Extend or add tests (e.g. `tests/unit/test_weekly_report_diagnostics.py`) with temporary dirs / monkeypatched `OUTPUT_DIR` if needed.
  </action>
  <acceptance_criteria>
    - `pytest` for the new/extended weekly report test passes.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 5 — Notebook hook (SIGNAL-11)</name>
  <read_first>
    - notebooks/ (existing notebook style)
  </read_first>
  <action>
    1. Add **`notebooks/08_diagnostics.ipynb`** with cells: load config, load `ratios_current.parquet` / `rrg_current.parquet` from `OUTPUT_DIR`, display preview, list expected plot filenames under `outputs/plots/`.
  </action>
  <acceptance_criteria>
    - Notebook valid JSON; no hardcoded API keys.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 6 — RUNBOOK + REQUIREMENTS + summary</name>
  <read_first>
    - RUNBOOK.md (Extended pipeline: steps 8 and 9)
    - .planning/REQUIREMENTS.md
  </read_first>
  <action>
    1. Update **RUNBOOK.md** to mention diagnostics **plots**, **weekly report** section, and prerequisite **step 6** for prices before step 8.
    2. Set **SIGNAL-10** and **SIGNAL-11** to **Complete** in **REQUIREMENTS.md** (checkbox + traceability table) when execution is done; create **`18-SUMMARY.md`** during `$gsd:execute-phase 18`.
  </action>
  <acceptance_criteria>
    - `grep -n "diagnostics\\|step 8\\|SIGNAL" RUNBOOK.md` shows updated guidance.
  </acceptance_criteria>
</task>

</tasks>

<verification>

## Automated

- `pytest tests/unit/test_diagnostics_rrg.py tests/unit/test_diagnostics_ratios.py tests/unit/test_weekly_report_diagnostics.py -q` (adjust filenames if consolidated)
- `python -c "from trading_crab_lib.config import load; load()"`

## Manual

- `python run_pipeline.py --steps 6,8 --plots` (requires cached or fresh `asset_prices.parquet`) and confirm `outputs/reports/diagnostics/*.parquet` and `outputs/plots/08_*.png`.
- Generate weekly report path that includes diagnostics (e.g. run step 7 or `write_weekly_report_md` integration path) and eyeball `outputs/reports/weekly_report.md`.

## Goal-backward (verify-phase)

- Map each **ROADMAP** Phase 18 success criterion to an artifact or test before marking phase complete.

</verification>
