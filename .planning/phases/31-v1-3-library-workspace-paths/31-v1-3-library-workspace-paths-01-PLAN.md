---
phase: 31-v1-3-library-workspace-paths
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - src/trading_crab_lib/paths.py
  - src/trading_crab_lib/__init__.py
  - README.md
  - tests/unit/test_library_paths.py
  - .planning/phases/31-v1-3-library-workspace-paths/31-SUMMARY.md
  - .planning/phases/31-v1-3-library-workspace-paths/31-v1-3-library-workspace-paths-01-SUMMARY.md
  - .planning/phases/31-v1-3-library-workspace-paths/31-VALIDATION.md
  - .planning/REQUIREMENTS.md
  - .planning/ROADMAP.md
  - .planning/STATE.md
autonomous: true
requirements:
  - PKG-10
user_setup:
  - None required for planning; execute may use a clean venv optional for manual smoke.
must_haves:
  truths:
    - "`src/trading_crab_lib/paths.py` defines `LibraryPaths` and `resolve_library_paths()` using env vars `TRADING_CRAB_ROOT` and/or `TRADING_CRAB_CONFIG`, `TRADING_CRAB_DATA`, `TRADING_CRAB_OUTPUT`."
    - "`__init__.py` sets `ROOT`, `CONFIG_DIR`, `DATA_DIR`, `OUTPUT_DIR` from the resolver before importing `config.load`."
    - "`README.md` contains a **Library-only install** (or equivalent heading) subsection with env examples."
    - "`tests/unit/test_library_paths.py` passes and covers simulated site-packages + env override vs repo detection."
  artifacts:
    - path: "src/trading_crab_lib/paths.py"
      provides: "PyPI-safe path resolution"
---

<objective>
Deliver **PKG-10:** a **workspace / path resolver** for **`trading_crab_lib`** so consumers after **`pip install`** can point config, data, and outputs via **environment variables** or explicit resolution, while **repo checkouts** keep working without extra env (parent walk to tree containing **`config/settings.yaml`**).
</objective>

**Non-goals:** Release engineering (**Phase 32**); changing checkpoint manifest schema; submodule edits.

<execution_context>
@.planning/phases/31-v1-3-library-workspace-paths/31-CONTEXT.md
@.planning/phases/31-v1-3-library-workspace-paths/31-RESEARCH.md
@.planning/research/ARCHITECTURE.md
@src/trading_crab_lib/__init__.py
@src/trading_crab_lib/config.py
@.planning/ROADMAP.md
</execution_context>

<tasks>

