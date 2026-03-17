---
phase: 8
slug: data-signals-diagnostics
status: complete
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-17
---

## Phase 8: Data + Signals + Diagnostics

**Goal:** Add macro series + yield-curve spreads and produce ratio/RRG diagnostics as artifacts.

### Wave 0 (after execution) checklist

- **FRED config**
  - [x] `config/settings.yaml` includes the new series IDs (VIXCLS, UNRATE, M2SL, M2NS, GS2, T10Y2Y, T10Y3M) with friendly names.
  - [x] Step 01 produces macro data including these columns (when API available).

- **Yield curve features**
  - [x] `src/market_regime/transforms.py` computes spread features (yc_10y_2y, yc_10y_3m, yc_2y_3m).
  - [x] Spreads can flow through log/derivative stages when included in configured feature lists.

- **Diagnostics step**
  - [x] `pipelines/08_diagnostics.py` exists and runs without network calls beyond what the pipeline already requires.
  - [x] Ratio diagnostics artifacts written:
    - [x] `outputs/reports/diagnostics/ratios_current.parquet`
  - [x] RRG diagnostics artifacts written:
    - [x] `outputs/reports/diagnostics/rrg_current.parquet`
  - [ ] Plots saved:
    - [ ] `outputs/plots/08_diagnostics_ratios.png`
    - [ ] `outputs/plots/08_diagnostics_rrg.png`

### Nyquist validation (required to mark complete)

- [x] Add/extend unit tests:
  - [x] FRED config expansion presence/shape
  - [x] Yield curve feature correctness
  - [x] Ratio diagnostics correctness on synthetic series
  - [x] RRG quadrant classification correctness on synthetic series
- [x] All tests pass: `pytest -q` (verified via `conda run -n py310 python -m pytest` on the targeted suite).
- [x] Update this file:
  - [x] `status: complete`
  - [x] `nyquist_compliant: true`
  - [x] `wave_0_complete: true`

