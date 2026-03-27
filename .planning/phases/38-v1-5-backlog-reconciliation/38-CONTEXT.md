# Phase 38: Backlog reconciliation — Context

**Gathered:** 2026-03-27  
**Status:** Ready for planning  
**Source:** `.planning/ROADMAP.md` (v1.5) + `.planning/REQUIREMENTS.md` (**TMPL-02**)

## Phase boundary

Align **product-facing markdown** (root **`ROADMAP.md`**, **`.planning/FUTURE-TODO.md`**, **`CLAUDE.md`**) with **`src/trading_crab_lib`** as it exists today — especially:

- **Yield-curve features:** Implementation uses **`add_yield_curve_features`** in **`transforms.py`** producing **`yc_10y_2y`**, **`yc_10y_3m`**, **`yc_2y_3m`** (from **fred_gs10**, **fred_gs2**, **fred_tb3ms**). Root **`ROADMAP.md`** §1.3 still describes older **`yield_spread_*`** / **`yield_curve_slope`** names.
- **Empirical forward-window probabilities:** Implemented as **`build_forward_window_probabilities()`** in **`regime.py`**, called from **`pipelines/04_regime_label.py`**, writing **`data/regimes/forward_window_probabilities.parquet`**. Docs still cite legacy **`compute_forward_probabilities()`** only and **`legacy/regime_analysis.py`** as the sole reference.

**Non-goals:** Implementing **TMPL-03** (confusion matrix plot) — that is **Phase 39**. Changing **`profiler.py`** or clustering logic. Editing **`legacy/**`.

## Locked decisions

- **Naming:** Prefer **`build_forward_window_probabilities`** + **`forward_window_probabilities.parquet`** in user-facing backlog text; mention **`compute_forward_probabilities`** only as legacy alias for readers comparing to **`legacy/**`**.
- **Yield curve:** Document **`yc_*`** as the shipped feature names; keep Tier 1 roadmap item as “expand / tune” if needed, not “implement from scratch” for spreads already present.
- **Confusion matrix:** Remains an open gap until Phase **39**; **`CLAUDE.md`** should stay consistent (one source of truth: **Remaining Gaps** vs **Next Priority**).

## Canonical code references

- `src/trading_crab_lib/transforms.py` — `add_yield_curve_features`
- `src/trading_crab_lib/regime.py` — `build_forward_window_probabilities`
- `pipelines/04_regime_label.py` — parquet write path
- `tests/unit/test_forward_window_probabilities.py`, `tests/unit/test_yield_curve_features.py`

## Deferred

- Root **`ROADMAP.md`** Tier 1 items not in TMPL-02 scope (LightGBM, macrotrends, etc.) — **touch only** where they contradict shipped code.