<task type="auto" tdd="false">
  <name>31-01-01 — Add paths.py (LibraryPaths + resolve_library_paths)</name>
  <read_first>
    - `src/trading_crab_lib/__init__.py`
    - `.planning/research/ARCHITECTURE.md`
    - `.planning/phases/31-v1-3-library-workspace-paths/31-CONTEXT.md`
  </read_first>
  <action>
    Add **`src/trading_crab_lib/paths.py`**:

    1. **`@dataclass(frozen=True) class LibraryPaths`** with fields **`root`**, **`config_dir`**, **`data_dir`**, **`output_dir`** (all **`Path`**). **`root`** is the implied project tree root (parent of **`config`**, **`data`**, **`outputs`** when using **`TRADING_CRAB_ROOT`**).

    2. **`def resolve_library_paths(*, package_file: Path | None = None) -> LibraryPaths`** — **`package_file`** defaults to **`Path(__file__)`** of **`paths.py`**; tests pass a temp **`conftest`-friendly** path.

    3. **Resolution order:**
       - If **`os.environ["TRADING_CRAB_ROOT"]`** is set and non-empty: **`root = Path(...).resolve()`**, **`config_dir = root / "config"`**, **`data_dir = root / "data"`**, **`output_dir = root / "outputs"`** (create-not-required in resolver; callers mkdir as today).
       - Else if **any** of **`TRADING_CRAB_CONFIG`**, **`TRADING_CRAB_DATA`**, **`TRADING_CRAB_OUTPUT`** set: resolve each set var to **`Path`**; for **unset** components, if **`TRADING_CRAB_ROOT`** is also set use layout above; otherwise **raise `RuntimeError`** listing required env vars (no partial silent defaults into **`site-packages`**).
       - Else **walk** parents starting from **`package_file.parent`** (the **`trading_crab_lib`** package directory): for each ancestor **`p`**, if **`(p / "config" / "settings.yaml").is_file()`**, treat **`p`** as **`root`**, set **`config_dir = p / "config"`**, **`data_dir = p / "data"`**, **`output_dir = p / "outputs"`**, return **`LibraryPaths`**.
       - Else (**no marker found**, typical **`site-packages`** install): **raise `RuntimeError`** whose message includes substring **`TRADING_CRAB_ROOT`** and documents that **`pip install`** users must set env vars.

    4. Module docstring: bullet list env vars and one-line semantics (**`TRADING_CRAB_CONFIG`** = **directory** containing **`settings.yaml`**, i.e. **`config_dir`** — not path to the YAML file unless you document file path; **prefer directory = `CONFIG_DIR`** to match **`load()`**).

    Adjust **(3)** if **`TRADING_CRAB_CONFIG`** is defined as **`config_dir`** directly: then **`config_dir = Path(env).resolve()`**, same for DATA/OUTPUT when those envs set.

    Keep **`frozen` dataclass** and **no** imports from **`config`** (avoid cycles).
  </action>
  <acceptance_criteria>
    - `test -f src/trading_crab_lib/paths.py` exits 0
    - `grep -q "class LibraryPaths" src/trading_crab_lib/paths.py` exits 0
    - `grep -q "def resolve_library_paths" src/trading_crab_lib/paths.py` exits 0
    - `grep -q "TRADING_CRAB_ROOT" src/trading_crab_lib/paths.py` exits 0
  </acceptance_criteria>
</task>

