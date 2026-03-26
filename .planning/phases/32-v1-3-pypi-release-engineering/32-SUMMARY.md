# Phase 32 — Execution summary (PKG-11)

**Plan:** `32-v1-3-pypi-release-engineering-01-PLAN.md`  
**Executed:** 2026-03-26  
**Requirement:** PKG-11

## What shipped

- **`LICENSE`** — MIT (2026, trading-crab-lib contributors).
- **`pyproject.toml`** — `readme`, SPDX **`license = "MIT"`**, **`[project.urls]`** (Homepage, Repository → `https://github.com/strycker/gsd-scratch-work`), classifiers through **Python 3.14**, **`build`** / **`twine`** in **`[project.optional-dependencies].dev`**, **`pythonpath`** for pytest includes **`"."`** so `run_pipeline` resolves in pipeline tests.
- **`requirements-dev.txt`** — **`build`**, **`twine`** for file-based installs.
- **`scripts/build_dist.sh`** — `python -m build` + `twine check dist/*`.
- **`docs/RELEASING.md`** — Build, TestPyPI, PyPI, Trusted Publishing link, yanking note, name-collision note, **GitHub Actions** appendix (YAML snippet — **not** checked in; workflow optional).
- **`README.md`** — **Install from PyPI** subsection + links to **Library-only install** and **RELEASING.md**.

## Traceability

- **`.planning/REQUIREMENTS.md`** — **PKG-11** complete.
- **`.planning/ROADMAP.md`** / **`.planning/STATE.md`** — Phase **32** closed; next **33**.

## Verification

```bash
bash scripts/build_dist.sh
pytest tests/ -q
```

**PyPI / TestPyPI:** Not uploaded in this execute — maintainers follow **`docs/RELEASING.md`** when ready.

**Optional:** `RUN_WHEEL_SMOKE=1 pytest tests/integration/test_wheel_smoke.py` — not run in this session (slow, network).

**Plan 01 hybrid summary:** `32-v1-3-pypi-release-engineering-01-SUMMARY.md`
