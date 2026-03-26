# Rebuilding Trading-Crab from scratch — analysis, lessons, and a principled sequence

This document is for **future you** (or a new repository) that wants to **replicate** the Trading-Crab idea with:

- **This codebase** available as a **submodule** or read-only mirror (reference for algorithms, tests, and config shape).
- **GSD** (`get-shit-done`) for phases, milestones, requirements, and verification.
- **Cursor** (or similar) for implementation.

It records **what exists today**, **what we would do differently with proper GSD**, and a **clear, prioritized, first-principles build order** in plain English.

---

## 1. How to use this guide in a new repo

1. **Add this repository as a submodule** (or subtree), e.g. `reference/trading-crab` — **read-only** for parity checks; implement in the new repo’s `src/` so you are not fighting submodule write rules.
2. **Initialize GSD first**: `$gsd-new-project` (or equivalent) so `.planning/` has `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`, and **one milestone** with phases sized for **vertical slices** (see §5).
3. **Map each greenfield phase** to a **single measurable outcome** (artifact + test + checkpoint), not “implement everything in clustering.”
4. **Point agents** at:
   - This file for **order and invariants**.
   - Submodule **`legacy/unified_script.py`** (if present in reference) for **numeric parity** when in doubt.
   - Submodule **`ARCHITECTURE.md`** and **`CLAUDE.md`** for **non-negotiable design choices**.

---

## 2. What this system is (compressed mental model)

**Inputs:** quarterly macro series (scraped + FRED) + ETF prices.

**Core pipeline:**

1. **Ingest** → raw tables (`macro_raw`, `asset_prices`) with **checkpoints** and **publication-lag** rules where needed.
2. **Features** → engineered columns (ratios, log, gap-fill, derivatives) with a **strict order**; **two** feature artifacts: **non-causal** (clustering) vs **causal** (supervised / live).
3. **Regimes** → PCA → clustering (e.g. balanced k-means) → **human-readable labels** in config.
4. **Supervised** → current regime + forward horizons + evaluation (time-series CV).
5. **Assets** → quarterly returns, regime-conditional stats, rankings.
6. **Reporting** → dashboard + optional email + tactics/diagnostics.

**First principle:** *anything that can leak future information into the training path must be isolated in causal feature files and never mixed with clustering artifacts.*

---

## 3. What we did well (worth keeping)

| Area | Why it matters |
|------|----------------|
| **Single `settings.yaml`** | All tunables, series lists, ETF universe, and clustering knobs in one place — reproducible and diffable. |
| **CheckpointManager + parquet** | Fast iteration without re-scraping; manifest/freshness semantics; DataFrames never pickled. |
| **RunConfig** | CLI and pipeline behavior are data, not scattered globals. |
| **Dual feature outputs** | `features` vs `features_supervised` (or equivalent names) is the correct answer to centered vs causal smoothing — see `ARCHITECTURE.md` §1. |
| **Balanced regimes for statistics** | `balanced_cluster` as default for downstream stats when N is small. |
| **Legacy monolith as ground truth** | `legacy/unified_script.py` as a parity anchor when refactoring. |
| **Tests + Nyquist-style verification** | `tests/` plus planning `*-VERIFICATION.md` close the loop between “claimed” and “proven.” |

---

## 4. What we would do differently (GSD + structure)

These are **process and sequencing** lessons, not regrets about the math.

### 4.1 Milestones and phases

- **Milestone = shippable story**, e.g. “Ingest + checkpoints,” then “Features + invariants,” then “Regimes,” not “all of ML.”
- **Phase size:** each phase should end with **one** primary artifact (e.g. `features_causal.parquet` contract) and **automated proof** (pytest + smoke script).
- **Order:** establish **data contracts** and **causal/non-causal split** *before* clustering and *long before* portfolio polish.
- **Planning files:** every phase should have a **PLAN** and **SUMMARY** when closed (GSD `stats` completeness) — retroactive catch-up is painful.