<task type="auto" tdd="true">
  <name>31-01-02 — Unit tests for resolver (env + walk + site-packages error)</name>
  <read_first>
    - `src/trading_crab_lib/paths.py`
    - `tests/conftest.py`
    - `tests/unit/test_transforms.py` (fixture style reference)
  </read_first>
  <action>
    Add **`tests/unit/test_library_paths.py`**:

    1. **`test_trading_crab_root_sets_all_dirs`** — **`monkeypatch.setenv("TRADING_CRAB_ROOT", str(tmp_path))`**, create **`tmp_path/config`**, **`data`**, **`out`** optional; call **`resolve_library_paths(package_file=tmp_path / "dummy" / "trading_crab_lib" / "paths.py")`** — actually resolver uses **`package_file.parent`** as start of walk; for env branch walk may be skipped. Implement test so **`TRADING_CRAB_ROOT`** branch does **not** require walk: pass any **`package_file`** under **`tmp_path`** if resolution short-circuits on env first.

    2. **`test_walk_finds_repo_layout`** — under **`tmp_path`**, create **`project/config/settings.yaml`** (empty file ok), **`project/vendor/trading_crab_lib/paths.py`** not needed — call **`resolve_library_paths(package_file=tmp_path / "project" / "vendor" / "trading_crab_lib" / "paths.py")`** with **`package_file.parent`** = **`.../trading_crab_lib`**. Walk upward must find **`project`**.

    3. **`test_site_packages_raises_with_message`** — **`package_file`** = path with parents that never contain **`config/settings.yaml`** (e.g. deep chain under **`tmp_path / "lib" / "site-packages" / "trading_crab_lib" / "paths.py"`**); clear env vars; expect **`RuntimeError`** and assert **`"TRADING_CRAB_ROOT"`** in **`str(exc)`**.

    Clear env keys in teardown or use **`monkeypatch.delenv(..., raising=False)`** for **`TRADING_CRAB_*`**.
  </action>
  <acceptance_criteria>
    - `pytest tests/unit/test_library_paths.py -q` exits 0
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>31-01-03 — Wire __init__.py and exports</name>
  <read_first>
    - `src/trading_crab_lib/__init__.py`
    - `src/trading_crab_lib/paths.py`
  </read_first>
  <action>
    1. In **`__init__.py`**, **`from .paths import LibraryPaths, resolve_library_paths`**, then **`_paths = resolve_library_paths()`**, then assign **`ROOT = _paths.root`**, **`CONFIG_DIR = _paths.config_dir`**, **`DATA_DIR = _paths.data_dir`**, **`OUTPUT_DIR = _paths.output_dir`** **before** **`from .config import load`** (keep existing import order compatibility).

    2. Extend **`__all__`** with **`"LibraryPaths"`** and **`"resolve_library_paths"`**.

    3. Run **`python -c "import trading_crab_lib as t; print(t.CONFIG_DIR)"`** from repo root in CI locally — should print **`.../config`** under repo (execute verifies).
  </action>
  <acceptance_criteria>
    - `grep -q "resolve_library_paths" src/trading_crab_lib/__init__.py` exits 0
    - `grep -q "LibraryPaths" src/trading_crab_lib/__init__.py` exits 0
    - `pytest tests/unit/test_library_paths.py tests/unit/test_config.py -q` exits 0 (or full `pytest tests/ -q` if fast enough)
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>31-01-04 — README library-only install subsection</name>
  <read_first>
    - `README.md` (headings, install section)
    - `src/trading_crab_lib/paths.py` (final env names)
  </read_first>
  <action>
    In **`README.md`**, add a subsection (suggested heading **`### Library-only install (pip)`** or **`## Library-only install`**) that:
    - Contrasts **full repo checkout** (editable, default paths) vs **`pip install trading-crab-lib`** (set **`TRADING_CRAB_ROOT`** or granular vars).
    - Shows **copy-pastable** **`export TRADING_CRAB_ROOT=...`** (POSIX) and one **`python -c "import trading_crab_lib as c; print(c.CONFIG_DIR)"`** line.

    Do not duplicate **Phase 32** release instructions beyond pointing at **`pip install`** + env vars.
  </action>
  <acceptance_criteria>
    - `grep -qi "library-only\\|pip install" README.md` exits 0
    - `grep -q "TRADING_CRAB_ROOT" README.md` exits 0
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>31-01-05 — PKG-10 traceability, SUMMARY, VALIDATION, hybrid 01-SUMMARY</name>
  <read_first>
    - `.planning/REQUIREMENTS.md`
    - `.planning/ROADMAP.md`
    - `.planning/STATE.md`
    - `.planning/phases/30-v1-3-submodule-unification-blueprint/30-SUMMARY.md`
  </read_first>
  <action>
    1. **`31-SUMMARY.md`** — execution date, artifacts list, **`pytest`** command.
    2. **`REQUIREMENTS.md`** — **`PKG-10`** **`[x]`**, Evidence paths, traceability **Complete**.
    3. **`ROADMAP.md`** — Phase **31** **`[x]`**; milestone line **28–31** shipped.
    4. **`STATE.md`** — Phase **31** complete; next **32**; bump **`completed_phases`** (**4**/7).
    5. **`31-VALIDATION.md`** — **`status: approved`**, **`nyquist_compliant: true`**, approval date
    6. **`31-v1-3-library-workspace-paths-01-SUMMARY.md`** — hybrid **As-built / Plan fidelity / Delta / Verification**.
  </action>
  <acceptance_criteria>
    - `grep -q "PKG-10 | 31 | Complete" .planning/REQUIREMENTS.md` exits 0
    - `grep -q '\[x\].*PKG-10' .planning/REQUIREMENTS.md` exits 0
    - `grep -q '\[x\].*Phase 31:' .planning/ROADMAP.md` exits 0
    - `test -f .planning/phases/31-v1-3-library-workspace-paths/31-SUMMARY.md` exits 0
    - `node .codex/get-shit-done/bin/gsd-tools.cjs validate health` → **`healthy`**, empty **`errors`**
  </acceptance_criteria>
</task>

</tasks>

<verification_criteria>

1. **`pytest tests/ -q`** green after execute.
2. **`validate health`** — no **I001** for this plan path (hybrid **01-SUMMARY**).

</verification_criteria>
