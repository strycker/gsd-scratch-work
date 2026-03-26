---
phase: 32-v1-3-pypi-release-engineering
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - LICENSE
  - pyproject.toml
  - README.md
  - docs/RELEASING.md
  - scripts/build_dist.sh
  - .planning/phases/32-v1-3-pypi-release-engineering/32-SUMMARY.md
  - .planning/phases/32-v1-3-pypi-release-engineering/32-v1-3-pypi-release-engineering-01-SUMMARY.md
  - .planning/REQUIREMENTS.md
  - .planning/ROADMAP.md
  - .planning/STATE.md
autonomous: true
requirements:
  - PKG-11
user_setup:
  - Maintainer: PyPI + TestPyPI API tokens for manual upload verification (optional during execute).
must_haves:
  truths:
    - "Root `LICENSE` file exists and `pyproject.toml` exposes license + `readme` + `[project.urls]` suitable for PyPI."
    - "`pyproject.toml` classifiers include Python 3.10 through 3.14 (or SUMMARY documents any Trove gap for 3.14)."
    - "`docs/RELEASING.md` lists exact commands: `python -m build`, `twine check`, TestPyPI upload, production upload, and optional Trusted Publishing pointers."
    - "Maintainers can reproduce `dist/*.whl` via `scripts/build_dist.sh` (or documented one-liner equivalent)."
    - "`README.md` includes a discoverable **PyPI** / **`pip install trading-crab-lib`** story cross-linked to `docs/RELEASING.md`."
  artifacts:
    - path: "docs/RELEASING.md"
      provides: "Release checklist"
    - path: "pyproject.toml"
      provides: "PEP 621 metadata for PyPI"
---

<objective>
Deliver **PKG-11:** make **`trading-crab-lib`** **publishable** on PyPI — reproducible **`python -m build`** output, **`twine check`**, documented **TestPyPI** / **PyPI** uploads, **OSS metadata** (**LICENSE**, **urls**, **readme**), **Python 3.10–3.14** classifiers, optional **Trusted Publishing** documentation — without putting pipelines/notebooks in the wheel.
</objective>

**Non-goals:** Claiming the PyPI name if unavailable (document only); changing **`src/`** package layout beyond metadata.

<execution_context>
@.planning/ROADMAP.md
@.planning/REQUIREMENTS.md
@.planning/STATE.md
@.planning/phases/32-v1-3-pypi-release-engineering/32-RESEARCH.md
@pyproject.toml
@README.md
</execution_context>

<tasks>

