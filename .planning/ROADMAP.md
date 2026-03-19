## Trading-Crab Roadmap (V1)

## Phases

- [ ] **Phase 1: Data & Constraints Foundations** - Establish ETF-only, non-intraday data universe with checkpointed, causal-aware feature pipeline.
- [x] **Phase 2: Regime Clustering & Interpretation** - Derive stable, interpretable market regimes and descriptive profiles. (completed 2026-03-16)
- [x] **Phase 3: Supervised Regime & Behavior Models** - Train and evaluate models for current and forward regimes and ETF/portfolio behavior. (completed 2026-03-19)
- [x] **Phase 4: Regime-Conditional ETF & Portfolio Behavior** - Quantify ETF and portfolio performance characteristics by regime. (completed 2026-03-17)
- [x] **Phase 5: Recommendations & Machine-Readable Outputs** - Turn analysis into transparent ETF-level recommendations and structured artifacts. (completed 2026-03-17)
- [x] **Phase 6: Weekly Report Pipeline** - Provide a one-button weekly report flow with email-ready summary. (completed 2026-03-17)
- [x] **Phase 7: Portfolio & Email Integration** - Wire portfolio config and SMTP/email delivery into the weekly pipeline. (completed 2026-03-17)
- [x] **Phase 8: Data + Signals + Diagnostics** - Add extra FRED series, yield-curve spreads, ratios, and RRG diagnostics. (completed 2026-03-17)
- [x] **Phase 9: Tactics & Diagnostics Integration** - Integrate diagnostics + tactics into the core pipeline and weekly report. (completed 2026-03-17)
- [x] **Phase 10: Tactics Layer + Install & Env Automation** - Add tactics layer and one-shot installer/env health checks. (completed 2026-03-17)
- [x] **Phase 11: Core Cleanup & Env Sanity** - Normalize directory layout, date handling, and style imports. (completed 2026-03-17)

## Phase Details

### Phase 1: Data & Constraints Foundations
**Goal**: Ensure Trading-Crab operates on an ETF-only, non-intraday universe with a reproducible, checkpointed data and feature pipeline suitable for downstream regime and model work.
**Depends on**: Nothing (first phase)
**Requirements**: DATA-01, DATA-02, DATA-03, CONSTR-01, CONSTR-02
**Success Criteria** (what must be TRUE):
  1. The pipeline can ingest macro series and ETF prices for the configured ETF universe over the intended historical window without manual intervention (DATA-01).
  2. Typical runs use parquet checkpoints and can skip full re-scrapes while still producing correct downstream artifacts (DATA-02).
  3. A documented feature set (including causal variants) is computed end-to-end with no look-ahead leakage into supervised training (DATA-03).
  4. All data ingestion, features, and models operate strictly on ETFs (including bitcoin via ETF) with no single stocks or direct crypto, and no intraday or auto-trading behavior is introduced (CONSTR-01, CONSTR-02).
**Plans**: 4 plans
Plans:
- [ ] 03-supervised-regime-behavior-models-01-PLAN.md — bootstrap scaffolding (superseded by 03-04)
- [x] 03-supervised-regime-behavior-models-02-PLAN.md — regime CV + forward transition models
- [x] 03-supervised-regime-behavior-models-03-PLAN.md — behavior directional models
- [x] 03-supervised-regime-behavior-models-04-PLAN.md — leakage hardening + behavior wiring + metrics artifacts

### Phase 2: Regime Clustering & Interpretation
**Goal**: Produce a small, stable set of interpretable market regimes with reproducible profiles and names that downstream models and users can rely on.
**Depends on**: Phase 1
**Requirements**: REGIME-01, REGIME-02, REGIME-03
**Success Criteria** (what must be TRUE):
  1. Historical quarters are assigned to a manageable number of regimes (target ~4–7) via PCA + clustering, using the established feature set (REGIME-01).
  2. For each regime, reproducible code produces descriptive statistics over key macro variables and ETF returns that support human-readable descriptions (REGIME-02).
  3. A version-controlled mapping from cluster IDs to human-readable regime names exists, is applied consistently across runs, and any renames are documented (REGIME-03).
