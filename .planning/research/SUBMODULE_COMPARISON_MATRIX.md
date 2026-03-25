# Submodule comparison matrix (v1.3 — SYNC-10)

**Generated:** 2026-03-25 (Phase 29 execute)  
**Canonical workspace:** `gsd-scratch-work` (this repo root)

## Operational constraint

These three directories are **read-only** mirrors for comparison: **`trading-crab-lib-repo-copy`**, **`claude-scratch-work-repo-copy`**, **`trading-crab-repo-copy`**. **Do not edit** files inside them or push submodule commits as part of v1.3 work. You may **`git submodule update --init --recursive`** to refresh checkouts only.

## Repository inventory

| | **Root (canonical)** | **trading-crab-lib-repo-copy** | **claude-scratch-work-repo-copy** | **trading-crab-repo-copy** |
|---|:---:|:---:|:---:|:---:|
| **Has `src/`** | Yes | Yes | Yes | No |
| **Package dir under `src/`** | `trading_crab_lib` | `trading_crab_lib` | `trading_crab_lib` | — |
| **`pyproject.toml` `[project].name`** | `trading-crab-lib` | `trading-crab-lib` | `trading-crab-lib` | (none) |
| **Approx `*.py` count (repo tree)** | 101 (excl. three mirror dirs) | 218 (includes nested clones; see caveats) | 86 | 0 |
| **Approx `*.py` under `src/trading_crab_lib/` only** | 29 | 24 | 30 | — |
| **`run_pipeline.py`** | Yes | Yes | Yes | No |
| **`config/settings.yaml`** | Yes | Yes | Yes | No |
| **`pipelines/`** | Yes (multi-step) | Yes | Yes | No |
| **`.planning/`** | Yes (GSD) | No (at submodule root) | No (at submodule root) | No |

## Layout caveats

- **`trading-crab-lib-repo-copy`** contains **nested** paths such as `gsd-scratch-work-repo-copy/` and `claude-scratch-work-repo-copy/` — treat as historical **nested checkout noise**; do not use nested trees as the primary comparison column without stating the path.
- **Root `find .` counts** must **exclude** the three mirror path prefixes or `.py` totals **inflate** (submodules are inside the worktree).

## Module areas

Legend: **P** = Present (observed in tree), **A** = Absent in that tree, **U** = Unknown / not audited file-by-file.

| Area | Root | trading-crab-lib-repo-copy | claude-scratch-work-repo-copy | trading-crab-repo-copy |
|------|:---:|:---:|:---:|:---:|
| **Ingestion** (`ingestion/`) | P | P | P | A |
| **Features / transforms** | P (`transforms.py`) | P | P (+ `divergence.py`, `momentum.py` in claude mirror) | A |
| **Clustering / regime** | P (`clustering.py`, `regime.py`, `gmm`, `density`, `spectral`, …) | P | P (+ `hmm.py`, `markov.py` in claude mirror) | A |
| **Prediction** | P (`prediction/`, `prediction.py`) | P (`prediction/ bundle-oriented`) | P | A |
| **Reporting / diagnostics / tactics** | P (`reporting.py`, `diagnostics.py`, `tactics.py`, `email.py`) | P | P | A |
| **Assets / returns** | P (`asset_returns.py`, `ingestion/assets`) | P | P | A |
| **Dashboard / weekly wiring** | P (`prediction/dashboard_model.py`, step-order in `run_pipeline.py`) | U | U | A |

## Tests

| | **Root** | **trading-crab-lib-repo-copy** | **claude-scratch-work-repo-copy** | **trading-crab-repo-copy** |
|---|----------|----------------------------------|-----------------------------------|----------------------------|
| **`tests/` present** | Yes | Yes | Yes | No |
| **Approx `tests/**/*.py` files** | 41 | 23 | 42 | 0 |
| **Notes** | Suite tied to v1.2+ features (diagnostics, tactics, step order, etc.) | Smaller mirror suite | Larger mirror suite per directory | No Python tests — notebook-era layout |

## Config and entrypoints

| | **Root** | **LIB mirror** | **claude mirror** | **trading-crab-repo-copy** |
|---|----------|----------------|-------------------|----------------------------|
| **`config/`** | Yes | Yes | Yes | No |
| **`run_pipeline.py`** | Yes | Yes | Yes | No |
| **`pipelines/`** | Yes | Yes | Yes | No |
| **`scripts/README.md` / setup** | Yes | U | Yes (per mirror README layout) | No |

## Planning and docs

| | **Root** | **LIB mirror** | **claude mirror** | **trading-crab-repo-copy** |
|---|----------|----------------|-------------------|----------------------------|
| **`.planning/` (GSD)** | Yes | Not at submodule root | Not at submodule root | No |
| **`README.md`** | Yes | Yes | Yes | Yes |
| **`CLAUDE.md`** | Yes (workspace) | U | Yes (large single-file guide in mirror) | No (see mirror README) |

## Merge order (locked for Phase 30+)

1. **`trading-crab-lib-repo-copy`** first — closest **library-only** sibling to **`src/trading_crab_lib`**; lowest risk to diff APIs and tests before app-layer noise.
2. **`claude-scratch-work-repo-copy`** second — often holds **experimental** modules (e.g. HMM/Markov/divergence/momentum); merge only after lib parity to avoid dragging experiments before core package stability.
3. **`trading-crab-repo-copy`** last — **no `src/` Python package** in this checkout (notebooks/data focus); compare for **docs/notebook** ideas and historical steps, not primary code port.

## Notable deltas and follow-ups

- **Canonical root** is the **integration** target: step **8/9** diagnostics & tactics, **`dashboard_model`**, **`resolve_pipeline_step_order`**, and **41** root test files vs leaner **LIB** package mirror.
- **claude-scratch-work-repo-copy** **package tree** includes **extra** top-level modules (**`hmm.py`**, **`markov.py`**, **`divergence.py`**, **`momentum.py`**) **not** present under canonical **`src/trading_crab_lib/`** in this worktree — Phase **30** should decide **port vs defer** per stakeholder.
- **trading-crab-repo-copy** is **not** a Python library checkout here — **Phase 30** treats it as **artifact/notebook** reference unless refreshed to a commit that restores `src/`.
- **Nested clones** under **LIB** mirror complicate line counts — Phase **30** blueprint should prefer **path-normalized** diffs (canonical paths only).
- **`git submodule status` (2026-03-25):** `claude-scratch-work-repo-copy` @ `300cb9b…`, `trading-crab-lib-repo-copy` @ `addc74f…`, `trading-crab-repo-copy` @ `5774906…`.
