---
phase: 32
title: PyPI release engineering — technical research
status: complete
---

# Phase 32 — RESEARCH.md

**Question:** What do we need to know to plan **PKG-11** (publishable **`trading-crab-lib`**) well?

**Requirement:** **PKG-11** — Release engineering: build, TestPyPI, PyPI, trusted publishing, README install story.

---

## Current state

- **`pyproject.toml`**: `[build-system]` uses **setuptools** + **wheel**; **`[project]`** has **`name = "trading-crab-lib"`**, **`requires-python = ">=3.10"`**, classifiers through **3.13** only; **no** `[project.urls]`, **no** `readme =`, **no** explicit **license** metadata; packages discovered under **`src/`** (`trading_crab_lib` only — pipelines/notebooks are not packaged).
- **No `LICENSE` file** at repo root (PyPI OSS expectation: add SPDX file + metadata).
- **Wheel smoke** already exists: **`tests/integration/test_wheel_smoke.py`** + **`scripts/smoke_wheel_paths.sh`** (opt-in **`RUN_WHEEL_SMOKE=1`**).
- **Phase 31** delivered **`TRADING_CRAB_*`** path resolution — README should stay aligned with “`pip install trading-crab-lib` + env” story.

---

## Build & distribution tooling

| Topic | Recommendation |
|--------|-----------------|
| **Standard build** | **`python -m build`** (PEP 517) produces **`dist/*.whl`** and **`dist/*.tar.gz`**. Add **`build`** to **`[project.optional-dependencies].dev`** (or document **`pip install build`** for maintainers). |
| **Backend** | Keep **setuptools**; no need to switch to hatchling for this phase unless maintainers prefer later. |
| **Check artifacts** | **`twine check dist/*`** before upload (catch metadata/rendering issues). |
| **TestPyPI** | **`twine upload --repository testpypi dist/*`** after **`~/.pypirc`** or env **`TWINE_USERNAME`/`TWINE_PASSWORD`** (TestPyPI token). |
| **Production PyPI** | Same with **`pypi.org`** credentials or **Trusted Publishing**. |

---

## Metadata (PEP 621)

- **`readme`**: Set **`readme = "README.md"`** (or **`{file = "README.md", content-type = "text/markdown"}`** per PEP 621 if needed for your setuptools version).
- **`license`**: Prefer **`license = { text = "MIT" }`** **or** **`license-files = ["LICENSE"]`** with a root **`LICENSE`** file (SPDX identifier in **`pyproject`** aligns with PyPI).
- **`[project.urls]`**: Typical keys: **Homepage**, **Repository**, **Documentation** (can point to README anchors or future RTD).
- **Classifiers**: Roadmap calls for **Python 3.10–3.14** — add **`Programming Language :: Python :: 3.14`** when supported on PyPI trove (verify at execute time; if trove lags, document in SUMMARY).
- **`requires-python`**: Already **`>=3.10`**; document in **RELEASING.md** that **3.14** is supported in CI/matrix when available.

---

## Trusted Publishing (optional but documented)

- **PyPI Trusted Publishers** (GitHub Actions OIDC): no long-lived PyPI password in CI; workflow **`pypi-publish`** / **`attestations`** patterns are standard.
- Phase deliverable can be **docs-only** (steps + link to PyPI docs) **or** a minimal **`.github/workflows/publish.yml`** triggered on **`release`** with **`permissions: id-token: write`** — choose one in execute based on maintainer preference.

---

## Non-goals (this phase)

- Actually **claiming** the **`trading-crab-lib`** name on PyPI if already taken (document check in RELEASING).
- Bundling **pipelines/** or **notebooks/** inside the wheel (already excluded by **`packages.find`**).

---

## Validation Architecture

Plans for **PKG-11** should be verifiable without a live PyPI upload in CI:

1. **Automated:** **`python -m build`** exits **0** and **`dist/`** contains **`trading_crab_lib-*.whl`** (or **`trading_crab_lib`** normalized name per setuptools).
2. **Automated:** **`twine check dist/*`** exits **0** after build.
3. **Automated:** **`pytest`** (existing suite) still passes; optional **`RUN_WHEEL_SMOKE=1`** remains green after metadata changes.
4. **Manual (maintainer):** One **TestPyPI** upload using **RELEASING.md** commands — recorded in **32-SUMMARY.md** as done or deferred with reason.

Dimension 8 (Nyquist): validation strategy lives in **`32-VALIDATION.md`**; execution sampling uses **`pytest -q`** + build/twine commands per wave.

---

## RESEARCH COMPLETE

Ready for **`32-*-PLAN.md`** with concrete **`pyproject.toml`** keys, **`LICENSE`** text, **`RELEASING.md`** command blocks, and **README** cross-links.
