---
phase: 04-regime-conditional-etf-portfolio-behavior
verified: 2026-03-19T00:00:00Z
status: passed
score: 3/3 requirements satisfied (PORT-01..03)
human_verification:
  - test: "Inspect asset_return_profile and behavior parquets on a full pipeline run"
    expected: "Medians/ranks look plausible vs known ETF history; template rows match config/portfolio_templates names."
    why_human: "Numeric sanity and economic interpretation are judgment calls."
---

# Phase 4: Regime-Conditional ETF & Portfolio Behavior — Verification

**Phase goal (ROADMAP):** Quantify ETF and template portfolio behavior by regime.  
**Audit closure:** Phase 12 — evidence for PORT-01..03.  
**Status:** **passed** (canonical path: `python run_pipeline.py --steps 6` matches `pipelines/06_asset_returns.py` after parity fix).

## Requirement coverage

| ID | Description | Status | Evidence |
|----|-------------|--------|----------|
| PORT-01 | Regime-conditional ETF return distributions | ✓ | `src/trading_crab_lib/asset_returns.py`: `returns_by_regime`, `rank_assets_by_regime`, `behavior_tables`. `run_pipeline.step6_asset_returns` and `pipelines/06_asset_returns.py` write `data/regimes/asset_return_profile.parquet` and `data/regimes/etf_behavior_by_regime.parquet`. |
| PORT-02 | Named portfolio templates evaluated by regime | ✓ | `config/settings.yaml` → `assets.portfolio_templates`. `compute_template_returns` + `behavior_tables` → `data/regimes/template_behavior_by_regime.parquet` when templates non-empty (**both** `run_pipeline.step6` and `pipelines/06_asset_returns.py`). |
| PORT-03 | User / blended regime expectations for holdings | ✓ | `run_pipeline.step7_dashboard` + `pipelines/07_dashboard.py`: `predict_current`, `transition_matrix`, `simple_regime_portfolio`, `blended_regime_portfolio` from `trading_crab_lib.reporting` and `asset_return_profile.parquet`. |

## Key code ↔ artifact links

| From | To | Via |
|------|----|-----|
| `run_pipeline.py` `step6_asset_returns` | `data/regimes/asset_return_profile.parquet` | `returns_by_regime` |
| `run_pipeline.py` `step6_asset_returns` | `data/regimes/etf_behavior_by_regime.parquet` | `behavior_tables` |
| `run_pipeline.py` `step6_asset_returns` | `data/regimes/template_behavior_by_regime.parquet` | `compute_template_returns` + `behavior_tables` if `assets.portfolio_templates` |
| `pipelines/06_asset_returns.py` | Same three parquets | Same helpers (stand-alone runner) |

## Automated tests

- `tests/unit/test_returns.py` — `returns_by_regime`, `rank_assets_by_regime`, `compute_quarterly_returns`, etc. (no network).

## Changelog (Phase 12 execution)

- **2026-03-19:** `run_pipeline.step6_asset_returns` extended to write `etf_behavior_by_regime.parquet` and conditional `template_behavior_by_regime.parquet`, matching `pipelines/06_asset_returns.py`.
