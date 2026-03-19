## Trading-Crab — V1 Requirements

### Overview

This document captures the v1 functional and non-functional requirements for Trading-Crab, a market-regime analysis and ETF portfolio guidance system.

- Scope: ETF-only portfolios (broad indices, sectors, bonds, precious metals, bitcoin ETF).
- Cadence: Weekly / quarterly, not intraday.
- Outputs: Research views + concrete buy/hold/sell recommendations and a weekly report.

Each requirement has a stable ID for traceability from roadmap → plans → tests.

---

## v1 Requirements

### 1. Data Ingestion & Feature Engineering

- **DATA-01 — Macro & ETF ingestion**
  - **Description**: Ingest macroeconomic time series (multpl + FRED) and ETF prices for the chosen ETF universe.
  - **Details**:
    - Macro data: quarterly resolution, ~1950–present where available.
    - ETFs: as far back as each ETF’s history allows.
  - **Rationale**: Regime discovery and ETF behavior analysis require long history.

- **DATA-02 — Checkpointed pipeline**
  - **Description**: Maintain a checkpointed data pipeline so full re-scrapes are optional.
  - **Details**:
    - Use parquet checkpoints + manifest to avoid re-scraping on every run.
    - Typical workflows should re-use cached data/checkpoints.
  - **Rationale**: Scraping is slow; iteration must be fast.

- **DATA-03 — Feature set & causal variants**
  - **Description**: Compute a stable, documented feature set with both non-causal and causal variants.
  - **Details**:
    - Include cross-asset ratios, log transforms, Bernstein gap fill, smoothed derivatives, and any additional yield-curve/feature work defined in `settings.yaml`.
    - Ensure any supervised training that mimics “what was knowable then” uses causal features with no look-ahead bias.
  - **Rationale**: Prevent leakage while preserving analytical richness.

### 2. Regime Clustering & Interpretation

- **REGIME-01 — Regime clustering**
  - **Description**: Cluster quarters into a small, interpretable set of regimes.
  - **Details**:
    - Use PCA + KMeans (and related tools already in the codebase).
    - Target ~4–7 regimes with clear differences in macro conditions and asset returns.
  - **Rationale**: Regimes are the core abstraction for all downstream logic.

- **REGIME-02 — Regime profiling**
  - **Description**: For each regime, compute descriptive statistics over key macro features and ETF returns.
  - **Details**:
    - Macro profiles are produced via `regime.build_profiles()` and saved to `data/regimes/profiles.parquet`.
    - ETF return behavior by regime is captured in `data/regimes/asset_return_profile.parquet` (written by step 6 `06_asset_returns.py` via `returns_by_regime()`).
    - Summaries should enable human-readable descriptions (e.g. “high inflation, low growth, tight credit”) and be reproducible from code (not manual notebooks only).
  - **Rationale**: Users need to understand what each regime actually means, both in macro terms and in terms of ETF performance.

- **REGIME-03 — Stable regime naming**
  - **Description**: Provide a stable mapping from cluster IDs to human-readable regime names.
  - **Details**:
    - Keep the mapping in version-controlled config (e.g. `regime_labels.yaml`).
    - Document any renames / re-labeling decisions.
  - **Rationale**: Names should not silently shift across runs; critical for longitudinal analysis.

### 3. Supervised Models (Current & Forward)

- **MODEL-01 — Current-regime classifier**
  - **Description**: Train models that predict the current quarter’s regime from currently-available features.
  - **Details**:
    - No forward-looking features; respect publication lags and causal variants.
    - Use time-series appropriate validation (e.g. `TimeSeriesSplit` walk-forward).
  - **Rationale**: Needed to turn unsupervised regimes into a real-time signal.

- **MODEL-02 — Forward regime transitions**
  - **Description**: Train forward-horizon models that estimate regime transition probabilities.
  - **Details**:
    - At minimum, support 1-quarter-ahead transitions; ideally extend to 2–8 quarters.
    - Outputs should be interpretable probabilities per future regime (given current regime and features).
  - **Rationale**: Portfolio guidance should account for likely near-term regime shifts.

- **MODEL-03 — Forward ETF/portfolio behavior**
  - **Description**: Provide simple forward-looking behavior estimates for individual ETFs and candidate portfolios.
  - **Details**:
    - At minimum, a directional view (up/flat/down or similar) for the next quarter.
    - Prefer models that can be summarized in a small set of metrics (probability of “good” vs “bad” outcome).
  - **Rationale**: Helps connect regime predictions to asset-level expectations.

