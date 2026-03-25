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

#### Active (next milestone) — v1.3

- [ ] **Consolidation & OSS library** — see **Current Milestone: v1.3** below.

#### Deferred (post-v1.3 / future)

- Ideas from **`milestones/v1.2-REQUIREMENTS.md`**: HMM / temporal clustering, full broker execution, empirical forward probabilities, macrotrends backfill, etc. — not part of v1.3 unless pulled in explicitly.

#### Validated (shipped — v1.2)

- ✓ Expanded FRED macro + yield spreads; optional data providers; preservation secondaries — **v1.2**
- ✓ Ratio/RRG diagnostics; tactics classification; boosted models + configurable live regime model (**RF/GB**) — **v1.2**
- ✓ Weekly pipeline ordering (**8 → 9 → 7**) and `run_weekly_report.py` alignment with diagnostics/tactics — **v1.2**

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
| v1.2 boosted models + `dashboard.regime_model` | RF remains default; GB selectable for live scoring with explicit pickle resolution. | **Shipped v1.2** |
| v1.2 step order for weekly E2E | When steps **7+8+9** run together, order **8 → 9 → 7** so `weekly_report.md` can include diagnostics/tactics. | **Shipped v1.2** |

---

## Milestone model (aligned with GSD)

## Current Milestone: v1.3 — Consolidation, submodule parity & PyPI

**Goal:** Complete outstanding planning hygiene, reconcile the canonical repo with three read-only submodule mirrors so this tree is the **superset**, and publish **`trading-crab-lib`** (from `src/` only) as **public OSS** on PyPI with a credible consumer story.

**Target features:**

- Close **GSD I001** gaps: add **hybrid** `*-SUMMARY.md` files (as-built + plan fidelity + delta-from-plan) for every plan missing a summary; no reopened code scope unless a delta exposes a defect.
- **Analyze & compare** root vs `trading-crab-lib-repo-copy`, `claude-scratch-work-repo-copy`, and `trading-crab-repo-copy` (local mirrors only; **read-only** except `git pull` refresh). Prefer the **more complete / better-tested** implementation when repos diverge; **confirm with owner** before replacing code. Primary merge order: **lib → claude-scratch → trading-crab**, refined by dependency/risk.
- **PyPI:** single package **`trading-crab-lib`** from `src/`; pipelines/notebooks remain **repo-only**. Target **Python 3.10–3.14**; semantic versioning and changelog discipline for OSS.
- **Simplify root:** prune redundant notebooks, scratch paths, and duplicate **root** docs — **do not** prune `legacy/` or submodule trees.
- **Documentation for humans & AI:** extensive **Google-style** docstrings, file-level “why” paragraphs, and short rationale before major blocks throughout `src/trading_crab_lib/` (and aligned root docs where helpful).

**Research:** **`.planning/research/SUMMARY.md`** (2026-03-25) — stack, features/architecture, pitfalls.

## Current position

**v1.2 — Tactics, triggers & expanded signals** is **shipped** (**2026-03-24**, git tag **`v1.2`**). Archives: **`.planning/milestones/v1.2-ROADMAP.md`**, **`v1.2-REQUIREMENTS.md`**, **`v1.2-MILESTONE-AUDIT.md`**. Ledger: **`.planning/MILESTONES.md`**.

**v1.3 — Consolidation & PyPI** is **in definition** — domain research complete; **next:** scoped **`REQUIREMENTS.md`** + **`$gsd-discuss-phase`** / **`$gsd-plan-phase`** starting at phase **28**.

---

### v1.0 — Core pipeline + planning evidence (**shipped**)

**Status:** ✅ **Complete** — **2026-03-20** (git tag **`v1.0`**). **`.planning/milestones/v1.0-ROADMAP.md`**, **`v1.0-REQUIREMENTS.md`**, **`v1.0-MILESTONE-AUDIT.md`**.

### v1.2 — Tactics, triggers & expanded signals (**shipped**)

**Status:** ✅ **Complete** — **2026-03-24** (git tag **`v1.2`**). Expanded signals, diagnostics, boosted models + interpretability, tactics, email/install hardening, GSD gap-closure (**26–27**), and pipeline weekly E2E wiring.

---

*Last updated: 2026-03-25 — v1.3 milestone opened; domain research in **`.planning/research/`***

