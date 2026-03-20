## Project: Trading-Crab — Market Regime Analysis & ETF Portfolio Guidance

### What This Is

Trading-Crab is a Python-based research and execution environment for understanding macro-driven market regimes and turning that understanding into ETF-level portfolio decisions. It is the living, code-centered expression of the ideas captured in `CLAUDE.md`, using GSD-style planning (`.planning/`) to keep architecture, requirements, and implementation in sync.

The project is intentionally opinionated about data sources, modeling choices, and UX so that the owner can iterate quickly with AI assistance while still preserving reproducibility and auditability.

### Purpose

Trading-Crab is a research and decision-support system that analyzes macroeconomic time series and ETF performance to:

- Classify historical and current quarters into market regimes (e.g. stagflation, growth boom).
- Understand how broad asset-class and sector ETFs behave in each regime.
- Predict the current quarter’s regime and expected portfolio return.
- Provide forward-looking guidance and weekly buy/hold/sell recommendations for a real ETF portfolio.

This repository is also a scratch/workbench for experimenting with Claude Code–assisted development; Trading-Crab is the primary, production-quality project inside it.

### Core Value

The core value of Trading-Crab is **transparent, regime-aware ETF guidance**: instead of opaque black-box signals, it provides a traceable pipeline from raw macro data → engineered features → regimes → diagnostics → portfolio recommendations and tactics. The goal is to help a single, quantitatively minded investor make fewer, better decisions with clear context, not to maximize automation or complexity for its own sake.

### Target Users

- A single primary user (the repository owner) acting as:
  - Quantitatively minded investor.
  - Developer comfortable running Python pipelines and notebooks.

The system may later be exposed to additional users (e.g. via a dashboard), but v1 is optimized for solo use.

### V1 Outcome (Definition of Success)

For v1, success means:

1. **Historical & current regime analysis**
   - The system can ingest ~1950–present macroeconomic data at quarterly resolution.
   - It can cluster quarters into a manageable number of interpretable regimes and label them with human-readable names.
   - It can analyze past and current financial quarters to characterize “what kind of environment we’re in” (growth, inflation, stress, etc.).

2. **Regime-aware ETF performance understanding**
   - For each regime, the system can report which ETFs and simple portfolios historically performed well/poorly.
   - It can rank ETFs and a small set of portfolio templates by regime-conditional returns and risk characteristics.

3. **Unsupervised + supervised learning pipeline**
   - Unsupervised models (e.g. PCA + clustering) establish regime labels without look-ahead bias.
   - Supervised models can:
     - Predict the current quarter’s regime from currently-available features.
     - Estimate expected returns for the current ETF portfolio under the inferred current regime.

4. **Forward-looking asset and portfolio predictions**
   - Models can estimate, for at least the next quarter:
     - Likely regime transitions (transition probabilities from current regime to others).
     - Directional behavior (and ideally rough distribution) of key ETFs and candidate portfolios.

5. **Actionable portfolio recommendations**
   - Given the current ETF portfolio and the current/forecast regimes, the system can:
     - Propose incremental buy/sell/hold changes that move the portfolio toward an “ideal” regime-aware target mix.
     - Explain recommendations at the ETF/asset-class level (not black-box).

6. **Weekly email/report**
   - Once per week, the system can generate a concise report that includes:
     - The inferred current regime (with confidence).
     - Notable regime-transition risks for the next few quarters.
     - A simple, actionable buy/hold/sell summary for the current ETF portfolio.
   - The report should be suitable for sending as an email (text first; future automation is a stretch goal).

If all of the above are working end-to-end on real data with reasonable performance and tests, v1 is considered successful.

### In-Scope Assets (V1)

**V1 restricts itself strictly to ETF-level exposure**:

- Broad equity indices (e.g. S&P 500 via `SPY` or similar).
- Sector and style ETFs (e.g. tech vs consumer discretionary).
- Precious metals and related miners (e.g. `IAU`, `SLV`, `GDX`).
- Bonds and duration exposure (e.g. `TLT`, other Treasury or aggregate bond ETFs).
- A **bitcoin ETF** for crypto exposure (spot or futures-based), treated like any other ETF.

All models, dashboards, and recommendations should treat these as the core investable universe for v1.

### Explicitly Out of Scope (V1)

The following are **deliberately excluded** from v1:

- Individual stocks (single-name equity selection).
- Direct cryptocurrency holdings (e.g. on-chain BTC/ETH); only ETF wrappers are allowed.
- Options, futures beyond what’s embedded in ETFs, leverage, and short-selling strategies.
- Intraday or high-frequency trading; the cadence is weekly / quarterly, not minute-by-minute.
- Fully automated trade execution; v1 focuses on recommendations, not placing trades.
- Complex portfolio optimization beyond simple/robust weighting schemes (full-blown mean-variance with tight constraints can wait).