- **MODEL-04 — Evaluation & reporting**
  - **Description**: Evaluate supervised models with transparent metrics and confusion-style summaries.
  - **Details**:
    - Track performance across train/test splits with time-series aware CV.
    - Produce human-inspectable metrics (accuracy, F1, etc.) and per-class breakdowns where meaningful.
  - **Rationale**: User needs to see whether models are actually working before trusting recommendations.

### 4. ETF & Portfolio Behavior by Regime

- **PORT-01 — Regime-conditional ETF returns**
  - **Description**: For each regime, compute historical return distributions for every ETF in scope.
  - **Details**:
    - Include median, quantiles, and basic risk metrics (e.g. drawdowns) per regime.
    - Surface which ETFs are generally “green” or “red” in each environment.
  - **Rationale**: Forms the empirical basis for regime-aware allocations.

- **PORT-02 — Portfolio templates**
  - **Description**: Define and evaluate a small library of simple portfolio templates.
  - **Details**:
    - Example templates: 60/40, risk-off, risk-on, barbell, inflation-hedged.
    - Compute regime-conditional performance for each template.
  - **Rationale**: Provides understandable building blocks for recommendations.

- **PORT-03 — Current-portfolio expectation**
  - **Description**: Given a specific ETF portfolio (weights), estimate expected return and risk under:
    - The inferred current regime.
    - The most likely near-term regimes (from transition models).
  - **Rationale**: Bridges the gap between high-level regimes and the user’s actual holdings.

### 5. Recommendations & UX

- **UX-01 — Incremental ETF recommendations**
  - **Description**: Generate concrete per-ETF buy/hold/sell recommendations for a given current portfolio.
  - **Details**:
    - Recommendations should move weights incrementally toward a regime-aware target mix.
    - Respect ETF-only constraints (no single stocks, no direct crypto).
    - Avoid hyperactive turnover; changes should be plausible to implement weekly.
  - **Rationale**: Turn analysis into actionable guidance without over-trading.

- **UX-02 — Explanation & transparency**
  - **Description**: For each recommendation, provide a brief explanation grounded in regime and ETF behavior.
  - **Details**:
    - E.g. “Reduce `TLT` because current regime and likely transitions historically penalize long-duration bonds.”
  - **Rationale**: User must understand the “why” behind suggestions to trust them.

- **UX-03 — Machine-readable outputs**
  - **Description**: Emit machine-readable artifacts (CSV/JSON) capturing:
    - Current regime and probabilities.
    - Key transition probabilities.
    - Current portfolio metrics.
    - Recommended trades / target weights.
  - **Rationale**: Enables downstream automation and experimentation (dashboards, emails, scripts).

### 6. Weekly Report / Automation

- **REPORT-01 — Weekly report pipeline**
  - **Description**: Provide a reproducible way (CLI or small script) to generate a full weekly report.
  - **Details**:
    - Refresh or reuse data as configured.
    - Infer current regime and key transitions.
    - Compute current-portfolio expectations.
    - Generate recommendations and a human-readable summary.
  - **Rationale**: Encodes the “one-button” workflow for ongoing use.

- **REPORT-02 — Email-ready summary**
  - **Description**: Produce a compact text summary suitable to send as a weekly email.
  - **Details**:
    - Include: current regime (with confidence), notable transition risks, and ETF-level buy/hold/sell suggestions.
    - Actual email sending can remain out-of-scope; focus on the content.
  - **Rationale**: Aligns with the end vision of an automated weekly advisory email.

### 7. Constraints & Non-Goals

- **CONSTR-01 — ETF-only universe**
  - **Description**: The system must operate on ETFs only for v1.
  - **Details**:
    - Broad indices, sectors, bonds, precious metals, and a bitcoin ETF are in scope.
    - No individual stocks or direct cryptocurrency holdings.
  - **Rationale**: Keeps the problem tractable and aligned with current data/architecture.

- **CONSTR-02 — No intraday / auto-trading**
  - **Description**: The system must not attempt intraday or fully automated trade execution.
  - **Details**:
    - Cadence: weekly/quarterly; no reliance on sub-daily data.
    - Outputs are recommendations and reports, not broker orders.
  - **Rationale**: Focus v1 on robust research and guidance, not execution infrastructure.

### 8. Portfolio, email, expanded macro & ops (Phases 7–11 — audit IDs)

These IDs tie **ROADMAP** Phases 7–11 to the same requirement vocabulary used in milestone audits. They complement (and do not replace) the v1.2 aspirational backlog later in this file.

- **PORT-04 — User portfolio in config**
  - **Description**: A YAML portfolio file supplies ETF weights for the weekly / dashboard path.
  - **Details**: Consumed via `trading_crab_lib.config.load_portfolio`; outputs include portfolio-aware recommendation bundles.