<task type="auto" tdd="false">
  <name>32-01-01 — Add LICENSE and complete PEP 621 metadata in pyproject.toml</name>
  <read_first>
    - `pyproject.toml`
    - `.planning/phases/32-v1-3-pypi-release-engineering/32-RESEARCH.md`
    - https://packaging.python.org/en/latest/guides/writing-pyproject-toml/ (if ambiguous)
  </read_first>
  <action>
    1. Add root **`LICENSE`** file with **MIT** text (SPDX: `MIT`) — use standard OSI MIT template with copyright year **2026** and copyright holder **`trading-crab-lib` contributors** (or repository owner name if documented elsewhere).

    2. In **`pyproject.toml`** under **`[project]`**:
       - Set **`readme = "README.md"`** (if setuptools needs explicit content-type, use the table form supported by your setuptools version).
       - Set **`license = { text = "MIT" }`** **or** equivalent PEP 621 + setuptools-supported **`license-files`** pointing at **`LICENSE`** (single consistent story).
       - Add **`[project.urls]`** with at least:
         - **`Homepage`** = repository URL or placeholder `https://github.com/OWNER/REPO` replaced with **actual** remote if `git remote -v` shows one; if no remote, use **`Documentation`** → README anchor and **`Repository`** → `"https://github.com/PLACEHOLDER/trading-crab"` only if roadmap requires — **prefer real `git` remote URL** when present.
       - Append classifier **`Programming Language :: Python :: 3.14`** after **`3.13`** entry.
       - Add one-line comment if Trove does not accept 3.14 yet (executor verifies by running build/twine).

    3. Do **not** change **`[tool.setuptools.packages.find]`** — wheel must remain **`src/trading_crab_lib` only**.
  </action>
  <acceptance_criteria>
    - `test -f LICENSE` exits 0
    - `grep -qi "MIT" LICENSE` exits 0
    - `grep -q "readme" pyproject.toml` exits 0
    - `grep -q "\[project.urls\]" pyproject.toml` exits 0
    - `grep -q "Programming Language :: Python :: 3.14" pyproject.toml` exits 0 OR `32-*-SUMMARY.md` documents classifier deferral with reason
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>32-01-02 — Add build + twine to dev extras; add scripts/build_dist.sh</name>
  <read_first>
    - `pyproject.toml`
    - `scripts/smoke_wheel_paths.sh`
  </read_first>
  <action>
    1. Add to **`[project.optional-dependencies].dev`**: **`build>=1.0`** and **`twine>=5.0`** (minimum bounds consistent with project style).

    2. Create **`scripts/build_dist.sh`**:
       - `set -euo pipefail`
       - `cd` to repo root via `$(dirname "$0")/..`
       - Remove prior artifacts: **`rm -rf dist/`** (or `rm -rf build/` if needed for clean setuptools)
       - Run **`python -m build`**
       - Run **`twine check dist/*`**
       - Echo success with **`dist/`** listing

    3. **`chmod +x scripts/build_dist.sh`**
  </action>
  <acceptance_criteria>
    - `grep -q "build>=" pyproject.toml` exits 0
    - `grep -q "twine>=" pyproject.toml` exits 0
    - `test -x scripts/build_dist.sh` exits 0
    - `grep -q "twine check" scripts/build_dist.sh` exits 0
    - `bash scripts/build_dist.sh` exits 0 (from repo root with dev deps installed)
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>32-01-03 — Write docs/RELEASING.md (checklist + TestPyPI + PyPI + Trusted Publishing)</name>
  <read_first>
    - `.planning/phases/32-v1-3-pypi-release-engineering/32-RESEARCH.md`
    - `scripts/build_dist.sh`
  </read_first>
  <action>
    Create **`docs/RELEASING.md`** with markdown sections:

    1. **Prerequisites** — Python **3.10+**, **`pip install -e ".[dev]"`** (or equivalent), PyPI and TestPyPI accounts, API tokens.

    2. **Build** — exact command **`bash scripts/build_dist.sh`** (and plain **`python -m build`** + **`twine check dist/*`** as alternative).

    3. **TestPyPI** — **`twine upload --repository testpypi dist/*`**; note **`~/.pypirc`** or **`TWINE_USERNAME=__token__`** / **`TWINE_PASSWORD`** env vars; **`pip install -i https://test.pypi.org/simple/ trading-crab-lib==VERSION`** smoke.

    4. **PyPI** — **`twine upload dist/*`** (production); warn about **yanking** vs deleting.

    5. **Trusted Publishing** — short subsection with link to **https://docs.pypi.org/trusted-publishers/**** and optional **GitHub Actions** pattern (`permissions: id-token: write`, **`pypa/gh-action-pypi-publish`** or PyPI docs); state “not configured in-repo” unless task 32-01-05 adds workflow.

    6. **Name collision** — if **`trading-crab-lib`** is taken, document choosing **`trading-crab-lib`** on TestPyPI first or renaming in **`pyproject.toml`** (major policy — one paragraph).
  </action>
  <acceptance_criteria>
    - `test -f docs/RELEASING.md` exits 0
    - `grep -q "twine upload" docs/RELEASING.md` exits 0
    - `grep -q "test.pypi.org" docs/RELEASING.md` exits 0
    - `grep -qi "trusted" docs/RELEASING.md` exits 0
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>32-01-04 — README: PyPI install story + link to RELEASING</name>
  <read_first>
    - `README.md`
    - `docs/RELEASING.md`
  </read_first>
  <action>
    Add a subsection under **Installation** (or new **PyPI** section) that includes:

    - **`pip install trading-crab-lib`** (document **pre-release**: install from TestPyPI index example from **RELEASING.md**).
    - Reminder: set **`TRADING_CRAB_ROOT`** (link to existing **Library-only install** subsection anchor if present).
    - Link **`docs/RELEASING.md`** for maintainers (**`[RELEASING.md](docs/RELEASING.md)`**).

    Keep tone consistent with existing README; do not remove **clone + editable** workflow — add PyPI as an alternative.
  </action>
  <acceptance_criteria>
    - `grep -qi "pip install trading-crab-lib" README.md` exits 0
    - `grep -q "docs/RELEASING.md" README.md` exits 0
    - `grep -qi "TRADING_CRAB" README.md` exits 0
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>32-01-05 — Optional: GitHub Actions workflow for Trusted Publishing (document-only if skipped)</name>
  <read_first>
    - `docs/RELEASING.md`
    - `.github/` (if exists)
  </read_first>
  <action>
    **Either:**

    - **A)** Add **`.github/workflows/publish-pypi.yml`** that runs on **`release`** (or **`workflow_dispatch`**): checkout, setup Python **3.12** (or matrix **3.10–3.14** only if needed), **`pip install build twine`**, **`python -m build`**, **`twine check`**, upload with **`pypa/gh-action-pypi-publish@release/v1`** using **`permissions: id-token: write`**, **environment** `pypi` optional; **OR**

    - **B)** Do **not** add workflow; extend **`docs/RELEASING.md`** with copy-paste **GitHub Actions** YAML snippet in an appendix.

    Record choice in **`32-v1-3-pypi-release-engineering-01-SUMMARY.md`** under **As-built**.
  </action>
  <acceptance_criteria>
    - If workflow added: `test -f .github/workflows/publish-pypi.yml` exits 0 AND `grep -q "gh-action-pypi-publish" .github/workflows/publish-pypi.yml` exits 0
    - If skipped: `grep -q "GitHub Actions" docs/RELEASING.md` exits 0 AND **01-SUMMARY** states **B)** chosen
  </acceptance_criteria>
</task>

<task type="auto" tdd="true">
  <name>32-01-06 — Regression: pytest + optional RUN_WHEEL_SMOKE</name>
  <read_first>
    - `tests/integration/test_wheel_smoke.py`
  </read_first>
  <action>
    1. Run **`pytest tests/ -q`** — must pass.

    2. Optionally run **`RUN_WHEEL_SMOKE=1 pytest tests/integration/test_wheel_smoke.py -q`** once if network available; if skipped, note in SUMMARY.
  </action>
  <acceptance_criteria>
    - `pytest tests/ -q` exits 0
  </acceptance_criteria>
</task>

</tasks>

---

## Verification criteria (phase)

- **`REQUIREMENTS.md`**: **PKG-11** marked complete with evidence paths.
- **`ROADMAP.md` / `STATE.md`**: Phase **32** progress updated per project convention.
- **`32-SUMMARY.md`** + **`32-v1-3-pypi-release-engineering-01-SUMMARY.md`**: As-built, plan fidelity, TestPyPI/PyPI manual step status.

---

## PLANNING COMPLETE
