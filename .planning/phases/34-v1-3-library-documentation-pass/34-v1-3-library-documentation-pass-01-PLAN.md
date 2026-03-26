---
phase: 34
slug: v1-3-library-documentation-pass
plan: 01
status: ready
---

# Plan 01 — Library documentation & rationale (DOCS-10)

**Goal:** Google-style **module + public API** docstrings and **file-level “why”** across **`src/trading_crab_lib/`**, with **major-block rationale** only where it helps — no redundant “what” comments.

**Depends on:** Phase **33** complete (prune); else document waiver in **SUMMARY**.

---

## Wave 1 — Package root & I/O

| # | Task | Files | Done |
|---|------|-------|------|
| 1.1 | Expand **module** docstrings + public **`load`/`setup_logging`** docs | `config.py` | [ ] |
| 1.2 | Ensure **`__init__.py`** documents package surface (exports, `ROOT`, dirs) | `__init__.py` | [ ] |
| 1.3 | **`runtime.py`**: `RunConfig` + factory docstrings | `runtime.py` | [ ] |
| 1.4 | **`checkpoints.py`**: module “why” + `CheckpointManager` public methods | `checkpoints.py` | [ ] |

**Verify:** `pytest tests/ -q`; `python -m compileall -q src/trading_crab_lib`

---

## Wave 2 — Features & clustering

| # | Task | Files | Done |
|---|------|-------|------|
| 2.1 | Pipeline-order **why** + key public funcs (`engineer_all`, etc.) | `transforms.py` | [ ] |
| 2.2 | PCA/KMeans/sweep helpers | `clustering.py` | [ ] |
| 2.3 | GMM / density / spectral / comparison | `gmm.py`, `density.py`, `spectral.py`, `cluster_comparison.py` | [ ] |

**Verify:** same as Wave 1

---

## Wave 3 — Regime, assets, reporting, misc

| # | Task | Files | Done |
|---|------|-------|------|
| 3.1 | Regime profiling / transitions | `regime.py` | [ ] |
| 3.2 | Returns + proxy fallback | `asset_returns.py` | [ ] |
| 3.3 | Dashboard / reporting entrypoints | `reporting.py` | [ ] |
| 3.4 | Plot helpers (reference `RunConfig`) | `plotting.py` | [ ] |
| 3.5 | Diagnostics, tactics, top-level `prediction.py`, email | `diagnostics.py`, `tactics.py`, `prediction.py`, `email.py` | [ ] |

**Verify:** same

---

## Wave 4 — `ingestion/` & `prediction/`

| # | Task | Files | Done |
|---|------|-------|------|
| 4.1 | FRED/multpl/assets/macro_partial/grok + `ingestion/__init__` | `ingestion/*.py` | [ ] |
| 4.2 | **Spot-check roadmap:** **`classifier`** module docstring + key train/predict APIs | `prediction/classifier.py` | [ ] |
| 4.3 | Feature gating, dashboard model, metrics artifacts, `prediction/__init__` | `prediction/feature_gating.py`, `prediction/dashboard_model.py`, `prediction/model_metrics_artifacts.py`, `prediction/__init__.py` | [ ] |

**Note:** **`paths.py`** already has strong rationale — **light pass** (ensure public helpers documented).

**Verify:** same

---

## Wave 5 — Closure

| # | Task | Done |
|---|------|------|
| 5.1 | **`34-SUMMARY.md`**: **coverage table** — every **`src/trading_crab_lib/**/*.py`** → **edited** or **waived** + one-line reason | [ ] |
| 5.2 | **`REQUIREMENTS.md`**: mark **DOCS-10** **Complete** | [ ] |
| 5.3 | **`34-VERIFICATION.md`**: checklist + test log snippet | [ ] |

---

## Success criteria (roadmap)

1. Coverage checklist in **`*-SUMMARY.md`** — every **`.py`** touched or waived.
2. **`pytest`** + **`compileall`** green (and **`ruff`** only if project already uses it).
3. Spot-check: **`config`**, **`checkpoints`**, **`transforms`**, **`prediction/classifier`** have expanded module docstrings (called out in SUMMARY).
4. **DOCS-10** → **Complete** in **REQUIREMENTS.md**.

---

## Risks

| Risk | Mitigation |
|------|------------|
| Doc-only edit breaks string/escape | Run **compileall**; avoid unclosed `"""` in examples |
| Scope creep | No refactors; docstrings + brief comments only |
