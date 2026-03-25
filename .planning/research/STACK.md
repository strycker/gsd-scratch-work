# Stack Research — v1.3 (PyPI + OSS hardening)

**Domain:** Python scientific / quant library publication  
**Researched:** 2026-03-25  
**Confidence:** HIGH (standard PyPA practice; repo-specific caveats noted)

**Milestone inputs (locked):** Single PyPI distribution **`trading-crab-lib`**, package code **only from `src/`**, public OSS with stable API discipline over time, target **Python 3.10–3.14**, API/CLI breakage acceptable during v1.3 (early phase).

## Recommended stack (build + release)

### Core build / metadata

| Technology | Version | Purpose | Why recommended |
|------------|---------|---------|-------------------|
| `setuptools` | `>=68` (already in `pyproject.toml`) | Wheels + sdist | Already configured; wide tooling compatibility |
| `build` | current PyPI | Isolated builds | `python -m build` — reproducible artifacts without leaking local env |
| `twine` | current | Upload to PyPI | Standard uploader; supports **Trusted Publishing** with short-lived tokens |
| GitHub Actions | — | CI + publish | **OIDC Trusted Publishing** to PyPI (no long-lived API token in secrets) |

*Alternative:* `hatchling` is popular for greenfield; **migration not required** for v1.3 unless setuptools pain appears.

### Quality gates for OSS

| Tool | Purpose | Notes |
|------|---------|-------|
| `ruff` | Lint + format | Fast default in 2025+ ecosystem; can replace flake8/isort for new work |
| `mypy` | Static typing | Gradual; `py.typed` already declared — expand typed surface for library consumers |
| `pytest` | Tests | Already in `dev` extra; CI matrix **3.10–3.14** before release |

### Versioning

| Approach | Fit |
|---------|-----|
| **Semantic versioning** | Matches “maintain API stability” goal; pre-1.0 (`0.x`) allows breaking changes with minor bump |
| **Changelog** (`CHANGELOG.md` or GitHub Releases) | Expected for public OSS |

**Align `pyproject.toml` `version` with git tags** after first release (e.g. `v0.1.0`).

## Python 3.10–3.14

- Extend **`classifiers`** in `[project]` to include `3.14` when interpreters available in CI.
- Add **`requires-python = ">=3.10,<3.15"`** (or upper bound policy you decide) once 3.14 support is verified.
- CI: **`strategy.matrix.python-version`** listing at least `[3.10, 3.11, 3.12, 3.13, 3.14]` when runners support 3.14.

## PyPI packaging checklist (trading-crab-lib only)

1. **Name reservation:** Confirm **`trading-crab-lib`** available on PyPI (and TestPyPI dry run).
2. **README + docs:** Root `README.md` should describe *library install* vs *full repo clone* (pipelines/notebooks).
3. **`[project.urls]`:** `Homepage`, `Repository`, `Documentation`, `Changelog`.
4. **`LICENSE`:** File present at repo root; SPDX in `pyproject.toml` if desired.
5. **Optional dependencies:** Keep `dev`, `data-extras`, `clustering-extras` — document in README.
6. **Smoke test:** Fresh venv → `pip install dist/*.whl` → `import trading_crab_lib` → minimal API call **without** repo `config/` on disk (see ARCHITECTURE.md — **path coupling is a gap**).
7. **Trusted publishing:** Configure PyPI project + GitHub OIDC.
8. **First upload:** TestPyPI first, then PyPI.

## Installation (consumer-facing)

```text
pip install trading-crab-lib
# Optional clusters / data providers
pip install "trading-crab-lib[clustering-extras,data-extras]"
```

## What not to add (for v1.3)

- No second top-level PyPI package for the “full app”; repo-only scripts stay out of the wheel unless promoted deliberately.

## Submodule note

**Research scope:** local clones only (`*_repo-copy/`). Do not edit submodule trees in v1.3; **`git pull` / refresh** only to update mirrors for comparison.
