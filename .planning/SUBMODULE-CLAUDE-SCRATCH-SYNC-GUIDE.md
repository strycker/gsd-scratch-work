# Aligning this repo with `claude-scratch-work-repo-copy` — analysis & porting plan

**Submodule path (this workspace):** `claude-scratch-work-repo-copy/`  
**Upstream remote (per `.gitmodules`):** `https://github.com/strycker/claude-scratch-work`  

**Hard rule:** Do **not** commit changes **inside** the submodule. Treat it as a **read-only reference fork**. All enhancements land in **this repository** (`gsd-scratch-work` / Trading-Crab main tree) via deliberate ports.

**Purpose of this document:** Summarize what differs between the two trees, **prioritize** what to pull in, and give **step-by-step** instructions for synchronization without losing work that exists **only** here (PyPI path resolution, GSD planning, etc.).

---

## Table of contents

1. [How the two codebases relate](#1-how-the-two-codebases-relate)
2. [Summary comparison](#2-summary-comparison)
3. [What the submodule has that this repo lacks (gaps)](#3-what-the-submodule-has-that-this-repo-lacks-gaps)
4. [What this repo has that the submodule may lack or diverge on](#4-what-this-repo-has-that-the-submodule-may-lack-or-diverge-on)
5. [Critical technical fork: `transforms.py`](#5-critical-technical-fork-transformspy)
6. [Prioritized porting backlog](#6-prioritized-porting-backlog)
7. [Step-by-step synchronization procedure](#7-step-by-step-synchronization-procedure)
8. [Per-item porting notes (tests, risks, merge tips)](#8-per-item-porting-notes-tests-risks-merge-tips)
9. [Documentation to merge or mirror](#9-documentation-to-merge-or-mirror)
10. [Critique & sanity checks](#10-critique--sanity-checks)
11. [Appendix — file-level inventory](#appendix--file-level-inventory)

---

## 1. How the two codebases relate

- **`claude-scratch-work-repo-copy`** is an **alternate evolution** of the same Trading-Crab idea: same broad layout (`src/trading_crab_lib`, `pipelines/`, `run_pipeline.py`), but it invested heavily in **pipeline monitoring**, **expanded plotting**, **notebook diagnostics**, **macrotrends ingestion**, **HMM**, **momentum/divergence/markov** feature modules, and a **single mega-`CLAUDE.md`** (no separate `ARCHITECTURE.md` in that tree).
- **This repo (`gsd-scratch-work`)** is the **primary workspace** you use with GSD: richer `.planning/`, separate `ARCHITECTURE.md` / `RUNBOOK.md`, **`paths.py`** for installable-library path resolution, and a **different `__init__.py`** contract (`LibraryPaths`, lazy submodule attrs).

Neither tree is a strict subset of the other: **both** contain ideas the other should adopt after review.

---

## 2. Summary comparison

| Dimension | This repo (`gsd-scratch-work`) | Submodule (`claude-scratch-work-repo-copy`) |
|-----------|--------------------------------|---------------------------------------------|
| **Planning / GSD** | Extensive `.planning/` phases, milestones, STATE | Root `STATE.md`, product `ROADMAP.md`; submodule **does not** drive your GSD stats here |
| **Docs split** | `CLAUDE.md` + `ARCHITECTURE.md` + `RUNBOOK.md` + … | Consolidated **`CLAUDE.md`** (~1.5k+ lines), no top-level `ARCHITECTURE.md` |
| **`__init__.py` / paths** | `paths.py` → `LibraryPaths`, `TRADING_CRAB_*` env vars | Simpler **`TC_*`** env vars on `ROOT`/`CONFIG_DIR`/…; convenience `load`/`RunConfig` lazy exports |
| **`plotting.py` size** | ~837 lines (typical) | **~2k+ lines** — many monitoring / CV / diagnostic plots |
| **`run_pipeline.py`** | Larger (~1.6k lines) — more local evolution | **~1.4k lines** — **wired to `monitoring.py`** throughout |
| **`monitoring.py`** | **Absent** | **Present** — ingestion/feature/cluster/predict/dashboard summaries, QA helpers |
| **Ingestion** | `fred`, `multpl`, `assets`, `grok`, `macro_partial` | Same core + **`ingestion/macrotrends.py`** + config **`macrotrends:`** block |
| **Feature stack** | `transforms.py` **without** submodule momentum/divergence hooks in the same form | **`momentum.py`**, **`divergence.py`**, **`markov.py`** integrated into **`engineer_all`** |
| **Regime / ML extras** | Clustering suite in-repo; no `hmm.py` | **`hmm.py`** (optional `hmmlearn`) |
| **Notebooks** | e.g. `08_diagnostics.ipynb`, `09_raw_series.ipynb` | **`09_diagnostics.ipynb`**, **`10_model_comparison.ipynb`**, different numbering vs raw-series |
| **Plans** | `MONITORING_EXPANSION_PLAN.md` **not** in root | **`MONITORING_EXPANSION_PLAN.md`** — master plan for monitoring + notebooks (phases A–E, C1–C7, D1–D10, etc.) |

**Rough line counts (indicative):** submodule `plotting.py` ≫ main; main `run_pipeline.py` ≫ submodule — **do not** assume “smaller file = less feature”; integration points differ.

---

## 3. What the submodule has that this repo lacks (gaps)

Below is **prioritized by impact** on correctness, observability, and research value.

### P0 — Observability & QA (high leverage, lower math risk)

| Item | Evidence | Why pull in |
|------|----------|-------------|
| **`monitoring.py` + `run_pipeline` / pipeline hooks** | `run_pipeline.py` imports `format_completeness_table`, `compute_feature_quality`, CV reports, `PipelineHealthSummary`, etc. | Catches bad data **before** you interpret regimes; aligns with `MONITORING_EXPANSION_PLAN.md` Phases C1–C4. |
| **Extended `plotting.py`** | Many functions named in `MONITORING_EXPANSION_PLAN.md` (scree, CV bars, calibration, RRG, etc.) | Faster diagnosis; parity with submodule notebooks. |
| **`tests/unit/test_monitoring.py`** (and related) | Present in submodule | Without tests, ports are fragile. |

### P1 — Data & long history (product + clustering geometry)

| Item | Evidence | Why pull in |
|------|----------|-------------|
| **`ingestion/macrotrends.py`** + **`config/settings.yaml` `macrotrends:`** | Documented in submodule `ROADMAP.md` Tier 1.5 | Gold/oil backfill pre-ETF era; **requires** re-run clustering if `clustering_features` change. |
| **Ingestion wiring** | `pipelines/01_ingest.py` imports macrotrends + monitoring | Must port **together** with config + tests (`test_macrotrends.py`). |

### P2 — Feature engineering (changes geometry — plan a milestone)

| Item | Evidence | Why pull in |
|------|----------|-------------|
| **`momentum.py`**, **`divergence.py`**, **`markov.py`** | `transforms.py` calls `add_momentum_features`, `add_divergence_features` (level + derivative passes) | Regime-change signals; **invalidates** existing `regime_labels.yaml` / clusters until re-benchmarked. |
| **Transforms merge** | Submodule `engineer_all` has extra steps vs main | **Highest conflict surface** — see §5. |

### P3 — Research / optional ML

| Item | Evidence | Why pull in |
|------|----------|-------------|
| **`hmm.py`** | Optional `hmmlearn` | Temporal alternative to k-means; for notebooks / comparison, not necessarily production default. |
| **Notebooks 09–10** | `09_diagnostics.ipynb`, `10_model_comparison.ipynb` | Education + method comparison; port after plotting + data paths work. |

### P4 — Product / DX (evaluate case-by-case)

| Item | Evidence | Notes |
|------|----------|--------|
| **Email env overrides (`TC_SMTP_*`, etc.)** | `MONITORING_EXPANSION_PLAN.md` Phase C5 | Compare with **this** repo’s `email.py` and `paths` — unify **one** env naming scheme (`TRADING_CRAB_*` vs `TC_*`) to avoid confusion. |
| **`test_confusion_matrix_plot.py`** | Submodule | Port if `plot_confusion_matrix` is added to main `plotting.py`. |

---

## 4. What this repo has that the submodule may lack or diverge on

**Protect these during ports:**

| Asset | Why it matters |
|-------|----------------|
| **`src/trading_crab_lib/paths.py`** + `LibraryPaths` | PyPI / installed-package layout; submodule’s `TC_*` pattern is simpler but **not** equivalent. **Do not** replace wholesale—**merge** env override *ideas* into `paths.py` if needed. |
| **`prediction/dashboard_model.py`, `feature_gating.py`, `model_metrics_artifacts.py`** (if present) | Possible main-only evolution — diff before overwriting `prediction/`. |
| **`.planning/`**, GSD phases, `REBUILD-FROM-SCRATCH-GUIDE.md` | Process value; submodule does not track this. |
| **Separate `ARCHITECTURE.md` / `RUNBOOK.md`** | Keep; optionally **lift** relevant paragraphs from submodule `CLAUDE.md` into ADRs here. |

---

## 5. Critical technical fork: `transforms.py`

**Observation:** Submodule `transforms.py` embeds **momentum** and **divergence** (twice: level-space and derivative-space) inside `engineer_all`. A grep on **this** repo’s `transforms.py` shows **no** `divergence` / `momentum` symbols—meaning the **feature manifold** differs.

**Implications:**

1. **You cannot “copy monitoring only”** and expect identical clusters—monitoring assumes a feature stack that may include extra columns in the submodule.
2. Porting **monitoring** without porting **transforms** is valid **if** monitoring functions only use columns that exist in both—or you gate new plots behind `if col in df`.
3. Porting **divergence/momentum** is a **milestone-level** change: update `settings.yaml` (`clustering_features`, `initial_features`), re-run step 2–7, re-pin `regime_labels.yaml`, update `ARCHITECTURE.md`.

**Recommendation:** Treat **P0 monitoring** as **orthogonal** to **P2 feature modules**; schedule P2 only after a dedicated design checkpoint (see §10).

---

## 6. Prioritized porting backlog

### Tier A — “Safe-ish” (mostly additive)

1. Add **`monitoring.py`** (copy from submodule, adapt imports to **this** package layout).
2. Wire **`run_pipeline.py`** and **`pipelines/01_ingest.py`**, **`02_features.py`**, … incrementally using submodule as reference **diffs** (`git diff --no-index` or manual).
3. Port **tests** for monitoring (`test_monitoring.py`).
4. Expand **`plotting.py`** with functions you actually need first (don’t merge 2k lines blindly—use `MONITORING_EXPANSION_PLAN.md` Phase A1–A5 as a menu).

### Tier B — Data (moderate risk)

5. Add **`ingestion/macrotrends.py`** + YAML + step-01 wiring + **`test_macrotrends.py`**.
6. Run full pipeline on a **branch**; compare cluster silhouettes vs baseline.

### Tier C — Feature geometry (high risk)

7. Add **`momentum.py`**, **`divergence.py`**, **`markov.py`** (if desired).
8. Merge **`transforms.py`** carefully—preserve **this** repo’s invariant **order** (ratios → log → …) per `ARCHITECTURE.md`; insert submodule steps only where they don’t violate order.
9. Full regression: `pytest`, selected legacy parity, re-cluster.

### Tier D — Research & notebooks

10. **`hmm.py`** + optional dependency.
11. Notebooks **`09_diagnostics`**, **`10_model_comparison`** — align numbering with **this** repo’s notebook scheme or rename to avoid confusion.

### Tier E — Docs & DX

12. Merge useful **email** env behavior into **this** `email.py` with **one** env prefix policy.
13. Import selected submodule **`CLAUDE.md`** sections into **`ARCHITECTURE.md`** / **`PITFALLS.md`** here—**don’t** replace your split-doc structure.

---

## 7. Step-by-step synchronization procedure

### Phase 0 — Preparation (no code moves yet)

1. **Update submodule pointer** (read-only):  
   `git submodule update --init --recursive`  
   `cd claude-scratch-work-repo-copy && git fetch && git log -1 --oneline`
2. **Snapshot baseline** in **this** repo: note current `pytest` count, run `python run_pipeline.py --steps 3 --plots` (or your smoke) on a **known** cache.
3. **Open a working branch**: e.g. `feature/port-claude-scratch-monitoring`.

### Phase 1 — Diff inventory (automated + manual)

4. **List file differences** (example):  
   `diff -qr src/trading_crab_lib claude-scratch-work-repo-copy/src/trading_crab_lib | head -100`  
   Focus on: `monitoring.py`, `plotting.py`, `transforms.py`, `ingestion/`, `run_pipeline.py`, `pipelines/`.
5. **For each candidate file**, label: **additive** / **replace** / **merge manually** / **skip**.

### Phase 2 — Port Tier A (monitoring + selective plots)

6. Copy **`monitoring.py`** into `src/trading_crab_lib/` (new file).
7. Merge **`run_pipeline.py`** monitoring imports and call sites **in small commits**—one step at a time (step 1, then 2, …).
8. Port **`test_monitoring.py`**; run `pytest tests/unit/test_monitoring.py -v`.
9. Cherry-pick **plotting** functions you need; each function + test if submodule has one.

### Phase 3 — Port Tier B (macrotrends) *optional milestone*

10. Copy **`macrotrends.py`** + tests + **`settings.yaml`** section.
11. Wire **`01_ingest`**; run ingestion with `--refresh` on a **dev** machine (network).
12. Document in **`ARCHITECTURE.md`** new series and lag rules.

### Phase 4 — Port Tier C (features) *separate milestone*

13. Freeze a **design doc** in `.planning/`: which pairs, which windows, order relative to existing steps.
14. Port **`momentum` / `divergence` / `markov`** + merge **`transforms.py`** behind a **config flag** if possible (`features.enable_divergence: false` default) for safer rollout.
15. Re-run pipeline; update **`regime_labels.yaml`** deliberately.

### Phase 5 — Verification

16. **Full `pytest`**.
17. **Smoke pipeline** per `RUNBOOK.md`.
18. Update **`STATE.md`** / GSD artifacts if you track progress.

---

## 8. Per-item porting notes (tests, risks, merge tips)

| Port target | Suggested tests | Main risks |
|-------------|-----------------|------------|
| `monitoring.py` | Submodule `test_monitoring.py` | Log spam; performance on huge DataFrames — gate verbose tables behind `RunConfig.verbose` |
| `plotting` additions | `test_plotting.py` / per-plot smoke | Filename collisions in `outputs/plots/` — keep naming convention |
| `macrotrends` | `test_macrotrends.py` + mocked HTML | Site layout change; rate limits — respect `RATE_LIMIT_SECONDS` |
| `momentum`/`divergence` | `test_evaluate_momentum.py`, `test_divergence.py`, `transforms` tests | **Cluster drift**; longer runtime in step 2 |
| `hmm` | `test_*hmm*` if any | Optional `hmmlearn` — skip in CI if heavy |
| `email` env | `test_email_weekly.py` | **Two env schemes** — unify deliberately |
| `__init__.py` | `test_init_module.py` submodule | **Do not** replace `paths.py` with submodule `TC_*` without migration guide |

---

## 9. Documentation to merge or mirror

| Source (submodule) | Destination (this repo) |
|----------------------|---------------------------|
| `MONITORING_EXPANSION_PLAN.md` | Copy to `.planning/` or `scratch/` as **reference backlog**; check off items as you port |
| `ROADMAP.md` (product) | Merge Tier 1 items into **`ROADMAP.md`** / **`CLAUDE.md` Next priority** — dedupe with existing roadmap |
| Submodule `CLAUDE.md` sections on monitoring | Extract into **`ARCHITECTURE.md`** or new **`MONITORING.md`** — avoid 1500-line single file here unless you want it |
| `STATE.md` (submodule) | **Do not overwrite** this repo’s `.planning/STATE.md` — compare only |

---

## 10. Critique & sanity checks

**Question:** Is submodule always “ahead”? **No** — this repo has GSD, `paths.py`, and possibly prediction/reporting edits the submodule never picked up.

**Question:** Should you merge submodule `run_pipeline.py` wholesale? **No** — binary-merge will **destroy** local `run_pipeline` changes; use **patch hunks** or re-apply monitoring blocks.

**Question:** Port plotting before monitoring? **Allowed** if functions are **pure** and tested—but **monitoring** delivers more operational value per line for pipeline trust.

**Question:** Submodule tests count similar file count—are we done? **No** — **assertion coverage** differs; run **coverage diff** on touched modules.

---

## Appendix — file-level inventory

### Present in submodule `src/trading_crab_lib/` but **not** in main (or significantly different)

- `monitoring.py`
- `hmm.py`
- `ingestion/macrotrends.py`
- `momentum.py`, `divergence.py`, `markov.py` (top-level; main may fold some behavior into `diagnostics.py` only)

### Present in main; verify before overwriting from submodule

- `paths.py`
- `prediction/dashboard_model.py`, `feature_gating.py`, `model_metrics_artifacts.py` (if they exist)
- `tactics.py`, `regime.py`, `reporting.py` — **diff** against submodule versions

### Canonical reference docs in **this** repo (keep authoritative)

- `ARCHITECTURE.md`, `RUNBOOK.md`, `CLAUDE.md` (root), `.planning/REBUILD-FROM-SCRATCH-GUIDE.md`

---

*Maintainers: when either tree changes significantly, refresh the diff summary in §2–§3 and the appendix. Submodule path name: `claude-scratch-work-repo-copy`.*
