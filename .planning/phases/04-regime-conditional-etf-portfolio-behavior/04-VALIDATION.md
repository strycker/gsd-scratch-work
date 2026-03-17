## Phase 4 — Regime-Conditional ETF & Portfolio Behavior — Validation

- **phase_id**: 4
- **phase_key**: 04-regime-conditional-etf-portfolio-behavior
- **milestone**: v1.1 ETF Behavior & Portfolios
- **status**: complete
- **nyquist_compliant**: true

### Scope

This phase quantifies how individual ETFs and simple portfolio templates behave across the discovered market regimes, using the Trading-Crab pipeline and legacy reference implementation as ground truth.

### Preconditions

- [x] Phase 1 data foundations are in place and produce stable features and checkpoints.
- [x] Phase 2 regime clustering and naming are complete and reproducible.
- [x] Phase 3 supervised models can emit current and forward regime labels on demand.

### What Was Validated

- [x] **ETF returns by regime**: For each in-scope ETF, quarterly regime-conditional return distributions (median, quantiles, basic risk metrics) are computed from historical data with no look-ahead leakage.
- [x] **Portfolio templates**: A small library of named portfolio templates (e.g. risk-on, risk-off, inflation-hedged) is defined in configuration and evaluated with regime-conditional performance statistics.
- [x] **User portfolio hooks**: Given a user-specified ETF portfolio, the system can report expected return and simple risk metrics under the inferred current regime and the near-term forward regimes.
- [x] **Artifacts**: Regime-conditional ETF and portfolio behavior tables are saved in `outputs/` (and/or via checkpoints) in machine-readable form for downstream recommendation logic.

### Tests & Evidence

- [x] Unit / integration tests covering:
  - Regime-conditional ETF return tables.
  - Portfolio template evaluation.
- [x] Manual inspection of a sample of ETFs across multiple regimes to confirm that behavior matches domain expectations (e.g. bonds vs equities in stress regimes).
- [x] Sanity-check plots/notebooks verifying that per-regime performance surfaces are stable across reruns with the same config.

### Known Limitations

- [x] Historical coverage is limited by ETF inception dates; pre-ETF history relies on macro proxies where necessary.
- [x] Portfolio templates are intentionally simple and may be expanded in later milestones.

### Validation Decision

- [x] Phase 4 is **complete** and its outputs are reliable enough to be consumed by Phase 5 recommendations and downstream reporting.

