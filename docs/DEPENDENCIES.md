# Dependency files — canonical source and forks

This document explains how **`pyproject.toml`**, **`requirements.txt`**, **`requirements-dev.txt`**, and install scripts relate. Use it when onboarding a fork or choosing between `pip install -r` and editable installs.

## Canonical definition (`pyproject.toml`)

The installable package **`trading-crab-lib`** is defined in **`pyproject.toml`**:

- **`[project]`** — `name`, `version`, `requires-python`, and **`dependencies`** (runtime: pandas, numpy, scikit-learn, FRED/scraping stack, visualization, etc.).
- **`[project.optional-dependencies]`** — extras:
  - **`dev`** — pytest, ruff, ipykernel, jupyterlab, build, twine, hdbscan (for tests that need density clustering).
  - **`data-extras`** — `pandas-datareader`, `openbb` (fallback ETF data sources).
  - **`clustering-extras`** — `hdbscan`, `kneed` (optional clustering backends).

Publishing to PyPI / installing with **`pip install trading-crab-lib`** uses this file. **Changing dependency policy starts here**; other files should stay aligned.

## `requirements.txt` vs `pyproject.toml`

**`requirements.txt`** lists **minimum version bounds** for a flat **`pip install -r requirements.txt`** workflow. Its header states that bounds match **`pyproject.toml`** and are compatible with Python 3.10+.

Treat **`requirements.txt`** as a **convenience mirror** for environments that do not use **`pip install -e`** (CI, quick venvs, or **`scripts/setup.sh`** without editable install). When you add or bump a dependency in **`[project].dependencies`**, update **`requirements.txt`** in the same change so they stay in sync.

## `requirements-dev.txt`

**`requirements-dev.txt`** starts with **`-r requirements.txt`**, then adds dev/test/notebook/packaging packages. It is aligned with **`pip install -e ".[dev]"`**: same idea (runtime + dev tooling), different mechanism (`-r` flat list vs setuptools extras).

Use either:

- **`pip install -r requirements-dev.txt`**, or  
- **`pip install -e ".[dev]"`** after **`pip install -U pip`**

for local development. Optional **`k-means-constrained`** is not in the default lists; install it separately if you want balanced KMeans (see **`scripts/setup.sh`**).

## Scripts and README paths

- **`scripts/setup.sh`** installs with **`pip install -r requirements.txt`** (default) or **`pip install -r requirements-dev.txt`** (`--dev`). It does not run **`pip install -e .`**; the package is used from the repo via **`PYTHONPATH`** / project layout as documented in **README**.
- **README** and **`docs/CURSOR.md`** recommend **`pip install -e ".[dev]"`** for developers who want the package importable from **`src/`** with extras — equivalent in intent to **`requirements-dev.txt`**.

## Optional lockfiles

For **exact** reproducibility across machines, you can generate a lockfile (e.g. **`pip-tools`**: **`pip-compile pyproject.toml --output-file requirements-lock.txt`**). The **`requirements.txt`** header mentions this pattern; committing a lockfile is optional and not required for normal development.

## Fork checklist

1. Clone the repository and **`cd`** into it.
2. Create a venv: **`python3 -m venv .venv`** and **`source .venv/bin/activate`** (Windows: **`.venv\Scripts\activate`**).
3. Install either:
   - **`bash scripts/setup.sh --dev`**, or  
   - **`pip install -U pip`** then **`pip install -e ".[dev]"`**, and optionally **`pip install k-means-constrained`**.
4. Copy **`.env.example`** to **`.env`** and set **`FRED_API_KEY`**.
5. Run tests: **`pytest`** (or **`make test`** if defined in your checkout).

For IDE interpreter selection, see **`docs/CURSOR.md`**.
