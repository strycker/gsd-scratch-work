---
phase: 17-v1-2-expanded-macro-signals
verified: 2026-03-21T12:00:00Z
status: human_needed
score: 5/5 plan must-haves (code); roadmap success 2/3 auto-verified
---

# Phase 17: v1.2 expanded macro & yield data — Verification Report

**Phase goal (ROADMAP):** Extend FRED ingest and feature engineering with additional series and yield-curve / spread features, preserving publication-lag rules and causal variants.

**Requirement:** DATA-10

**Verified:** 2026-03-21

**Overall status:** `human_needed` — all **plan must-haves** are satisfied in the codebase and tests pass; **one roadmap success criterion** (live step-1 ingest with API) and optional **manual smoke** remain for a human with `FRED_API_KEY` and network.

---

## Goal achievement

### Observable truths (from `17-v1-2-expanded-macro-signals-01-PLAN.md` must_haves)

| # | Truth | Status | Evidence |
|---|--------|--------|----------|
| 1 | Every `fred.series` entry ingests when the API key is present (failures logged; pipeline does not crash). | ✓ VERIFIED (code) | `src/trading_crab_lib/ingestion/fred.py` `fetch_all`: per-series `try`/`except`, `log.warning` on failure, series omitted from frame — no uncaught exception. **End-to-end pull of every ID** not run in this verification (no API call). |
| 2 | `yc_*` from `add_yield_curve_features` are in `features.initial_features` and receive derivatives per conventions. | ✓ VERIFIED | `config/settings.yaml`: `yc_10y_2y`, `yc_10y_3m`, `yc_2y_3m` in `initial_features`; `*_d1`/`*_d2` in `clustering_features`. `transforms.engineer_all` runs `add_yield_curve_features` before selection. |
| 3 | `features.clustering_features` includes new macro inputs per `17-CONTEXT.md` (or documented waiver). | ✓ VERIFIED | `17-CONTEXT.md` table + redundancy rule (`yc_*` not `fred_t10y2y`/`fred_t10y3m` in features). YAML matches: `log_fred_*`, `fred_gs2`, `yc_*` derivatives present. |
| 4 | Causal and non-causal builds see the same columns at `engineer_all` call sites (step 2 dual outputs). | ✓ VERIFIED | `run_pipeline.py` `step2_features`: `engineer_all(..., causal=False)` → `features.parquet`; `engineer_all(..., causal=True)` → `features_supervised.parquet`; comment documents contract. `tests/unit/test_transforms.py::TestEngineerAllExpandedMacro::test_engineer_all_causal_mode_same_columns` asserts identical column names. |
| 5 | Changing `clustering_features` triggers documented post-recluster path (RUNBOOK + `regime_labels`). | ✓ VERIFIED | `RUNBOOK.md` §Checkpoint hygiene: bullet **FRED / macro expansion** ties `fred.series` / `features.*` changes to `--recompute`, steps **3–7**, and `config/regime_labels.yaml`. |

**Truths score:** 5/5 at code/test level.

### Required artifacts (plan frontmatter)

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `config/settings.yaml` | FRED + coherent `features.*` | ✓ | `fred.series` includes Phase 8 IDs; `log_columns` / `initial_features` / `clustering_features` extended; comments on T10Y2Y/T10Y3M vs `yc_*`. |
| `src/trading_crab_lib/transforms.py` | `add_yield_curve_features` | ✓ | Present; `engineer_all` invokes it after cross-ratios. No Phase-17 edit required for goal. |
| `tests/unit/test_transforms.py` | Synthetic `engineer_all` coverage | ✓ | `TestAddYieldCurveFeatures`, `TestEngineerAllExpandedMacro`. |
| `tests/unit/test_fred_config.py` (plan name) | Config guards | ✓ **alias** | Implemented as `tests/unit/test_fred_series_config.py` (`test_fred_t10y_spreads_not_in_clustering_features`, phase-8 series keys). |
| `pipelines/01_ingest.py` / `run_pipeline.py` (plan `files_modified`) | — | ℹ️ Drift | Phase 17 did **not** change `01_ingest.py`. `run_pipeline.py` already had dual `engineer_all` before this phase — no gap for DATA-10 wiring. |