- **REPORT-03 — SMTP delivery path**
  - **Description**: Optional sending of the weekly report using a local, untracked email config.
  - **Details**: `trading_crab_lib.email` + `--send-email` on `run_pipeline.py` / `scripts/run_weekly_report.py`.

- **DATA-04 — Expanded FRED macro series**
  - **Description**: Additional FRED series in `config/settings.yaml` are fetched when step 1 runs with API access.
  - **Details**: e.g. VIX, unemployment, M2, yield-curve spreads — see `fred.series` for authoritative list.

- **DIAG-01 — Diagnostic ratio artifacts**
  - **Description**: Config-driven ETF ratios (Oil:Gold, Oil:Bonds, etc.) written as parquet diagnostics.
  - **Details**: `diagnostics.ratios` in `settings.yaml`; step 8 / `pipelines/08_diagnostics.py`.

- **DIAG-02 — RRG-style diagnostics**
  - **Description**: RS-ratio / RS-momentum style table vs configured benchmark(s).
  - **Details**: `diagnostics.rrg_benchmarks`; `outputs/reports/diagnostics/rrg_current.parquet`.

- **TACTICS-01 — Tactics artifact**
  - **Description**: Step 9 writes per-ETF tactics labels to a stable parquet file.
  - **Details**: `outputs/reports/tactics_signals.parquet`.

- **TACTICS-02 — Weekly report tactics section**
  - **Description**: Weekly markdown may include a tactics section when the artifact exists.
  - **Details**: `trading_crab_lib.reporting.write_weekly_report_md` optional block.

- **TACTICS-03 — Config + tests for tactics**
  - **Description**: Tactics parameters live in `settings.yaml` and are covered by unit tests.
  - **Details**: `tests/test_tactics.py`.

- **INSTALL-10 — Setup / env automation**
  - **Description**: Scripts and docs seed `.env` / email templates, scaffold dirs, and run smoke checks without committing secrets.
  - **Details**: `scripts/setup.sh`, `install_trading_crab.sh`, `check_env.sh`, `run_tests.sh`, `scripts/README.md`.

- **CORE-01 — Runtime directory layout**
  - **Description**: Expected `data/` and `outputs/` subtrees exist after setup or pipeline runs.
  - **Details**: `setup.sh` + `mkdir` calls in pipeline steps.

- **CORE-02 — Null end_date handling**
  - **Description**: `data.end_date: null` in YAML resolves to “today” for ingestion windows.
  - **Details**: `trading_crab_lib.ingestion.fred` and `ingestion.assets`; **unit test coverage still pending** (see Phase 11 verification).

---

## Traceability Notes

- `PROJECT.md` defines the vision, scope boundaries, and high-level outcomes.
- This file (`REQUIREMENTS.md`) refines that vision into concrete, testable v1 requirements.
- `ROADMAP.md` will map these requirements to phases; each phase will reference specific IDs (e.g. DATA-01, REGIME-01).
- Phase plans and tests should always reference requirement IDs to keep alignment explicit.

## Traceability

> **Gap closure (v1.0 audit):** `$gsd-plan-milestone-gaps` added **Phases 12–14** (see `.planning/ROADMAP.md`). **Phase 12** closed PORT/UX/REPORT (`04`–`06` verification). **Phase 13** (2026-03-19) added §8 narrative + traceability for Phase 7–11 IDs; **CORE-02** stays **Pending** until a unit test covers `end_date: null` → today (see `11-core-cleanup-VERIFICATION.md`).

| Requirement | Phase  | Status  |
|------------|--------|---------|
| DATA-01    | Phase 1 | Complete |
| DATA-02    | Phase 1 | Complete |
| DATA-03    | Phase 1 | Complete |
| REGIME-01  | Phase 2 | Complete |
| REGIME-02  | Phase 2 | Complete |
| REGIME-03  | Phase 2 | Complete |
| MODEL-01   | Phase 3 | Complete |
| MODEL-02   | Phase 3 | Complete |
| MODEL-03   | Phase 3 | Complete |
| MODEL-04   | Phase 3 | Complete |
| PORT-01    | Phase 12 | Complete |
| PORT-02    | Phase 12 | Complete |
| PORT-03    | Phase 12 | Complete |
| UX-01      | Phase 12 | Complete |
| UX-02      | Phase 12 | Complete |
| UX-03      | Phase 12 | Complete |
| REPORT-01  | Phase 12 | Complete |
| REPORT-02  | Phase 12 | Complete |
| CONSTR-01  | Phase 1 | Complete |
| CONSTR-02  | Phase 1 | Complete |
| PORT-04    | Phase 13 | Complete |
| REPORT-03  | Phase 13 | Complete |
| DATA-04    | Phase 13 | Complete |
| DIAG-01    | Phase 13 | Complete |
| DIAG-02    | Phase 13 | Complete |
| TACTICS-01 | Phase 13 | Complete |
| TACTICS-02 | Phase 13 | Complete |
| TACTICS-03 | Phase 13 | Complete |
| INSTALL-10 | Phase 13 | Complete |
| CORE-01    | Phase 13 | Complete |
| CORE-02    | Phase 13 | Pending |

