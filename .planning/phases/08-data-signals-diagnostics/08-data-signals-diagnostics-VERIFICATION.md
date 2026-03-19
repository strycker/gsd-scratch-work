---
phase: 08-data-signals-diagnostics
verified: 2026-03-19T00:00:00Z
status: passed
score: 3/3 roadmap success themes (DATA-04, DIAG-01, DIAG-02)
human_verification:
  - test: "Run step 1 with FRED_API_KEY set and --refresh; inspect macro_raw for fred_vix, fred_unrate, fred_t10y2y, …"
    expected: "New columns present for each configured FRED series where API returns data."
    why_human: "Network + API availability; column names depend on successful fetch."
  - test: "Run step 8 after asset_prices.parquet exists; open outputs/reports/diagnostics/*.parquet"
    expected: "Non-empty ratio and RRG frames when ETFs in config match price columns."
    why_human: "ETF history length and column alignment."
---

# Phase 8: Data + Signals + Diagnostics — Verification

**Phase goal (ROADMAP):** Richer FRED inputs, config-driven diagnostic ratios, and RRG-style machine-readable outputs.  
**Audit closure:** Phase 13 — evidence for DATA-04, DIAG-01, DIAG-02.  
**Status:** **passed** (ROADMAP examples explicitly checked against `settings.yaml`).

## Requirement coverage

| ID | Description | Status | Evidence |
|----|-------------|--------|----------|
| DATA-04 | Additional FRED series (e.g. VIX, unemployment, M2, yield-curve spreads) configured and ingested when available | ✓ | `config/settings.yaml` → `fred.series` includes **VIXCLS** (`fred_vix`), **UNRATE** (`fred_unrate`), **M2SL** / **M2NS**, **T10Y2Y**, **T10Y3M**, **GS2**, **HOUST**, **UMCSENT**, and existing core series. Ingestion uses `trading_crab_lib.ingestion.fred` from step 1 (`pipelines/01_ingest.py` / `run_pipeline.step1_ingest`). **Honesty:** Series appear in config; actual columns in `macro_raw` require a successful FRED fetch (no offline guarantee in CI). |
| DIAG-01 | Yield/spread series + key ratios (Oil:Gold, Oil:Bonds, Bonds:Gold, Lumber:Gold proxy, …) computed and surfaced as diagnostics | ✓ | Spread **levels** arrive via FRED (`fred_t10y2y`, `fred_t10y3m`). **Ratio** diagnostics are ETF-based: `config/settings.yaml` → `diagnostics.ratios` lists Oil:Gold (USO/GLD), Oil:Bonds (USO/TLT), Bonds:Gold (TLT/GLD), Lumber:Gold proxy (XLB/GLD). Implemented in `pipelines/08_diagnostics.py` + `trading_crab_lib.diagnostics`. Output: `outputs/reports/diagnostics/ratios_current.parquet`. |
| DIAG-02 | RRG-style diagnostics (RS-ratio, RS-momentum) as machine-readable artifacts vs benchmark(s) | ✓ | `diagnostics.rrg_benchmarks` lists **SPY**, **VT**. `rrg_for_benchmark` in `trading_crab_lib.diagnostics`; step 8 writes `outputs/reports/diagnostics/rrg_current.parquet`. |

## Pipeline wiring

| Step | Function | Output dirs/files |
|------|----------|-------------------|
| 1 | Ingest multpl + FRED | `data/raw/macro_raw.parquet` |
| 8 | Diagnostics | `outputs/reports/diagnostics/ratios_current.parquet`, `rrg_current.parquet` |

`run_pipeline.py` registers **`step8_diagnostics`** as `STEPS[8]`; docstring lists step 8 path under `outputs/reports/diagnostics/`.

## ROADMAP vs config audit (explicit)

| ROADMAP example | Present in `settings.yaml` |
|-----------------|----------------------------|
| VIXCLS | ✓ |
| UNRATE | ✓ |
| M2 (M2SL / M2NS) | ✓ |
| Yield-curve spreads (10Y–2Y, 10Y–3M) | ✓ (`T10Y2Y`, `T10Y3M`) |

**gaps_found:** None for the Phase 8 roadmap bullet list relative to current FRED config. (Optional Tier-1 items beyond this phase may still be tracked in `ROADMAP.md` / v1.2 notes.)

## Tests

| Test file | Coverage |
|-----------|----------|
| `tests/unit/test_diagnostics_rrg.py` | RRG helper behavior (unit, no full pipeline) |
| `tests/unit/test_fred_series_config.py` | FRED series config surface (if asserts expected IDs) |

## `key_links`

| From | To | Via |
|------|----|-----|
| `config/settings.yaml` (`fred.series`) | `macro_raw` columns | Step 1 FRED fetcher |
| `config/settings.yaml` (`diagnostics`) | `ratios_current.parquet` | `step8_diagnostics` |
| `config/settings.yaml` (`rrg_benchmarks`) | `rrg_current.parquet` | `rrg_for_benchmark` |

## Notes

- Step 8 is **read-only** with respect to regimes/features: it consumes existing ETF prices + config (`pipelines/08_diagnostics.py` header comment).

## Evidence checklist (audit)

- [x] `fred.series` lists expanded macro IDs matching ROADMAP Phase 8 examples (`config/settings.yaml`).
- [x] Ingestion code path exists for FRED (`trading_crab_lib.ingestion.fred`, used from step 1).
- [x] `diagnostics.ratios` and `diagnostics.rrg_benchmarks` present in YAML.
- [x] Step 8 writes `ratios_current.parquet` and `rrg_current.parquet` under `outputs/reports/diagnostics/`.
- [x] `run_pipeline.py` documents step 8 in header + `STEPS` map.

## Dependencies between steps

- Step **1** (or cached `macro_raw`) required for DATA-04 columns after fetch.
- Step **6** / `asset_prices.parquet` required before step 8 can compute ETF-based ratios and RRG.
- Step 8 does **not** require step 9.

## Revision history

- 2026-03-19 — Phase 13 audit: initial `*-VERIFICATION.md` for roadmap Phase 8.
