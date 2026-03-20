# Phase 18 — Context (v1.2 signal & diagnostic layer)

**Gathered:** 2026-03-21  
**Status:** Ready for execution (plan **01**)  
**Requirements:** **SIGNAL-10**, **SIGNAL-11**

## Phase boundary

**Deliver:** Product-complete ratio + RS/RRG-style diagnostics per **`.planning/REQUIREMENTS.md`**: config-driven cross-asset ratios with **trigger-style** signals (not model features), benchmark-relative rotation artifacts, **stable parquet outputs**, optional **plots**, and **weekly report + notebook hooks** — building on the v1.0 **step 8** implementation (no duplicate greenfield rewrite unless a gap requires it).

**Depends on:** Phase **17** (expanded macro columns in features). **Does not** change `clustering_features` or regime geometry unless explicitly waived.

## Brownfield inventory (current repo)

| Area | Location | Notes |
|------|----------|--------|
| Step 8 pipeline | `pipelines/08_diagnostics.py` | Loads `asset_prices.parquet`, writes `outputs/reports/diagnostics/ratios_current.parquet`, `rrg_current.parquet`. |
| Core math | `src/trading_crab_lib/diagnostics.py` | `rolling_zscore`, `percentile_rank`, `normalize_100`, `rrg_for_benchmark`. |
| Config | `config/settings.yaml` → `diagnostics.ratios`, `diagnostics.rrg_benchmarks` | Oil:Gold, Oil:Bonds, Bonds:Gold, Lumber:Gold; benchmarks SPY, VT. |
| Tests | `tests/unit/test_diagnostics_rrg.py` | Unit tests for helpers + RRG quadrants; **no** tests for ratio **pipeline** or **08_diagnostics** integration. |
| Weekly report | `src/trading_crab_lib/reporting.py` → `write_weekly_report_md` | Optional **Tactics** section when `tactics_signals.parquet` exists; **no** diagnostics section yet. |
| Plots | Step 8 `main()` sets `RunConfig(generate_plots=True)` but **does not** call `plotting` helpers for diagnostics (unlike other steps). |

## Gaps vs REQUIREMENTS / ROADMAP

| Requirement / criterion | Gap |
|-------------------------|-----|
| **SIGNAL-10** “trigger diagnostics” | Current output is latest value + z + percentile; **no** config bands / fired triggers / narrative labels. |
| **SIGNAL-10** “plots/tables” | Parquet only; **no** saved figures under `outputs/plots/` for step 8 (Phase 8 validation noted plots unchecked). |
| **SIGNAL-11** “notebook/report hooks” | **No** `notebooks/08_diagnostics.ipynb`; weekly report **does not** reference diagnostics. |
| **Roadmap** §18 success #3 | “Weekly report and/or plots reference new sections when configured” — **not** met until report + plots wired. |

## Locked decisions (for Plan 01)

1. **Extend `diagnostics` in `settings.yaml`** with optional **trigger rules** (e.g. global or per-ratio thresholds on `latest_zscore` and/or `percentile`) producing explicit columns such as `trigger` / `trigger_detail` in `ratios_current.parquet` — keep rules **diagnostic-only** (do not feed into `features.parquet` in this phase).
2. **Plots:** Add `trading_crab_lib/plotting.py` helpers (names TBD in implementation) for a **ratio summary** figure and an **RRG-style scatter** (rs_ratio vs rs_momentum) per benchmark; save with existing naming convention `outputs/plots/08_*.png` when `RunConfig.save_plots` and step 8 runs.
3. **Weekly report:** Extend `write_weekly_report_md` with an optional `## Diagnostics` section when `outputs/reports/diagnostics/ratios_current.parquet` and/or `rrg_current.parquet` exist and `diagnostics.weekly_report_include` is **true** (default **true** once implemented).
4. **Notebook:** Add `notebooks/08_diagnostics.ipynb` that loads the two parquets and displays heads + pointers to plot paths (minimal, no new scraping).
5. **Tests:** Add integration-style tests for ratio rows + trigger evaluation on synthetic prices; extend weekly report test to assert diagnostics section when fixtures present.

## Canonical references

- `.planning/ROADMAP.md` — Phase 18 goal & success criteria  
- `.planning/REQUIREMENTS.md` — SIGNAL-10, SIGNAL-11  
- `RUNBOOK.md` — extended pipeline steps 8–9  
- `.planning/phases/08-data-signals-diagnostics/` — historical Phase 8 design notes (`08-VALIDATION.md`, `*-PLAN.md`) — **reference only**; v1.2 work lives under phase **18** artifacts.

## Deferred (not Phase 18)

- Promoting any diagnostic series into `features.clustering_features` (explicit separate decision).  
- Exact match to proprietary RRG vendor math (documented approximation only).  
- **TACTICS-10** (Phase 20), **MODEL-10** (Phase 19).
