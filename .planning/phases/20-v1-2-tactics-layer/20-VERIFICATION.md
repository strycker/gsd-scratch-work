---
phase: 20-v1-2-tactics-layer
verified: 2026-03-23T18:00:00Z
status: human_needed
score: 5/5 plan must-haves (code + tests); roadmap 3/3 criteria mapped
---

# Phase 20: Tactics classification — Verification Report

**Phase goal (ROADMAP):** Asset/tactics buckets (hold / swing / stand-aside) using vol, trend, correlation signals — extended with multi-horizon classification, entry bias, and soft-stop proxy.

**Requirements:** TACTICS-10

**Verified:** 2026-03-23

**Overall status:** `human_needed` — all **plan must-haves** are verified in code and automated tests; **optional human** confirmation for **`python run_pipeline.py --steps 9`** (or `pipelines/09_tactics.py`) with real `asset_prices.parquet` + cluster labels to inspect `outputs/reports/tactics_signals.parquet` columns on disk.

**Scope note:** Real **anchored VWAP** deferred; **`soft_stop_z`** implements rolling-mean z-score proxy per **`20-SUMMARY.md`** / CONTEXT.

---

## Goal achievement

### Observable truths (plan `must_haves`)

| # | Truth | Status | Evidence |
|---|--------|--------|----------|
| 1 | `tactics_signals.parquet` includes `as_of` and quarter identifier plus per-asset metrics; one row per asset per run (snapshot). | ✓ VERIFIED | `compute_tactics_metrics` adds `as_of`, `quarter_end`, `last_price` per row; `pipelines/09_tactics.py` / `step9_tactics` write parquet from `classify_tactics(...).reset_index()`; `tests/test_tactics.py::test_tactics_classification_basic` asserts `as_of` / `quarter_end`. |
| 2 | `classify_tactics` uses configurable multi-horizon vol aggregate (e.g. max across `vol_*`) when `classification_version: v1_2`; documented in settings. | ✓ VERIFIED | `config/settings.yaml` `classification_version`, `vol_aggregate`; `classify_tactics` branches v1 vs v1_2 + `_aggregate_vol`; `test_v1_2_max_vol_can_stand_aside_when_v1_buy_hold` (v1_2 `stand_aside` vs v1 `swing` on same synthetic metrics). |
| 3 | `entry_bias_score` and `soft_stop_z` exist when config enables; no broker execution. | ✓ VERIFIED | `entry_bias_score` via `tanh(slope_short − slope_long)`; `soft_stop_z` via `_soft_stop_z_score`; `soft_stop_proxy.enabled`; `test_entry_bias_score_in_unit_interval`. |
| 4 | `write_weekly_report_md` surfaces enriched tactics when configured and columns exist. | ✓ VERIFIED | `reporting.py` — `tactics.weekly_report_enrich` + `entry_bias_score` / `soft_stop_z` bullets under **## Tactics**. |
| 5 | `pytest tests/test_tactics.py` passes with synthetic fixtures for new logic. | ✓ VERIFIED | 4 tests green (2026-03-23). |

**Truths score:** 5/5 (automated + code evidence).

### Required artifacts (plan frontmatter)

| Artifact | Status | Details |
|----------|--------|---------|
| `config/settings.yaml` | ✓ | `classification_version`, `vol_aggregate`, `entry_bias`, `soft_stop_proxy`, `weekly_report_enrich`, `min_corr_spy`, `trend_windows`. |
| `src/trading_crab_lib/tactics.py` | ✓ | Snapshot columns + v1/v1_2 classification + optional `min_corr_spy`. |
| `src/trading_crab_lib/reporting.py` | ✓ | Enriched Tactics subsection when flag + columns. |
| `tests/test_tactics.py` | ✓ | v1 vs v1_2, bias bounds, `min_corr_spy`. |
| `pipelines/09_tactics.py` / `run_pipeline.py` step 9 | ✓ | No API change required; still `compute_tactics_metrics` → `classify_tactics` → parquet. |

### Key wiring

| Link | Status |
|------|--------|
| `settings.yaml` → `compute_tactics_metrics` / `classify_tactics` | ✓ |
| `tactics_signals.parquet` → `write_weekly_report_md` | ✓ (existing + enrich path) |
| Step 9 → `outputs/reports/tactics_signals.parquet` | ✓ |

---

## ROADMAP success criteria (Phase 20)

| # | Criterion | Evidence |
|---|-----------|----------|
| 1 | Stable parquet keyed by ETF and date/quarter. | `asset` column + `as_of` + `quarter_end` on each row; unit test on synthetic prices. |
| 2 | Weekly report section when artifact present. | Existing **## Tactics** block; optional enrich when `weekly_report_enrich` + columns. |
| 3 | Unit tests for label logic on synthetic fixtures. | `tests/test_tactics.py` (v1, v1_2, min_corr, bias). |

---

## Requirements coverage

| Requirement | Status |
|-------------|--------|
| **TACTICS-10** | ✓ SATISFIED (REQUIREMENTS.md + traceability **Complete**). |

---

## Anti-patterns

Scanned `tactics.py` (new paths), `reporting.py` (tactics enrich): no `TODO`/`FIXME` blockers; reporting keeps broad `except` on tactics read (unchanged).

---

## Human verification (optional)

1. **Full step 9** — With steps 3 + 6 checkpoints, run `python run_pipeline.py --steps 9` and open `outputs/reports/tactics_signals.parquet` (expect `as_of`, `quarter_end`, `entry_bias_score`, `soft_stop_z`).
2. **Weekly enrich** — Set `tactics.weekly_report_enrich: true`, run step 7 after step 9; confirm *Enriched (TACTICS-10)* lines in `weekly_report.md`.

---

## Gaps summary

**None** for TACTICS-10 delivery vs plan must-haves.

---

## Automated commands (re-run)

```bash
cd /path/to/repo
. .venv/bin/activate
export PYTHONPATH=src
python -m pytest tests/test_tactics.py -q
python -c "from trading_crab_lib.config import load; load(); print('ok')"
```

**Last run:** 4 passed (2026-03-23, project `.venv`).

---

## Verification metadata

**Verification approach:** Goal-backward against plan `must_haves` and ROADMAP success criteria.  
**Must-haves source:** `20-v1-2-tactics-layer-01-PLAN.md` + `20-SUMMARY.md`.  
**Automated checks:** pytest + config load — green.  
**Human checks required:** 0 mandatory (optional disk checks above).

---
*Verified: 2026-03-23T18:00:00Z*
