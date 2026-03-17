## Phase 9 — Tactics & Diagnostics Integration — Validation

- **phase_id**: 9
- **phase_key**: 09-tactics-and-diagnostics
- **milestone**: v1.2 Tactics, Triggers & Expanded Signals
- **status**: complete
- **nyquist_compliant**: true

### Scope

This phase integrates diagnostics (ratios, RRG) and tactics signals into the main Trading-Crab pipeline and weekly report so that tactical views are first-class citizens alongside regimes and recommendations.

### Preconditions

- [x] Phase 8 diagnostics (ratios, RRG, additional FRED series, yield-curve features) is validated and produces its artifacts.
- [x] Tactics metrics and labels are implemented in `src/market_regime/tactics.py` and tested.

### What Was Validated

- [x] **Diagnostics wiring**:
  - [x] `pipelines/08_diagnostics.py` (or equivalent step function) runs as part of the configured pipeline steps and writes:
    - [x] `outputs/reports/diagnostics/ratios_current.parquet`
    - [x] `outputs/reports/diagnostics/rrg_current.parquet`
  - [x] No additional network dependencies were introduced beyond existing ingestion.
- [x] **Tactics integration**:
  - [x] A dedicated tactics step exists (e.g. `step9_tactics` in `run_pipeline.py`) that:
    - [x] Loads ETF prices and current/forward regime labels from checkpoints.
    - [x] Computes per-asset tactics metrics (volatility, trend, correlation) using config thresholds.
    - [x] Produces `outputs/reports/tactics_signals.parquet` with columns for metrics and `tactics_label`.
  - [x] `write_weekly_report_md` in `reporting.py` reads `tactics_signals.parquet` and appends a **Tactics** section (buy-and-hold, swing, stand-aside candidates).
- [x] **Contracts respected**:
  - [x] Filenames, columns, and semantics of diagnostics and tactics artifacts match expectations of tests and the weekly report.

### Tests & Evidence

- [x] Unit tests:
  - [x] `tests/unit/test_diagnostics_rrg.py` covers diagnostics helpers and RRG behavior.
  - [x] `tests/test_tactics.py` covers tactics metric calculations and label assignment on synthetic data.
- [x] Manual sanity checks:
  - [x] One run of the pipeline through diagnostics + tactics steps with visual/manual inspection of artifacts.
  - [x] Weekly report rendered with a tactics section consistent with the generated `tactics_signals.parquet`.

### Known Limitations

- [x] Tactics labels are coarse-grained; more nuanced position sizing and entry/exit rules may be added later.
- [x] Diagnostics plots are available via notebooks and saved figures, but not yet embedded directly into the email.

### Validation Decision

- [x] Phase 9 is **complete** and diagnostics + tactics integration are stable and trustworthy inputs to the weekly report and future tactics work.