---

## v1.2 — Planned Requirements (high-level, to be refined)

These capture the intent for the v1.2 milestone (Tactics, Triggers & Expanded Signals). They are **not yet mapped to phases** and will be refined into full REQ-IDs + traceability when we create the v1.2 roadmap.

### 1. Data & APIs (v1.2-DATA)

- **DATA-10 — Additional FRED series & spreads**
  - VIX (VIXCLS), unemployment (UNRATE), money supply (M2 series), and yield-curve proxies/spreads (e.g. 10Y–2Y, 10Y–3M).
  - Derived yield-curve spread features added in `transforms.py`, keeping causal vs non-causal variants consistent with existing design.
- **DATA-11 — Expanded price data sources**
  - Build on the existing stooq fallback and evaluate additional APIs the user may have (e.g. finviz Elite, and optionally others like polygon/Massive, FMP, Finnhub, Alpha Vantage) in a **configurable** way.
  - Preserve the current ingestion contract (checkpoint locations, ETF lists) and keep any new provider optional / guarded by config.

### 2. Signals, Ratios, and Diagnostics (v1.2-SIGNAL)

- **SIGNAL-10 — Ratio and trigger diagnostics**
  - Implement diagnostic ratios/triggers such as Lumber:Gold, Saylor↔Schiff-style signals, Oil:Gold, Oil:Bonds, Bonds:Gold, and related cross-asset ratios, with regime overlays.
  - Surface these first as **plots/tables and report excerpts**, not as hardwired allocation rules.
- **SIGNAL-11 — Relative Rotation Graphs (RRG)**
  - Add RS-ratio / RS-momentum style views (e.g. vs a benchmark like SPY or a core portfolio) to show leaders/laggards per regime.
  - Expose them via notebooks and/or saved plots, and consider later promotion into feature engineering for models.

### 3. Models (v1.2-MODEL)

- **MODEL-10 — Additional classifiers**
  - Introduce XGBoost and/or LightGBM (or similar gradient-boosting models) alongside the current RF/DT stack, for:
    - Current regime prediction.
    - Forward regime/behavior/return predictions.
  - Keep the same causal-feature discipline and TimeSeriesSplit-style validation.
- **MODEL-11 — Human-readable trees for interpretation**
  - For every RF / boosted model, also fit a simple `DecisionTreeClassifier` on the top-ranked RF (or boosted) features.
  - Visualize this tree (e.g. as text/plot) so a human can inspect decision boundaries, spot noisy or implicitly forward-looking features, and derive candidate new features.

### 4. Tactics & Volatility (v1.2-TACTICS)

- **TACTICS-10 — Strategy vs tactics classification**
  - Add a layer that classifies each asset (and/or template) into:
    - Buy-and-hold suitable.
    - Swing-trade candidate.
    - Stand-aside / wait (too noisy or unclear).
  - Use volatility at different time scales, trend slope, and correlations to inform this, with soft constraints:
    - Weekly **entries** preferred; **exits** can happen any day after close (no intraday day-trading).
    - Emphasis on finding weekly setups where a reasonable stop-loss (e.g. anchored VWAP) can be placed and trailed.

### 5. Email Delivery (v1.2-EMAIL)

- **EMAIL-10 — SMTP-based weekly report sending**
  - Add a small, optional email-sending helper/module that:
    - Reads SMTP host/port, username, and app password (e.g. Gmail) plus recipient address from a local, untracked config.
    - Sends `outputs/reports/weekly_report.md` (or a plain-text/HTML body derived from it) to the configured address.
  - Keep this **opt-in** and avoid committing any secrets; provide a template config and instructions instead.

### 6. Install & Secrets Setup (v1.2-INSTALL)

- **INSTALL-10 — Guided local setup for secrets**
  - Provide a small installation/setup helper (script or command) that:
    - Prompts for and writes `.env` (e.g. `FRED_API_KEY`) without committing secrets.
    - Prompts for and writes `config/email.local.yaml` (or similar secret configs) based on example templates.
    - Leaves `.env` and `email.local.yaml` gitignored and clearly documented.
  - Intended as a final v1.2 phase (E), once EMAIL-10 and other secret-dependent features exist.

