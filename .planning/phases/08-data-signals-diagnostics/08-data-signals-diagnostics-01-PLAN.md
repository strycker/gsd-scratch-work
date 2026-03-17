---
phase: 08-data-signals-diagnostics
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - config/settings.yaml
  - src/market_regime/transforms.py
  - src/market_regime/plotting.py
  - pipelines/08_diagnostics.py (new)
  - run_pipeline.py (wire step 8; optional)
  - tests/unit/test_fred_series_config.py (new)
  - tests/unit/test_yield_curve_features.py (new)
  - tests/unit/test_diagnostics_rrg.py (new)
autonomous: true
requirements:
  - DATA-10
  - SIGNAL-10
  - SIGNAL-11
user_setup: []
must_haves:
  truths:
    - "The pipeline can ingest the additional macro series (VIX, UNRATE, M2, yield-curve spreads) from FRED via config alone."
    - "Yield-curve spread features are explicitly computed and available for downstream transforms (log, derivatives) without look-ahead."
    - "Diagnostics (ratios/triggers + RRG) are produced as artifacts (tables + plots) and do not silently change clustering without an explicit config change."
  artifacts:
    - path: "data/raw/fred_macro.parquet"
      provides: "Raw quarterly macro table including new FRED columns (after step 01)."
    - path: "data/processed/features.parquet"
      provides: "Feature table including yield-curve spread columns (after step 02)."
    - path: "outputs/reports/diagnostics/ratios_current.parquet"
      provides: "Current ratio/trigger readings with z-scores/percentiles for configured ratios."
    - path: "outputs/reports/diagnostics/rrg_current.parquet"
      provides: "Current RRG coordinates (RS-Ratio, RS-Momentum, quadrant) per asset and benchmark."
    - path: "outputs/plots/08_diagnostics_ratios.png"
      provides: "Ratio/trigger diagnostic chart(s) with regime overlays."
    - path: "outputs/plots/08_diagnostics_rrg.png"
      provides: "RRG chart(s) for selected assets vs benchmark(s)."
  key_links:
    - from: "config/settings.yaml"
      to: "src/market_regime/ingestion/fred.py"
      via: "cfg['fred']['series'] entries auto-fetched by fetch_all()"
      pattern: "cfg['fred']['series']"
    - from: "src/market_regime/transforms.py"
      to: "pipelines/02_features.py"
      via: "engineer_all() feature pipeline order"
      pattern: "from market_regime.features.transforms import"
    - from: "pipelines/08_diagnostics.py"
      to: "src/market_regime/plotting.py"
      via: "plot helpers for ratios and RRG"
      pattern: "from market_regime import plotting"
---

<objective>
Add the v1.2 Phase 8 data expansions (FRED series + yield curve spreads) and first-pass diagnostic outputs (ratios/triggers + RRG) as reproducible artifacts.
</objective>

<execution_context>
@.planning/PROJECT.md
@.planning/phases/08-data-signals-diagnostics/08-RESEARCH.md
@config/settings.yaml
@src/market_regime/ingestion/fred.py
@src/market_regime/transforms.py
@src/market_regime/plotting.py
@run_pipeline.py
</execution_context>

<context>
- FRED ingestion already supports arbitrary series IDs from `config/settings.yaml` and resamples to quarter-end.
- Feature engineering pipeline order must not change (cross ratios → log → select → gap-fill → derivatives → select).
- Diagnostics should be additive and inspectable; no allocation rules hardwired here.
</context>

<tasks>

<task type="auto">
  <name>Task 1: Expand FRED series configuration (DATA-10)</name>
  <files>config/settings.yaml</files>
  <action>
    - Add requested FRED IDs to `fred.series`:
      - VIXCLS → fred_vix
      - UNRATE → fred_unrate
      - M2SL   → fred_m2sl
      - M2NS   → fred_m2ns
      - GS2    → fred_gs2
      - T10Y2Y → fred_t10y2y
      - T10Y3M → fred_t10y3m
    - Keep shift=false for all of the above (GDP/GNP remain shift=true).
    - Ensure naming is consistent with existing `fred_*` columns.
  </action>
  <verify>
    - Unit test asserts the new keys exist and map to the expected friendly names.
    - Step 01 ingest completes and the resulting macro parquet includes the new columns (when API access is available).
  </verify>
