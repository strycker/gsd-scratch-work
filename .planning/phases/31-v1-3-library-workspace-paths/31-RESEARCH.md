# Phase 31 — Technical research

**Phase:** 31 — Library workspace & path API (**PKG-10**)  
**Researched:** 2026-03-25

## Questions

1. Where does **`trading_crab_lib`** assume **`ROOT`** today beyond **`__init__.py`**?
2. What is the minimal **env + detection** surface to satisfy ARCHITECTURE without rewiring every call site?

## Findings

### Import-time consumers of `CONFIG_DIR` / `DATA_DIR` / `OUTPUT_DIR`

| Module | Usage |
|--------|--------|
| `__init__.py` | Defines constants |
| `config.py` | Default `settings_path`, `portfolio_path` |
| `checkpoints.py` | `CHECKPOINT_DIR`, `_config_hash()` |
| `clustering.py` | `CONFIG_DIR / "settings.yaml"` for manifest hash |
| `email.py` | `CONFIG_DIR`, `OUTPUT_DIR` defaults |
| `plotting.py` | `OUTPUT_DIR` → `PLOT_DIR` |
| `reporting.py` | `OUTPUT_DIR` paths |

**Implication:** Resolving paths **once** in **`__init__.py`** before submodules that `from trading_crab_lib import DATA_DIR` are loaded is sufficient, provided **`__init__.py`** assigns **`CONFIG_DIR`**, **`DATA_DIR`**, **`OUTPUT_DIR`** (and **`ROOT`**) **before** `from .config import load` and lazy submodule paths only read those constants after package init completes.

### Circular import note

`config.py` does `from trading_crab_lib import CONFIG_DIR`. Safe if **`__init__.py`** sets **`CONFIG_DIR`** **before** `from .config import load`.

### Recommended implementation shape

- New **`paths.py`**: **`LibraryPaths`** (`NamedTuple` or dataclass): **`root`**, **`config_dir`**, **`data_dir`**, **`output_dir`**; **`resolve_library_paths()`** implements env → walk → error.
- **`__init__.py`**: `_paths = resolve_library_paths(); ROOT = _paths.root; ...`
- **`tests/`**: **`monkeypatch`** **`trading_crab_lib.paths.__file__`** or **`_package_root`** helper to simulate **`site-packages`** layout; assert env-only resolution; second test: fake repo layout with **`config/settings.yaml`** + **`pyproject.toml`**.

### pyproject / package metadata

Touch **`pyproject.toml`** only if **keywords** / **classifiers** / **readme** pointers need alignment for “library-only” story; heavy **PKG-11** release metadata deferred to Phase 32.

## Validation Architecture

Phase 31 is **code + tests + README**. **Automated:** `pytest` on new **`test_paths_*.py`** or **`test_workspace_*.py`**; **`ruff`** / existing CI; `grep` for env prefix **`TRADING_CRAB_`** in **`paths.py`**. **Manual:** Install package in clean venv, unset env, expect **clear error** or documented default (per plan). **Sampling:** run new unit tests after each task touching **`paths.py`** / **`__init__.py`**.

## RESEARCH COMPLETE
