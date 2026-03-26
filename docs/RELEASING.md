# Releasing `trading-crab-lib`

Checklist for maintainers: build artifacts, upload to TestPyPI, then PyPI.

## Prerequisites

- **Python 3.10+** (aligned with `requires-python` in `pyproject.toml`).
- Editable install with dev tools: `pip install -e ".[dev]"` (includes `build`, `twine`, `pytest`, `ruff`).
- Accounts on [PyPI](https://pypi.org/) and [TestPyPI](https://test.pypi.org/).
- API tokens for uploads (recommended: **API token** per project, not account password).

## Build

From the repository root:

```bash
bash scripts/build_dist.sh
```

This runs `python -m build`, then `twine check dist/*`, and lists `dist/`.

Equivalent manual steps:

```bash
rm -rf dist/ build/
python -m build
twine check dist/*
```

## TestPyPI

Configure credentials (pick one):

- **`~/.pypirc`** with a `testpypi` repository section, **or**
- Environment variables: `TWINE_USERNAME=__token__` and `TWINE_PASSWORD=<testpypi-api-token>`.

Upload:

```bash
twine upload --repository testpypi dist/*
```

Smoke-install from TestPyPI (use the version you uploaded):

```bash
pip install -i https://test.pypi.org/simple/ trading-crab-lib==0.1.0
```

(TestPyPI may not have all dependencies mirrored; a full runtime check is often done against PyPI deps plus the TestPyPI package.)

## PyPI (production)

```bash
twine upload dist/*
```

Use PyPI API token (`TWINE_USERNAME=__token__`, `TWINE_PASSWORD=<pypi-token>`) or `~/.pypirc` `pypi` section.

**Yanking vs deleting:** Prefer [yanking](https://pypi.org/help/#yanked) a bad release so consumers pinning exact versions see the yank; deleting a release is discouraged and may break mirrors.

## Trusted Publishing

PyPI supports **Trusted Publishers** (e.g. GitHub Actions OIDC) so CI can upload without a long-lived PyPI password. See the official guide: [Trusted publishers](https://docs.pypi.org/trusted-publishers/).

No OIDC workflow is checked into this repository by default; use the appendix below if you add publishing to CI.

## Package name on PyPI

The distribution name is **`trading-crab-lib`**. If that name is already taken on PyPI, choose a new **`[project].name`** in `pyproject.toml` (and update imports/docs accordingly) or confirm ownership of the existing project. Validating on **TestPyPI** first is recommended.

---

## Appendix: example GitHub Actions workflow (optional)

This snippet is **not** active in-repo; copy to `.github/workflows/publish-pypi.yml` and configure a `pypi` **environment** + Trusted Publisher on PyPI.

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]
  workflow_dispatch:

permissions:
  contents: read
  id-token: write

jobs:
  publish:
    runs-on: ubuntu-latest
    environment: pypi
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install build twine
      - run: python -m build
      - run: twine check dist/*
      - uses: pypa/gh-action-pypi-publish@release/v1
        with:
          packages-dir: dist/
```

After enabling **Trusted Publishing** for this repo on [pypi.org](https://pypi.org/), uploads use OIDC instead of stored tokens in GitHub Secrets.