### 4.2 Naming and boundaries

- **One import path** for the library package (`trading_crab_lib` in this repo); avoid long-lived duplicate names (`market_regime` vs `trading_crab_lib`) across docs and tests.
- **Keep `pipelines/`** as thin orchestrators; **keep `src/`** as the library — same split in the new repo.

### 4.3 Optional complexity

- **Clustering investigation** (GMM, DBSCAN, spectral, etc.) is valuable but should be **Phase “3b”** or a **research milestone**, not blocking the first end-to-end “regimes + labels + dashboard” path.

---

## 5. Recommended milestone map (greenfield)

Use this as a **ROADMAP skeleton** (adjust names to your GSD conventions).

| Milestone | Intent | Exit criteria (examples) |
|-----------|--------|---------------------------|
| **M0 — Foundations** | Repo, package, config load, logging, `RunConfig`, CI (`pytest`). | `python -c "from trading_crab_lib.config import load"` works; `pytest` green on stubs. |
| **M1 — Data plane** | Ingestion + checkpoints + publication lag + ETF universe constraints. | `macro_raw` / `asset_prices` parquet; refresh/recompute flags; tests with mocks. |
| **M2 — Feature plane** | Full `engineer_all` order; **dual** outputs; gap-fill + derivatives. | Two parquet artifacts; tests that assert **no accidental mixing**; causal vs non-causal documented in `ARCHITECTURE.md` equivalent. |
| **M3 — Regimes** | PCA + primary clustering + balanced assignment + labels file. | `cluster_labels.parquet` + `regime_labels.yaml`; plots optional. |
| **M4 — Supervised** | Current regime + forward models + honest metrics (time-series CV). | Saved models; metrics files; no look-ahead on features. |
| **M5 — Assets & portfolio** | Returns, regime-conditional stats, rankings, simple portfolio helpers. | Report tables reproducible from checkpoints. |
| **M6 — Product shell** | Dashboard, weekly report, email/SMTP, tactics/diagnostics — **last**. | One command run; human-readable output. |

This order matches **dependency reality** and **risk**: get **correct data + features** before **pretty reporting**.

---

## 6. Step-by-step rebuild sequence (prioritized)

Follow **in order**. Skip steps only if you are explicitly building a **research-only** fork.

### Phase A — Project skeleton

1. **Create** `pyproject.toml` (src layout), `README.md`, `pyproject`/`pytest` config.
2. **Define** `config/settings.yaml` **shape** early (even with placeholder lists): `data`, `fred`, `multpl`, `features`, `clustering`, `prediction`, `assets`.
3. **Add** `RunConfig` (or equivalent) and a **single CLI entrypoint** (`run_pipeline.py`) that delegates to numbered steps.
4. **Add** `CheckpointManager`: parquet for DataFrames, pickle for sklearn; **manifest** optional but recommended.

**Proof:** import + `pytest` with no network.

### Phase B — Ingestion

5. **FRED** client with per-series **shift** (GDP/GNP-style publication lag).
6. **Multpl** scraper driven **only** from YAML URLs (no hardcoded URLs in Python).
7. **ETF prices** (yfinance or your fallback chain) with quarterly resampling.
8. **Wire** Step 01 pipeline; **checkpoint** `macro_raw` and `asset_prices`.

**Proof:** run with cached data; tests mock HTTP.

### Phase C — Feature engineering (the heart)

9. **Cross-ratios** → **log** → **subset** → **Bernstein gap-fill** → **derivatives** → **subset** — **never reorder** without re-architecting.
10. **Emit two parquet artifacts** for non-causal vs causal smoothing; **identical column names**; different keys in checkpoint manager.
11. **Document** invariants in an `ARCHITECTURE.md` equivalent **immediately**.

**Proof:** unit tests on small synthetic series; property tests for “causal uses only past” if feasible.

### Phase D — Regimes