These may appear in later milestones but should not sneak into the v1 design or requirements.

### Requirements (Initial Hypotheses)

These are **hypotheses** to be validated as the pipeline solidifies. They will be refined and assigned REQ-IDs in `REQUIREMENTS.md`.

#### Validated

- The existing `legacy/` implementation and `src/market_regime/` package already:
  - Ingest key macro series (multpl + FRED) and ETF prices.
  - Engineer features via log transforms, Bernstein gap filling, and smoothed derivatives.
  - Perform PCA + clustering and regime profiling.
  - Train supervised classifiers and compute regime-conditional ETF returns.

These constitute the **baseline capabilities** that v1 will refine and productize.

#### Active (to validate in v1.2+)

- [ ] Deeper tactics classification, richer cross-asset signals, and optional first-class email automation (see **v1.2** milestone).

#### Validated (shipped — v1.0)

- ✓ End-to-end CLI pipeline with checkpoints (`run_pipeline.py`, steps 1–9) — **v1.0**
- ✓ Interpretable regimes with pinned labels and reproducible macro + ETF-by-regime artifacts — **v1.0**
- ✓ Current regime, transitions, portfolio-aware recommendations, weekly report — **v1.0**
- ✓ Machine-readable outputs and operational **`RUNBOOK.md`** — **v1.0**

#### Out of Scope

- Individual-stock selection or ranking; all analysis is at the ETF level.
- Handling intraday data or sub-daily decision-making.
- Auto-executing trades with brokers or exchanges.
- Direct integration with individual crypto wallets or exchanges.

### Key Decisions (So Far)

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Focus on ETF-level portfolios only (no individual stocks) | Simpler, more robust universe; aligns with available data and reduces overfitting risk. | **Locked for v1** |
| Allow bitcoin exposure only via ETF wrappers | Avoid operational/security complexity of direct crypto while still capturing the macro signal. | **Locked for v1** |
| Weekly report cadence | Matches the regime/quarterly focus; avoids false precision from daily/intraday noise. | **Locked for v1** |

---

## Milestone model (aligned with GSD)

### v1.0 — Core pipeline + planning evidence (**shipped**)

**Status:** ✅ **Complete** — **2026-03-20** (git tag **`v1.0`**). Full roadmap, requirements, and audit: **`.planning/milestones/v1.0-ROADMAP.md`**, **`v1.0-REQUIREMENTS.md`**, **`v1.0-MILESTONE-AUDIT.md`**. Ledger: **`.planning/MILESTONES.md`**.

### v1.2 — Tactics, Triggers & Expanded Signals (**current** milestone)

**Status:** **Not yet** split into new phases on **`.planning/ROADMAP.md`**. Start with **`$gsd-new-milestone`** (phase numbering continues from **17**).

**Goal:** Deepen Trading-Crab from regime-aware strategy into actionable tactics by expanding data sources, adding richer signals (ratios, correlations, differential-equation-style views), upgrading models, and wiring the weekly report all the way to email delivery.

**Target features (high level):**
- **Email delivery first (D):** Simple SMTP-based sending of the weekly report (e.g. via Gmail) with email address and SMTP credentials stored in a local, non-committed config file.
- **More macro + ratios (A):** Additional FRED series (e.g. VIX, UNRATE, M2, yield-curve spreads) and derived triggers/ratios such as Lumber:Gold and Saylor↔Schiff-style signals, Oil:Gold, Oil:Bonds, Bonds:Gold, etc., surfaced as diagnostic plots/tables first.
- **Richer models (B):** Add XGBoost / LightGBM (or similar) alongside RF/DT for regime and forward-return prediction, using non-forward-looking features including correlations, ratios, and higher-order derivatives; always also fit a simple DecisionTree on top RF features and visualize it for human review.
- **Tactics layer (C):** Classify assets into buy-and-hold vs swing-trade vs stand-aside based on volatility at different time scales, trend slope, and correlations, with a focus on weekly entries and multi-day holds, anchored-VWAP-style stop-loss ideas, and soft constraints (no strict enforcement).
- **More assets/APIs:** Broaden ETF/asset coverage (REITs and other investable exposures beyond current broker-specific lists) and evaluate/plug in additional data providers where practical (e.g. stooq, and—optionally and safely—other APIs the user has access to such as finviz Elite), while preserving the existing pipeline’s integrity.

At each step of the pipeline, v1.2 should encourage answers to:
- **Is now a good time to invest at all (vs cash)?**
- **If yes, in what (cash vs stocks vs bonds vs gold vs energy/commodities)?**
- **What should be done now (tactics) and on what horizon?**
- **What human review is helpful here (plots, trees, triggers), and can it be toggled via a flag?**

---

*Last updated: 2026-03-21 — v1.0 shipped and archived; v1.2 is next planning cycle*