**Artifacts:** All required behaviors present; only **plan manifest** naming/path drift vs actual repo layout.

### Key wiring (manual; `gsd-tools verify key-links` N/A — no `key_links` in plan frontmatter)

| From | To | Via | Status |
|------|----|-----|--------|
| `settings.yaml` `features.*` | `engineer_all` | `load()` → `step2_features` | ✓ WIRED |
| Raw macro parquet | Centered + causal feature parquets | `run_pipeline.step2_features` | ✓ WIRED |

---

## ROADMAP success criteria (`.planning/ROADMAP.md`)

| # | Criterion | Auto-verified? |
|---|-----------|----------------|
| 1 | New series in `settings.yaml` ingest in step 1 when API available. | ✗ Needs human (live FRED + step 1). Code path verified only. |
| 2 | Derived spreads/features documented and produced in causal + non-causal artifacts. | ✓ `17-CONTEXT`, dual parquet in `step2_features`, unit tests. |
| 3 | Tests or smoke paths cover new columns without breaking clustering defaults. | ✓ Unit tests + config guard; full pipeline re-cluster not run here. |

---

## Requirements coverage (`.planning/REQUIREMENTS.md`)

| Requirement | Status |
|-------------|--------|
| **DATA-10** (Phase 17) | ✓ SATISFIED — checkbox and traceability row **Complete**; implementation references `config/settings.yaml` and `17-CONTEXT.md`. |

---

## Anti-patterns (files touched in `17-SUMMARY.md`)

Scanned `config/settings.yaml`, `RUNBOOK.md`, `tests/unit/test_transforms.py`, `tests/unit/test_fred_series_config.py`, `17-CONTEXT.md`: no `TODO`/`FIXME`, no placeholder copy, no empty stubs in scope.

---

## Human verification required

1. **Live FRED ingest (roadmap success #1)**  
   **Test:** With `FRED_API_KEY` set, run `python run_pipeline.py --refresh --steps 1` (or full 1–2) and confirm `data/raw/macro_raw.parquet` (or logs) shows expected `fred_*` columns without fatal errors.  
   **Expected:** Each configured series either present or logged as failed; pipeline completes.  
   **Why human:** Requires network and secrets; not executed in CI for this report.

2. **Optional — features materialization**  
   **Test:** `python run_pipeline.py --recompute --steps 2` after fresh raw data; inspect `data/processed/features.parquet` columns for new `log_fred_*` / `yc_*` derivatives.  
   **Expected:** New columns present when upstream raw columns exist.  
   **Why human:** Depends on local data cache and API availability.

---

## Gaps summary

**No code gaps** relative to DATA-10 and plan must-haves.

**Non-blocking notes:**

- Plan frontmatter listed `test_fred_config.py` and `pipelines/01_ingest.py`; repo uses `test_fred_series_config.py` and did not require ingest edits for this phase.
- `gsd-tools verify artifacts` / `verify key-links` returned errors (frontmatter uses nested `must_haves.artifacts` — tool expects a different shape). Verification was done manually.

---

## Recommended fix plans

None for goal closure. Optional follow-ups:

- Align plan `files_modified` / test filename with repo reality in a docs-only edit (cosmetic).
- Add a mocked `fredapi` test for `fetch_all` series enumeration (deferred in `17-SUMMARY.md`).

---

## Automated verification commands (re-run)

```bash
. .venv/bin/activate
PYTHONPATH=src python -c "from trading_crab_lib.config import load; load(); print('ok', len(load()['features']['clustering_features']), 'clustering features')"
PYTHONPATH=src python -m pytest tests/unit/test_transforms.py tests/unit/test_fred_series_config.py tests/unit/test_regime.py -q
```

**Last run:** 32 passed (transforms + fred config + regime).