**Plans**: 3 plans
Plans:
- [ ] 02-regime-clustering-interpretation-01-PLAN.md — Harden clustering pipeline and artifacts for deterministic regime labels (REGIME-01).
- [ ] 02-regime-clustering-interpretation-02-PLAN.md — Implement regime profiling, naming, and transitions with tests (REGIME-01, REGIME-02, REGIME-03).
- [ ] 02-regime-clustering-interpretation-03-PLAN.md — Add empirical forward-window regime reach probabilities as diagnostic artifacts with tests (supports REGIME-02/REGIME-03; complements MODEL-02).

### Phase 3: Supervised Regime & Behavior Models
**Goal**: Train, validate, and report on supervised models that turn regimes into real-time and forward-looking signals for regimes and ETF/portfolio behavior.
**Depends on**: Phases 1, 2
**Requirements**: MODEL-01, MODEL-02, MODEL-03, MODEL-04
**Success Criteria** (what must be TRUE):
  1. A current-regime classifier predicts the present quarter’s regime from currently-available, causally valid features with time-series aware validation (MODEL-01).
  2. Forward-horizon models output regime transition probabilities for at least one quarter ahead (and ideally further horizons) in an interpretable format (MODEL-02).
  3. Models provide, at minimum, directional next-quarter behavior (e.g. up/flat/down) for individual ETFs and candidate portfolios (MODEL-03).
  4. Model performance is summarized with transparent, time-series aware metrics (e.g. accuracy, F1, per-class breakdowns) that can be inspected before trusting recommendations (MODEL-04).
**Plans**: TBD

### Phase 4: Regime-Conditional ETF & Portfolio Behavior
**Goal**: Quantify how ETFs and simple portfolio templates behave across regimes so users can see which assets and allocations historically do well or poorly in each environment.
**Depends on**: Phases 1, 2, 3
**Requirements**: PORT-01, PORT-02, PORT-03
**Success Criteria** (what must be TRUE):
  1. For every ETF in scope, regime-conditional return distributions (including median, quantiles, and basic risk metrics) are computed and inspectable (PORT-01).
  2. A small library of named portfolio templates (e.g. risk-on, risk-off, inflation-hedged) is defined and evaluated with regime-conditional performance statistics (PORT-02).
  3. Given a user-specified ETF portfolio, the system can report expected return and risk under the inferred current regime and likely near-term regimes (PORT-03).
**Plans**: TBD

### Phase 5: Recommendations & Machine-Readable Outputs
**Goal**: Turn regime and behavior insights into concrete, explainable ETF-level recommendations and structured outputs suitable for automation.
**Depends on**: Phases 1, 2, 3, 4
**Requirements**: UX-01, UX-02, UX-03
**Success Criteria** (what must be TRUE):
  1. For a given current ETF portfolio, the system emits per-ETF buy/hold/sell recommendations that move weights incrementally toward a regime-aware target mix without excessive turnover (UX-01).
  2. Each recommendation includes a brief, human-readable explanation grounded in regime conditions and historical ETF/portfolio behavior (UX-02).
  3. Machine-readable artifacts (e.g. CSV/JSON) are produced that capture current regime probabilities, key transition probabilities, portfolio metrics, and recommended trades/target weights (UX-03).
**Plans**: TBD

### Phase 6: Weekly Report Pipeline
**Goal**: Provide a reproducible, one-button weekly workflow that refreshes data as configured and generates an email-ready summary combining regimes, expectations, and recommendations.
**Depends on**: Phases 1, 2, 3, 4, 5
**Requirements**: REPORT-01, REPORT-02
**Success Criteria** (what must be TRUE):
  1. A CLI or small script exists that runs the weekly report pipeline end-to-end, including data refresh/reuse, regime inference, portfolio expectations, and recommendations (REPORT-01).
  2. The pipeline outputs a concise text summary suitable as the body of a weekly email, including current regime with confidence, notable transition risks, and ETF-level buy/hold/sell suggestions (REPORT-02).
**Plans**: TBD

### Phase 7: Portfolio & Email Integration
**Goal**: Make the pipeline portfolio-aware and wire email delivery so that weekly recommendations reflect a real ETF portfolio and can be sent automatically.
**Depends on**: Phases 1–6
**Requirements**: PORT-04, REPORT-03
**Success Criteria** (what must be TRUE):
  1. A portfolio config file (e.g. `config/portfolio.yaml`) defines tickers and weights and is consumed by the weekly pipeline.
  2. Machine-readable recommendation bundles include portfolio-aware deltas and summary metrics.
  3. Email configuration (`config/email.local.yaml`) can be provided and a `--send-email` flag sends the generated report to the configured recipient.
