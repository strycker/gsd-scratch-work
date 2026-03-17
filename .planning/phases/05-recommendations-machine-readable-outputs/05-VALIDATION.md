## Phase 5 — Recommendations & Machine-Readable Outputs — Validation

- **phase_id**: 5
- **phase_key**: 05-recommendations-machine-readable-outputs
- **milestone**: v1.1 ETF Behavior & Portfolios
- **status**: complete
- **nyquist_compliant**: true

### Scope

This phase turns regime and behavior insights into concrete ETF-level recommendations and structured artifacts that can be consumed by downstream tools (e.g. the weekly report and email pipeline).

### Preconditions

- [x] Phases 1–4 are validated and produce stable data, regimes, and regime-conditional ETF/portfolio behavior tables.
- [x] A current ETF portfolio can be specified via configuration.

### What Was Validated

- [x] **Per-ETF signals**: For each ETF in the configured universe, the system emits buy/hold/sell or green/neutral/red signals consistent with the documented thresholds and scoring rules.
- [x] **Portfolio deltas**: Given a current portfolio and a target regime-aware mix, the system computes incremental weight adjustments (deltas) rather than hard resets, with simple safeguards against excessive turnover.
- [x] **Explanations**: Each recommendation includes a short, human-readable rationale grounded in regime conditions and regime-conditional ETF/portfolio behavior statistics.
- [x] **Machine-readable bundle**: A structured artifact (e.g. `outputs/reports/recommendation_bundle.parquet` and/or CSV/JSON equivalents) is produced containing:
  - Current regime probabilities and key transition probabilities.
  - Per-ETF signals and suggested trades.
  - Portfolio-level summary metrics.
- [x] **Contracts respected**: Filenames, columns, and schemas for recommendation artifacts match what the weekly report and tests expect.

### Tests & Evidence

- [x] Automated tests around:
  - Absolute and relative signal thresholds (green/red/neutral semantics).
  - Presence and basic shape of the recommendation bundle artifact.
- [x] Manual sanity checks that recommendations for a few representative dates/portfolios line up with regime intuition and historical behavior.

### Known Limitations

- [x] Recommendation logic is deliberately simple (no full mean-variance optimizer); later milestones may refine position sizing and constraints.
- [x] Turnover controls are basic and rely on configuration rather than a fully formalized cost model.

### Validation Decision

- [x] Phase 5 is **complete** and its recommendation artifacts are stable enough to be used by the weekly report pipeline and email delivery.

