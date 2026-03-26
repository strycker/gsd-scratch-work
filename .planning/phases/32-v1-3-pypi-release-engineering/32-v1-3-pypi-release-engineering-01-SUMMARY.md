# Plan 01 — As-built (Phase 32)

**Plan:** `32-v1-3-pypi-release-engineering-01-PLAN.md`  
**Executed:** 2026-03-26

## As-built

| Task | Outcome |
|------|---------|
| 32-01-01 | **`LICENSE`**, **`pyproject.toml`** metadata (`readme`, `license`, `urls`, 3.14 classifier). |
| 32-01-02 | **`build`/`twine`** in dev extras + **`requirements-dev.txt`**; **`scripts/build_dist.sh`**. |
| 32-01-03 | **`docs/RELEASING.md`** full checklist. |
| 32-01-04 | **`README.md`** — **Install from PyPI** + cross-links. |
| 32-01-05 | **Option B** — No **`.github/workflows/publish-pypi.yml`**; **appendix** YAML in **`docs/RELEASING.md`**. |
| 32-01-06 | **`pytest tests/ -q`** — 357 passed, 14 skipped. |

## Plan fidelity

- Matches plan: OSS metadata, **`dist/`** reproducibility via **`build_dist.sh`**, maintainer docs, README PyPI story.
- **Delta:** **`pytest`** `pythonpath` extended with **`"."`** (repo root) so **`tests/test_pipelines_ingest_features.py`** can import **`run_pipeline`**; **`license`** uses SPDX string **`"MIT"`** (not `{ text = "MIT" }`) to satisfy setuptools deprecation warning.

## Delta from plan

- None blocking.