**Plans**: TBD

### Phase 8: Data + Signals + Diagnostics
**Goal**: Expand macro inputs and diagnostics so that regime decisions and tactics are grounded in richer FRED series, yield-curve spreads, ratios, and RRG-style views.
**Depends on**: Phases 1–3
**Requirements**: DATA-04, DIAG-01, DIAG-02
**Success Criteria** (what must be TRUE):
  1. Additional FRED series (e.g. VIXCLS, UNRATE, M2, yield-curve spreads) are configured and ingested when available.
  2. Yield-curve spreads and key ratios (Oil:Gold, Oil:Bonds, Bonds:Gold, Lumber:Gold proxy, etc.) are computed and surfaced as diagnostics.
  3. RRG-style diagnostics (RS-ratio, RS-momentum) are available as machine-readable artifacts for at least one benchmark (e.g. SPY).
**Plans**: TBD

### Phase 9: Tactics & Diagnostics Integration
**Goal**: Integrate diagnostics and tactics into the core pipeline and weekly report so that tactical views are first-class alongside regimes and recommendations.
**Depends on**: Phases 3, 4, 5, 8
**Requirements**: TACTICS-01, TACTICS-02
**Success Criteria** (what must be TRUE):
  1. A pipeline step computes per-asset tactics metrics and labels (buy-and-hold / swing / stand-aside) and writes a stable `tactics_signals` artifact.
  2. Weekly reports surface tactics sections that are consistent with diagnostics and recommendation artifacts.
**Plans**: TBD

### Phase 10: Tactics Layer + Install & Env Automation
**Goal**: Harden the tactics layer and make installation/environment health as close to one-command as possible.
**Depends on**: Phases 1–3, 6, 9
**Requirements**: TACTICS-03, INSTALL-10
**Success Criteria** (what must be TRUE):
  1. Tactics metrics and labels are parameterized via `config/settings.yaml` and covered by tests.
  2. One-shot install and env-check scripts exist and are documented, and they can run a small smoke suite successfully.
**Plans**: TBD

### Phase 11: Core Cleanup & Env Sanity
**Goal**: Normalize directory layout, date handling, and style imports so that the pipeline behaves predictably across machines and over time.
**Depends on**: Phases 1–3
**Requirements**: CORE-01, CORE-02
**Success Criteria** (what must be TRUE):
  1. Expected `data/` and `outputs/` subdirectories are created automatically by setup scripts or pipeline steps.
  2. `data.end_date` handling in config and ingestion is robust (null → “today”) and tested.
  3. Style imports (`from __future__ import annotations`, etc.) are consistent in key modules.
**Plans**: TBD

## Progress

| Phase | Name                                      | Plans Complete | Status       | Completed    |
|-------|-------------------------------------------|----------------|--------------|--------------|
| 1     | Data & Constraints Foundations            | 2/3            | In Progress  | -            |
| 2     | Regime Clustering & Interpretation        | 2/2            | Complete     | 2026-03-16   |
| 3     | Supervised Regime & Behavior Models       | 4/4            | Complete     | 2026-03-19   |
| 4     | Regime-Conditional ETF & Portfolio Behavior | 0/0          | Complete     | 2026-03-17   |
| 5     | Recommendations & Machine-Readable Outputs | 0/0          | Complete     | 2026-03-17   |
| 6     | Weekly Report Pipeline                    | 0/0            | Complete     | 2026-03-17   |
| 7     | Portfolio & Email Integration             | 0/0            | Complete     | 2026-03-17   |
| 8     | Data + Signals + Diagnostics              | 1/1            | Complete     | 2026-03-17   |
| 9     | Tactics & Diagnostics Integration         | 0/0            | Complete     | 2026-03-17   |
| 10    | Tactics Layer + Install & Env Automation  | 0/0            | Complete     | 2026-03-17   |
| 11    | Core Cleanup & Env Sanity                 | 0/0            | Complete     | 2026-03-17   |

