# Cursor / IDE setup (fresh clone)

This note is for **anyone opening a new clone** in Cursor, VS Code, or another editor: how to get the same **Python environment** the project expects for tests, lint, and optional clustering tests.

For how **`pyproject.toml`** relates to **`requirements.txt`** / **`requirements-dev.txt`** and which file is authoritative, see **[DEPENDENCIES.md](DEPENDENCIES.md)**.

## Why `.venv` is not in Git

The directory **`.venv/`** is listed in **`.gitignore`** on purpose. Virtual environments are machine-specific (paths, compiled wheels, OS). Each clone must create its own `.venv` (or use Conda) and install dependencies locally.

## One-shot setup (recommended)

From the repository root:

```bash
bash scripts/setup.sh --dev
source .venv/bin/activate   # Windows: .venv\Scripts\activate
cp .env.example .env        # then set FRED_API_KEY
```

`--dev` installs from **`requirements-dev.txt`**, which includes runtime deps plus **pytest**, **ruff**, **hdbscan**, Jupyter tooling, and packaging tools — aligned with **`pip install -e ".[dev]"`** in **`pyproject.toml`**.

Equivalent without the script:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"
pip install k-means-constrained   # optional; balanced KMeans
```

## Point Cursor at the right interpreter

1. **Command Palette** → **“Python: Select Interpreter”**.
2. Choose **`./.venv/bin/python`** (or the path shown under your repo root).

The **integrated terminal** inherits that environment when configured; if tests still use another Python, open a **new terminal** after switching interpreters.

**Conda users:** If you prefer a Conda env, activate it and run **`pip install -e ".[dev]"`** there — but then select **that** interpreter in Cursor so the editor, terminal, and **Test Explorer** agree.

## What “dev” pulls in (relevant to tooling)

| Area | Packages (see `pyproject.toml` `[project.optional-dependencies]` → `dev`) |
|------|-----------------------------------------------------------------------------|
| Tests | `pytest`, `pytest-cov` |
| Lint / format | `ruff` — run **`make lint`** or `ruff check` / `ruff format --check` (see `pyproject.toml` `[tool.ruff]`) |
| HDBSCAN unit tests | `hdbscan` — avoids skips in `tests/unit/test_density.py` when the module is importable |
| Notebooks | `ipykernel`, `jupyterlab` |

Optional extras not in `dev`:

- **`pip install -e ".[clustering-extras]"`** — `hdbscan` + `kneed` (overlap with dev for `hdbscan`; adds knee-detection helper).
- **`pip install -e ".[data-extras]"`** — Stooq / OpenBB fallbacks for ETF data.

## Sanity checks

```bash
source .venv/bin/activate   # if not already active
make lint                   # ruff
pytest tests/ -q            # full suite
bash scripts/check_env.sh   # optional: prints python/pytest/ruff versions
```

## Optional / slow tests (environment variables)

| Variable | Effect |
|----------|--------|
| `RUN_WHEEL_SMOKE=1` | Runs `tests/integration/test_wheel_smoke.py` (slow; network for pip) |
| `RUN_PIPELINE_INGEST_SMOKE=1` | Runs mocked `pipelines/01_ingest` smoke test (slow module load) |

Or: `pytest --pipeline-ingest-smoke` (sets the ingest flag; see `tests/conftest.py`).

## If the AI assistant “forgets” your packages

Agents only see what is installed in the **Python environment** attached to the workspace. After a fresh clone:

1. Create/activate **`.venv`** and **`pip install -e ".[dev]"`** (or `bash scripts/setup.sh --dev`).
2. **Select that interpreter** in Cursor.
3. In chat, you can **`@`-mention** this file (**`docs/CURSOR.md`**) when asking for test or lint commands so context matches this workflow.

---

*This file is documentation only; it does not change runtime behavior.*