12. **PCA** (fixed component count — document why).
13. **K-sweep** + **primary** `balanced_cluster` (or your chosen constraint) for downstream labeling.
14. **Persist** labels + cluster assignments; **pin** `regime_labels.yaml`.

**Proof:** silhouette / CH metrics in logs; reproducibility across runs with fixed config.

### Phase E — Supervised

15. **Train** current-regime classifier on **causal** features only.
16. **Train** forward models (horizons from config) with **TimeSeriesSplit** (or equivalent).
17. **Save** models + metrics; **no** training on non-causal file.

**Proof:** metrics file + confusion matrix / reports as you prefer.

### Phase F — Assets and reporting

18. **Quarterly returns** from prices; join to regimes.
19. **Rank** ETFs / templates by regime; **portfolio** helpers last.
20. **Dashboard CSV** + optional **email** + **tactics** once the core is stable.

**Proof:** end-to-end script from checkpoints → report; smoke test in CI.

---

## 7. Contracts checklist (do not break silently)

Before declaring a milestone “done,” confirm:

- [ ] **GDP/GNP** (and any other lagged series) use **publication-lag** rules from config.
- [ ] **Gap-fill runs in log space** after log transform; **not** before.
- [ ] **Clustering** uses **non-causal** (centered) features; **supervised** uses **causal** only.
- [ ] **PCA component count** is fixed and documented when changing.
- [ ] **Regime labels** are pinned in YAML; **no** silent relabel on cluster id drift.
- [ ] **ETF-only** and **non-intraday** constraints are enforced in code or tests, not only in prose.

---

## 8. How to record “what we already did” vs “greenfield plan”

In the **new** repo’s `.planning/`:

| Artifact | Purpose |
|----------|---------|
| `PROJECT.md` | Outcomes and scope (copy/adapt from this repo’s `PROJECT.md`). |
| `REQUIREMENTS.md` | Stable IDs (`DATA-01`, `REGIME-01`, …) — **fewer, sharper** than a dump of every wish. |
| `ROADMAP.md` | Milestones **M0–M6** with **phase headings** GSD can parse; avoid accidental `## Phase N:` collisions if your tool filters by them (see this repo’s ROADMAP lessons). |
| `STATE.md` | Optional `progress` YAML synced to `$gsd:stats` when you care about parity. |
| `milestones/vX-*.md` | Archives when you ship. |

**This repository** remains the **reference implementation**: diff against it when unsure, but **do not** treat scratch-work phase numbers as the ideal sequence.

---

## 9. Submodule workflow (practical)

- **Submodule path:** e.g. `external/trading-crab-reference`.
- **Update** with `git submodule update --remote` when you want parity checks.
- **CI** in the new repo: optional job that runs **reference tests** or **compares** a small golden parquet hash (only if you invest in golden files).
- **Never** require submodule writes for **your** daily workflow.

---

## 10. One-page “order of operations” (printable)

1. Config + package + checkpoints + CLI.  
2. Ingest macro + ETF + lag rules.  
3. Features with **dual** outputs + **documented** order.  
4. PCA + clustering + labels.  
5. Supervised models on **causal** features.  
6. **Assets** + **portfolio** + **dashboard**.  
7. **Email / tactics / polish** — **after** the pipeline is honest.

---

## 11. Key files in *this* repository to open first

| File | Use |
|------|-----|
| `CLAUDE.md` | Project map, conventions, run commands. |
| `ARCHITECTURE.md` | Invariants (dual features, PCA, gap-fill, checkpoints). |
| `RUNBOOK.md` | Operational golden path. |
| `config/settings.yaml` | Tunable surface. |
| `run_pipeline.py` | CLI wiring. |
| `pipelines/*.py` | Step orchestration. |
| `src/trading_crab_lib/` | Library implementation. |
| `tests/` | What “done” looks like. |

---

*This guide is descriptive, not a promise to re-implement every roadmap item. Update it when you change the canonical pipeline or GSD conventions.*
