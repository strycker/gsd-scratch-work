---
phase: 18-v1-2-signal-diagnostics
verified: 2026-03-21T14:00:00Z
status: human_needed
score: 5/5 plan must-haves (code + tests); roadmap 3/3 criteria mapped
---

# Phase 18: Signal & diagnostic layer — Verification Report

**Phase goal (ROADMAP):** Prominent ratio/trigger diagnostics and RS/RRG-style tables vs benchmarks.

**Requirements:** SIGNAL-10, SIGNAL-11

**Verified:** 2026-03-21

**Overall status:** `human_needed` — all **plan must-haves** are verified in code and automated tests; **optional human** confirmation for a full **`run_pipeline.py --steps 6,8 --plots`** run with real `asset_prices.parquet` (network/cache-dependent step 6).

---

## Goal achievement

### Observable truths (plan `must_haves`)

| # | Truth | Status | Evidence |
|---|--------|--------|----------|
| 1 | Config-driven ratios → stable parquet under `outputs/reports/diagnostics/` including trigger columns from rules. | ✓ VERIFIED | `config/settings.yaml` `diagnostics.ratios` + `trigger_defaults`; `compute_ratios_diagnostics()` writes `trigger` / `trigger_detail`; `tests/unit/test_diagnostics_ratios.py`. |
| 2 | RRG RS outputs machine-readable per benchmark; ETFs vs benchmark in prices. | ✓ VERIFIED | `rrg_for_benchmark(..., lookback=cfg)`; `run_pipeline.step8_diagnostics` concatenates `rrg_current.parquet`; `tests/unit/test_diagnostics_rrg.py`. |
| 3 | `weekly_report.md` includes **Diagnostics** when parquets exist and `weekly_report_include` is true; no crash if missing. | ✓ VERIFIED | `_append_diagnostics_section` in `reporting.py`; `test_weekly_report_diagnostics.py` (include + skip when disabled); malformed parquet caught. |
| 4 | Step 8 saves ratio + RRG plot categories when `save_plots` / `generate_plots`. | ✓ VERIFIED | `plot_diagnostics_ratios_summary`, `plot_diagnostics_rrg` → `08_diagnostics_*.png`; tests patch `PLOT_DIR` and assert PNG exists. |
| 5 | `notebooks/08_diagnostics.ipynb` documents loading parquets + plot paths. | ✓ VERIFIED | Notebook cells load `ratios_current.parquet` / `rrg_current.parquet` and list `08_diagnostics_*.png`. |

**Truths score:** 5/5 (automated evidence).

### Required artifacts (plan frontmatter)

| Artifact | Status | Details |
|----------|--------|---------|
| `config/settings.yaml` | ✓ | `trigger_defaults`, `weekly_report_include`, `rrg_lookback` present under `diagnostics`. |
| `src/trading_crab_lib/diagnostics.py` | ✓ | `evaluate_ratio_triggers`, `compute_ratios_diagnostics`. |
| `pipelines/08_diagnostics.py` | ✓ | Uses shared compute; calls plotting when `RunConfig(generate_plots=True)`. |
| `src/trading_crab_lib/reporting.py` | ✓ | `write_weekly_report_md(..., cfg=...)` + Diagnostics section. |
| `notebooks/08_diagnostics.ipynb` | ✓ | Present and valid. |

### Key wiring

| Link | Status |
|------|--------|
| `settings.yaml` → `compute_ratios_diagnostics` / `step8_diagnostics` | ✓ |
| `step8_diagnostics` → `plotting.plot_diagnostics_*` when `--plots` | ✓ |
| `write_weekly_report_md` + `cfg` from `run_pipeline` / `07_dashboard` | ✓ |

---

## ROADMAP success criteria (Phase 18)

| # | Criterion | Evidence |
|---|-----------|----------|
| 1 | Config-driven ratio definitions with stable parquet outputs. | `ratios_current.parquet` schema includes triggers; unit + integration-style tests. |
| 2 | At least one benchmark-relative RS/rotation artifact for the ETF universe. | `rrg_benchmarks` (e.g. SPY, VT); `rrg_current.parquet` rows per non-benchmark ETF. |
| 3 | Weekly report and/or plots reference new sections when configured. | `## Diagnostics` in markdown; PNG filenames documented in notebook + RUNBOOK. |

---

## Requirements coverage

| Requirement | Status |
|-------------|--------|
| **SIGNAL-10** | ✓ SATISFIED (REQUIREMENTS.md checkbox + traceability **Complete**). |
| **SIGNAL-11** | ✓ SATISFIED |

---

## Anti-patterns

Scanned `diagnostics.py`, `reporting.py` (diagnostics block), `plotting.py` (step 08): no `TODO`/`FIXME` blockers; diagnostics section uses broad `except` intentionally to avoid breaking weekly report.

---

## Human verification (optional)

1. **Full step 6 + 8 + plots** — With local `data/raw/asset_prices.parquet`, run `python run_pipeline.py --steps 6,8 --plots` and confirm `outputs/reports/diagnostics/*.parquet` and `outputs/plots/08_*.png` on disk.  
2. **Weekly report ordering** — Run step **7** after step **8** (or `6,8,7`) and confirm `outputs/reports/weekly_report.md` contains **## Diagnostics** when parquets exist.

---

## Gaps summary

**None** for SIGNAL-10/11 delivery vs plan must-haves.

---

## Automated commands (re-run)

```bash
. .venv/bin/activate
PYTHONPATH=src python -m pytest tests/unit/test_diagnostics_ratios.py tests/unit/test_diagnostics_rrg.py tests/unit/test_weekly_report_diagnostics.py tests/unit/test_phase12_gsd_validation.py -q
PYTHONPATH=src python -c "from trading_crab_lib.config import load; load(); print('ok')"
```

**Last run:** 16 passed (2026-03-21).
