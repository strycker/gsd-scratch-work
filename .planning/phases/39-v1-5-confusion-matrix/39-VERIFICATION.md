---
phase: 39-v1-5-confusion-matrix
verified: 2026-03-26T12:00:00Z
status: passed
score: 3/3 must-have truths
tooling_note: gsd-tools verify artifacts/key-links skipped — PLAN frontmatter uses inline `path:` artifact list not parsed as structured `must_haves.artifacts` by current gsd-tools schema; verification performed manually below.
---

# Phase 39: Confusion matrix (TMPL-03) — Verification Report

**Phase goal:** Add a confusion matrix visualization for supervised current-regime classifiers in `plotting.py`, wire step 5 when plots are enabled, save under `outputs/plots/`, update docs and tests without network.

**Status:** **passed** — goal-backed checks satisfied.

## Goal achievement

### Observable truths (from PLAN `must_haves.truths`)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | `plot_regime_confusion_matrix` saves a PNG under `outputs/plots/` when step 5 runs with plots enabled | ✓ VERIFIED | `run_pipeline.py` `step5_predict`: inside `if run_cfg.generate_plots:`, reads `metrics_dir / "confusion_matrices.parquet"` and calls `plotting.plot_regime_confusion_matrix(...)`. `plot_regime_confusion_matrix` ends with `_save_or_show(fig, filename, run_cfg)` default `filename="05_confusion_matrix.png"` → `PLOT_DIR` = `OUTPUT_DIR / "plots"`. |
| 2 | Current-regime RF confusion derived from metrics parquet with `family=regime` and `model=rf` | ✓ VERIFIED | `model_metrics_artifacts.write_model_metrics_artifacts` appends confusion rows with `"family": "regime"`, `"model": model_name` (from `cv_scores` including `"rf"`), `"horizon": None` for current-regime loop. `plot_regime_confusion_matrix` filters `family.eq("regime")`, `model.eq(model)` default `"rf"`, `horizon.isna()`. |
| 3 | `CLAUDE.md` no longer claims confusion matrix visualization is unsupported | ✓ VERIFIED | **Legacy Alignment** lists ✓ confusion heatmap + paths; **Gap 7** closed; **Remaining Gaps** addresses legacy *text* `generate_classification_report` only, not missing heatmap. |

**Score:** 3/3 truths verified.

### Required artifacts (from PLAN frontmatter)

| Artifact | Status | Details |
|----------|--------|---------|
| `src/trading_crab_lib/plotting.py` | ✓ EXISTS + SUBSTANTIVE | `def plot_regime_confusion_matrix(...)` (~L649+): pivot, seaborn heatmap, `_save_or_show`. |
| `run_pipeline.py` | ✓ EXISTS + WIRED | `step5_predict` plot block after `write_model_metrics_artifacts` (see ~L975–980). |

**Additional shipped (from 39-01-SUMMARY):** `pipelines/05_predict.py` (`--plots`), `tests/unit/test_plot_confusion_matrix.py` — present and reviewed.

### Key wiring (manual)

| From | To | Via | Status |
|------|----|-----|--------|
| `write_model_metrics_artifacts` | `outputs/reports/model_metrics/confusion_matrices.parquet` | `conf_df.to_parquet(confusion_path)` | ✓ |
| `step5_predict` + `generate_plots` | `plot_regime_confusion_matrix` | `pd.read_parquet(cm_path)` → plot | ✓ |
| Standalone `05_predict.py --plots` | Same plot helper | After metrics write, optional YAML regime names | ✓ |

## Requirements coverage

| Requirement | Status | Notes |
|-------------|--------|-------|
| **TMPL-03** | ✓ SATISFIED | Checked in `.planning/REQUIREMENTS.md` (complete); implementation matches description. |

## Automated checks

| Check | Result |
|-------|--------|
| `pytest tests/unit/test_plot_confusion_matrix.py -q` | 1 passed |
| `ruff check` (paths from plan) | Clean (as of phase closeout) |

## Anti-patterns (targeted scan)

No `TODO` / `FIXME` / placeholder returns in the new confusion-matrix path; no blockers logged for this phase.

## Human verification

**Optional (product QA):** After a full local run with data (`python run_pipeline.py --steps 5 --plots` or `pipelines/05_predict.py --plots`), open **`outputs/plots/05_confusion_matrix.png`** and confirm the heatmap labels and counts look reasonable. This is not required for automated goal verification (PNG generation is proven by code path + `_save_or_show` when `save_plots=True`).

## Gaps summary

**None.** Phase goal achieved; TMPL-03 satisfied.

## Orchestrator return

- **status:** `passed`
- **score:** 3/3 must-have truths
- **report:** `.planning/phases/39-v1-5-confusion-matrix/39-VERIFICATION.md`
- **follow-up:** None required; optional visual QA above.
