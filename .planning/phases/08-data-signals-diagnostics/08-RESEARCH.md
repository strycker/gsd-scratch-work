# Phase 8 — Data + Signals + Diagnostics: Research

**Researched:** 2026-03-17  
**Domain:** Macro data expansion (FRED) + diagnostic ratios/triggers + Relative Rotation Graphs (RRG)  
**Confidence:** MEDIUM (concepts clear; exact data availability varies by series / vendor)  

## Goal

Extend Trading-Crab’s macro input coverage and add **diagnostic “why” layers** that help humans sanity-check regimes and recommendations:

- **More macro series (FRED)** including VIX, unemployment, money supply, and yield curve slope.
- **Derived yield-curve features** (explicit spreads) alongside the existing macro feature set.
- **Ratio / trigger diagnostics** (Oil:Gold, Oil:Bonds, Bonds:Gold, Lumber:Gold, Saylor↔Schiff-style) surfaced as plots/tables first.
- **RRG (Relative Rotation Graph) diagnostics** for ETFs vs benchmark(s) across weekly/quarterly/yearly windows, always with quarterly regime context.

This phase is about **data + visibility** (diagnostics), not changing the core regime definitions or recommendations logic.

## Inputs and canonical IDs (FRED)

These are the canonical series IDs to add (all can be ingested via the existing `src/market_regime/ingestion/fred.py` which fetches whatever is present in `config/settings.yaml`):

### Requested core additions (v1.2 Phase 8)

- **VIX**: `VIXCLS` (daily)
- **Unemployment**: `UNRATE` (monthly)
- **Money supply**: `M2SL` (monthly, seasonally adjusted) and `M2NS` (monthly, not seasonally adjusted)
- **2Y yield**: `GS2` (monthly)
- **Yield curve spreads**: `T10Y2Y` (daily), `T10Y3M` (daily)

### Optional “weekly-friendly” complements (if we decide to support weekly diagnostics from FRED directly)

- **10Y yield daily**: `DGS10`
- **2Y yield daily**: `DGS2`
- **3M T-bill daily**: `DTB3`
- **WTI crude weekly**: `WCOILWTICO` (weekly)

Notes:

- The pipeline currently resamples every FRED series to **quarter-end** (`.resample("QE").last()`); mixing daily/monthly series is fine under that contract.
- Some historical “spot gold fixing” series previously used in FRED have been discontinued; for Phase 8 we can prefer **ETF proxies** (e.g., GLD) for robust availability, while optionally supporting any still-active gold proxy series later.

## Yield curve features (derived)

For supervised/regime feature engineering, we want the spreads explicitly present as columns (and therefore eligible for log transforms / derivatives just like other inputs):

- \( \text{yc\_10y\_2y} = \text{fred\_gs10} - \text{fred\_gs2} \) (monthly-based)
- \( \text{yc\_10y\_3m} = \text{fred\_gs10} - \text{fred\_tb3ms} \) (monthly-based)
- \( \text{yc\_2y\_3m} = \text{fred\_gs2} - \text{fred\_tb3ms} \) (monthly-based)

We can also ingest `T10Y2Y` / `T10Y3M` directly (daily-based), but derived-from-monthly spreads keep the feature set consistent with existing `fred_gs10` / `fred_tb3ms` inputs.

## Ratio / trigger diagnostics

We should keep these as **diagnostic artifacts** first (plots/tables), not hardwired allocation rules. Targets include:

- **Oil:Gold** (e.g., USO / GLD or WTI proxy / gold proxy)
- **Oil:Bonds** (e.g., USO / TLT)
- **Bonds:Gold** (e.g., TLT / GLD)
- **Lumber:Gold** (proxy: a lumber ETF / construction materials proxy vs GLD)
- **Saylor↔Schiff-style**: treat as a configurable ratio family (numerator/denominator tickers), so we can add/iterate without code changes.

Deliverable shape should be consistent: time series + z-score / percentile vs history, plus regime overlays and “current reading”.

## RRG (Relative Rotation Graph) diagnostics (first pass)

RRG is built from each asset’s price relative to a benchmark:

- **RS**: \( RS_t = 100 \times \frac{P^{asset}_t}{P^{benchmark}_t} \)
- **RS-Ratio**: standardized / normalized smoothed RS (centered around 100)
- **RS-Momentum**: standardized rate-of-change of RS-Ratio (also centered around 100)

We do not need to exactly replicate proprietary “JdK” smoothing in Phase 8; we need **consistent, documented, and testable** calculations that yield sensible quadrants:

- **Leading**: RS-Ratio > 100 and RS-Momentum > 100
- **Weakening**: RS-Ratio > 100 and RS-Momentum < 100
- **Lagging**: RS-Ratio < 100 and RS-Momentum < 100
- **Improving**: RS-Ratio < 100 and RS-Momentum > 100

We will compute RRG views for:

- Benchmarks: **SPY (default)**, **VT**, and a **60/40 template** (already config-driven in `config/settings.yaml` templates)
- Time scales: **weekly**, **quarterly**, **yearly**, with **quarterly regime labels** used for annotation/overlays

## Risks / pitfalls

- **FRED series frequency mismatches**: monthly/daily are fine for quarterly resample, but if we add weekly diagnostics, we must be explicit about weekly resampling rules.
- **Missingness & inception dates**: VIX starts ~1990; spreads start ~1976/1982; weekly diagnostics must gracefully handle NaNs.
- **Do not destabilize regime clustering**: adding features changes cluster geometry. Phase 8 should treat these as additive *data availability* + *diagnostics* first; any feature-list changes that feed clustering should be deliberate and versioned.