# Architecture Research — v1.3 (library vs monorepo)

**Researched:** 2026-03-25  
**Confidence:** HIGH for goals; MEDIUM for refactor effort until path audit completes

## Current canonical layout (root repo)

- **Library:** `src/trading_crab_lib/` — installable package (`trading-crab-lib` in `pyproject.toml`).
- **Application / research orchestration:** `run_pipeline.py`, `pipelines/`, `scripts/`, `notebooks/` — **not** part of the published wheel requirement (stakeholder: app stays repo-only).
- **Config:** `config/settings.yaml`, `config/regime_labels.yaml` at **repo root**.
- **Data / outputs:** `data/`, `outputs/` — gitignored runtime.

## Critical design tension: `ROOT`, `CONFIG_DIR`, `DATA_DIR`

`trading_crab_lib/__init__.py` defines:

```text
ROOT = Path(__file__).parent.parent.parent   # repo root
CONFIG_DIR = ROOT / "config"
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
```

**Implication:** After `pip install trading-crab-lib`, `__file__` lives under `site-packages`; `parent.parent.parent` is **not** the user’s project — `CONFIG_DIR` / `DATA_DIR` point into **site-packages** or invalid paths.

**v1.3 architectural recommendation:**

1. **Separate “installed library” from “repo checkout”.**
   - Public APIs should accept **`config_path: Path | None`** and **`data_dir: Path | None`** (or a small **`LibraryPaths` / `Workspace`** dataclass) with defaults:
     - If running from **editable install** in repo: preserve today’s behavior OR detect repo root via marker file.
     - If **site-packages**: require explicit paths or env vars (e.g. `TRADING_CRAB_CONFIG`, `TRADING_CRAB_DATA`).
2. **Document** the two modes in README and package docstring.
3. **Tests:** Add matrix for “editable / simulated installed” path resolution.

This is **blocking quality** for PyPI consumers; stack rank with other v1.3 work in REQUIREMENTS.md.

## Submodule integration architecture (read-only)

- Treat mirrors as **specification + test artifact** sources.
- For each unification batch:
  1. Diff module-by-module.
  2. Choose implementation (stakeholder sign-off).
  3. Port missing tests into root `tests/`.
  4. Delete duplicate root docs only (never delete inside mirrors).

## Suggested build order inside v1.3 (technical, not roadmap phases)

1. **Path / workspace API** — unblocks honest PyPI story.
2. **Public API surface audit** — `__all__`, lazy imports in `__getattr__`, hide internals.
3. **Submodule parity passes** in stakeholder order (lib → claude-scratch → trading-crab).
4. **Commentary pass** — file-level “why” + major blocks (Google-style docstrings + short rationale comments).

## Pruning boundaries

| Safe to prune (root only) | Do not prune |
|---------------------------|--------------|
| Redundant notebooks, scratch dirs, duplicate markdown | `legacy/` |
| Stale docs superseded by RUNBOOK/ARCHITECTURE | `*_repo-copy/` contents |

## Planning / GSD

- **ROADMAP** continues phase numbering after **27** (v1.2).
- Research outputs feed **REQUIREMENTS.md** REQ-IDs; traceability links plans to code modules.