</task>

<task type="auto">
  <name>Task 2: Add yield curve spread features in transforms (DATA-10)</name>
  <files>src/market_regime/transforms.py</files>
  <action>
    - Add a small helper (e.g. add_yield_curve_features) that computes:
      - yc_10y_2y = fred_gs10 - fred_gs2
      - yc_10y_3m = fred_gs10 - fred_tb3ms
      - yc_2y_3m  = fred_gs2  - fred_tb3ms
    - Call it in engineer_all() in Step 1 section (cross-asset ratios) so the spreads exist prior to log transforms/derivatives.
    - Do not modify the ordering of the six pipeline stages.
  </action>
  <verify>
    - Unit test builds a tiny synthetic df with gs10/gs2/tb3ms columns and asserts spreads are computed correctly.
    - Unit test ensures the feature columns are preserved through select steps when present in config feature lists.
  </verify>
</task>

<task type="auto">
  <name>Task 3: Ratio/trigger diagnostics (SIGNAL-10)</name>
  <files>
    - pipelines/08_diagnostics.py (new)
    - src/market_regime/plotting.py
    - config/settings.yaml
  </files>
  <action>
    - Add config-driven ratio definitions (numerator/denominator tickers + label) under a new `diagnostics.ratios` section.
      - Include at least: Oil:Gold, Oil:Bonds, Bonds:Gold, Lumber:Gold, plus a generic “custom ratio” slot.
    - Implement a diagnostics pipeline step that:
      - Loads latest ETF price history (existing checkpoints) and current regime labels/probabilities if available.
      - Computes ratio time series, plus a standardized “current reading” table:
        - latest_value, zscore_vs_history, percentile_vs_history (rolling window optional)
      - Writes `outputs/reports/diagnostics/ratios_current.parquet` and optionally a full history parquet.
    - Add plotting helpers for a compact ratio dashboard with regime overlay shading.
  </action>
  <verify>
    - Unit test computes a simple ratio from synthetic price series and validates z-score/percentile outputs.
    - Running the diagnostics step produces the parquet artifact even when some ratios have missing data (graceful skip).
  </verify>
</task>

<task type="auto">
  <name>Task 4: RRG diagnostics (SIGNAL-11)</name>
  <files>
    - pipelines/08_diagnostics.py (new)
    - src/market_regime/plotting.py
    - config/settings.yaml
  </files>
  <action>
    - Implement RS (asset/benchmark) and a first-pass RS-Ratio / RS-Momentum:
      - Smooth RS with a rolling mean (configurable window)
      - Normalize to 100-centered z-scores (mean/std over lookback window)
      - Define RS-Momentum as ROC (or first difference) of RS-Ratio, normalized similarly
    - Support benchmarks: SPY (default), VT, and 60/40 template (from templates).
    - Produce `outputs/reports/diagnostics/rrg_current.parquet` with:
      - as_of_date, asset, benchmark, rs_ratio, rs_momentum, quadrant, and optionally trailing path points.
    - Add plotting helper to generate a readable RRG chart per benchmark.
  </action>
  <verify>
    - Unit test validates quadrant classification and 100-centering on a small synthetic dataset.
    - Diagnostics step runs without requiring new external providers (uses existing ETF price checkpoints).
  </verify>
</task>

<task type="auto">
  <name>Task 5 (optional): Wire diagnostics into run_pipeline (step 8)</name>
  <files>run_pipeline.py</files>
  <action>
    - Add a new step number "8" that runs pipelines/08_diagnostics.py.
    - Ensure `scripts/run_weekly_report.py` can include step 8 later (optional; not required in this plan).
  </action>
  <verify>
    - `python run_pipeline.py --steps 8` executes the diagnostics step and writes the artifacts.
  </verify>
</task>

</tasks>

<out_of_scope>
- No new ML models (XGBoost/LightGBM) in Phase 8 (those are v1.2 MODEL phases).
- No tactics layer (buy/hold/swing) in Phase 8.
- No changes to clustering feature lists without an explicit, deliberate decision.
</out_of_scope>
