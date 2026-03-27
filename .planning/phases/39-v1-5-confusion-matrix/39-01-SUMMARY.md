---
phase: 39-v1-5-confusion-matrix
plan: "01"
subsystem: supervised / plotting
tags: [TMPL-03, confusion-matrix, step5, model_metrics]

requires: []
provides:
  - plot_regime_confusion_matrix + step 5 wiring
  - tests/unit/test_plot_confusion_matrix.py
affects: [CLAUDE.md, ROADMAP.md, FUTURE-TODO, REQUIREMENTS]

tech-stack:
  added: []
  patterns: [tidy confusion parquet → heatmap, CV fold aggregation]

key-files:
  created:
    - tests/unit/test_plot_confusion_matrix.py
  modified:
    - src/trading_crab_lib/plotting.py
    - run_pipeline.py
    - pipelines/05_predict.py
    - CLAUDE.md
    - ROADMAP.md
    - .planning/FUTURE-TODO.md
    - .planning/REQUIREMENTS.md
    - .planning/STATE.md
    - .planning/ROADMAP.md
    - .planning/NEXT_STEPS.md

key-decisions:
  - "Heatmap uses aggregated counts across TimeSeriesSplit folds from confusion_matrices.parquet (family=regime, horizon null)."
  - "Standalone step 5 exposes --plots for confusion PNG only; full step-5 plots remain on run_pipeline.py --steps 5 --plots."

patterns-established: []

requirements-completed:
  - TMPL-03

duration: —
completed: 2026-03-26
---

# Plan summary — `39-01-PLAN.md`

**Phase:** 39 — Confusion matrix visualization (**TMPL-03**)

## As-built

- **`plot_regime_confusion_matrix()`** in **`plotting.py`**: filters tidy metrics, sums counts across folds, seaborn heatmap, **`outputs/plots/05_confusion_matrix.png`** via **`_save_or_show`**.
- **`run_pipeline.py`** `step5_predict`: after other step-5 plots, reads **`confusion_matrices.parquet`** when present; warns if missing (does not fail).
- **`pipelines/05_predict.py`**: **`--plots`** loads YAML regime names and calls the same plot helper.
- **`tests/unit/test_plot_confusion_matrix.py`**: synthetic parquet-shaped frame, **`save_plots=False`** smoke test.
- **Docs:** **`CLAUDE.md`** Gap 7 + backlog strings; root **`ROADMAP.md`** §1.7 done; **`.planning/FUTURE-TODO.md`** shipped note.

## Plan fidelity

| Task | Delivered |
|------|-----------|
| 39-01-01 — plotting + test | ✓ |
| 39-01-02 — run_pipeline + 05_predict | ✓ |
| 39-01-03 — CLAUDE / ROADMAP / FUTURE-TODO | ✓ |

## Delta from plan

- Filename **`05_confusion_matrix.png`** (matches existing **`05_*.png`** step-5 convention) rather than **`step_05_confusion_matrix.png`**.
