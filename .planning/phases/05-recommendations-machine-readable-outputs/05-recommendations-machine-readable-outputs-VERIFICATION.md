---
phase: 05-recommendations-machine-readable-outputs
verified: 2026-03-19T00:00:00Z
status: passed
score: 3/3 requirements satisfied (UX-01..03)
human_verification:
  - test: "Read trade_recommendations.csv and weekly_report.md after a full run"
    expected: "BUY/SELL/HOLD deltas align with blended targets vs config/portfolio.yaml; weekly bullets read clearly to a human advisor."
    why_human: "Wording quality and whether explanations feel 'grounded' enough is subjective."
---

# Phase 5: Recommendations & Machine-Readable Outputs — Verification

**Phase goal (ROADMAP):** Actionable ETF recommendations + machine-readable bundles.  
**Audit closure:** Phase 12 — evidence for UX-01..03.  
**Status:** **passed**.

## Requirement coverage

| ID | Description | Status | Evidence |
|----|-------------|--------|----------|
| UX-01 | Incremental per-ETF buy/hold/sell vs portfolio | ✓ | `generate_recommendation(target_weights, current_weights=..., threshold=...)` in `trading_crab_lib.reporting`. `run_pipeline.step7_dashboard` and `pipelines/07_dashboard.py` use `load_portfolio()` and `dashboard.recommendation_threshold` (default 0.03). |
| UX-02 | Brief explanation per recommendation | ✓ | `write_weekly_report_md` — per-asset lines with target vs current delta (`outputs/reports/weekly_report.md`). `trade_recommendations.csv` carries `signal`, `delta_pct`; narrative primarily in markdown (not a separate prose column in CSV). |
| UX-03 | Machine-readable artifacts | ✓ | `save_dashboard_csv` → `outputs/reports/dashboard.csv` (or dir convention from `save_dashboard_csv`). `portfolio_simple.csv`, `portfolio_blended.csv`, `trade_recommendations.csv`. `save_recommendation_bundle` → `outputs/reports/recommendation_bundle.parquet` when `etf_behavior_by_regime.parquet` exists. |

## Key entrypoints

| Component | Path |
|-----------|------|
| Canonical CLI step | `run_pipeline.py` `step7_dashboard` |
| Stand-alone | `pipelines/07_dashboard.py` |
| Core logic | `src/trading_crab_lib/reporting.py` |

## Changelog (Phase 12 execution)

- **2026-03-19:** `run_pipeline.step7_dashboard` aligned with `pipelines/07_dashboard.py`: portfolio-aware `generate_recommendation`, `recommendation_bundle.parquet` via `build_recommendation_digest` / `save_recommendation_bundle`.
