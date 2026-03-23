# Phase 20: v1.2 — Tactics classification (TACTICS-10)

**Gathered:** 2026-03-22  
**Status:** Ready for planning  
**Source:** Roadmap Phase 20, `.planning/REQUIREMENTS.md` **TACTICS-10**, existing `trading_crab_lib.tactics` + step 9 pipeline

## Phase boundary

Deliver **TACTICS-10**: extend the shipped tactics layer (v1.0 Phases 9–10) so classification explicitly uses **multi-horizon** volatility/trend inputs, adds **weekly-entry bias** and a **soft-stop proxy** (no broker execution), and writes a **stable, machine-readable** `outputs/reports/tactics_signals.parquet` that includes an **as-of** date (and quarter identifier) per run. **Weekly report** gains richer **Tactics** content when new columns exist. **Unit tests** cover label logic on synthetic price paths.

Out of scope: auto-trading, intraday execution, new pipeline step numbers (remain step 9 / `09_tactics.py`).

## Implementation decisions (locked)

- **Build on existing module** — Extend `src/trading_crab_lib/tactics.py` and `config/settings.yaml` `tactics:`; do not fork a second tactics implementation.
- **Parquet path unchanged** — `outputs/reports/tactics_signals.parquet` (append columns; preserve `asset`, `tactics_label`, existing metric columns for backward compatibility).
- **Multi-horizon rule** — Combine per-window `vol_*` using a **configurable reducer** (`max` default for conservative stand-aside when any horizon is “high vol”) instead of a single mid-column pick.
- **Weekly-entry bias** — Derived from **alignment of short vs long trend slopes** (e.g. additional short `trend_windows` entry) as a numeric `entry_bias_score` in `[-1, 1]` or discrete `favorable|neutral|unfavorable`; documented in YAML.
- **Soft-stop proxy** — **No volume-based VWAP** unless price data extended; use **z-score of last close vs rolling mean** over configurable window (`soft_stop_proxy` block) — informational only.
- **As-of / quarter** — Add `as_of` (last bar timestamp) and `quarter_end` (calendar quarter end string or timestamp) derived from the price panel index — satisfies ROADMAP “keyed by ETF and date/quarter” at **snapshot** granularity (one row per ETF per run).

## Claude's discretion

- Exact formula for `entry_bias_score` (tanh vs raw difference), default thresholds for bias bands.
- Whether to add optional `plotting` hook for tactics strip chart (only if low effort; not required for TACTICS-10).

## Canonical references

Downstream agents **must** read:

- `.planning/ROADMAP.md` — Phase 20 goal + success criteria  
- `.planning/REQUIREMENTS.md` — **TACTICS-10** bullet  
- `src/trading_crab_lib/tactics.py` — current metrics + `classify_tactics`  
- `pipelines/09_tactics.py` / `run_pipeline.py` — `step9_tactics`  
- `src/trading_crab_lib/reporting.py` — `## Tactics` block  
- `tests/test_tactics.py` — existing synthetic tests  
- `RUNBOOK.md` — step 9 documentation  

## Deferred

- Anchored VWAP with real intraday volume — deferred until price ingest exposes volume consistently.

---

*Phase: 20-v1-2-tactics-layer*
