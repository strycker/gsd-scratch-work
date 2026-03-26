# Phase 31: Library workspace & path API — Context

**Gathered:** 2026-03-25  
**Status:** Ready for planning  
**Source:** ROADMAP Phase 31, **PKG-10**, **`.planning/research/ARCHITECTURE.md`**

---

## Phase boundary

**In scope:** Replace implicit **`Path(__file__).parent.parent.parent`** “repo root” semantics with a **resolvable workspace API** so **`pip install`** users can set **explicit directories** (or environment variables) for config, data, and outputs, while **editable / repo checkout** keeps today’s layout by detection or the same relative walk.

**Out of scope for Phase 31:** PyPI publish checklist (**Phase 32**), submodule code ports, changing **`config/settings.yaml`** schema.

---

## Locked decisions

1. **Environment contract (installed / CI):** Support explicit paths via env vars documented in code and README. Prefer **`TRADING_CRAB_ROOT`** (single tree: `config/`, `data/`, `outputs/`) **or** granular **`TRADING_CRAB_CONFIG`**, **`TRADING_CRAB_DATA`**, **`TRADING_CRAB_OUTPUT`** as **directory** paths (config dir = parent of `settings.yaml` or the dir containing YAML — spell out one convention in implementation).
2. **Repo detection:** When env vars unset, **walk parents** of the installed package for a marker tie-break (e.g. directory containing **`config/settings.yaml`** and **`pyproject.toml`** with `trading-crab-lib` / project name) before falling back; if under **`site-packages`** with no marker, **require** env or **clear error** with message listing expected vars (no silent bogus paths).
3. **Backward compatibility:** Module-level **`ROOT`**, **`CONFIG_DIR`**, **`DATA_DIR`**, **`OUTPUT_DIR`** remain the public surface; implementation resolves them once at import via a small internal module (e.g. **`paths.py`**).
4. **`load()` / `CheckpointManager`:** `load(settings_path=...)` and `CheckpointManager(checkpoint_dir=...)` already exist; Phase 31 ensures **defaults** use resolved dirs, not broken site-packages relatives.
5. **Docs:** **README.md** (or **`docs/`**) gains a **“Library-only install”** subsection with copy-pastable env + Python snippet per ROADMAP.

---

## Canonical references

| Path | Role |
|------|------|
| `src/trading_crab_lib/__init__.py` | Current `ROOT` / dir constants |
| `src/trading_crab_lib/config.py` | `load()`, `CONFIG_DIR` default |
| `src/trading_crab_lib/checkpoints.py` | `DATA_DIR`, optional `checkpoint_dir` |
| `.planning/research/ARCHITECTURE.md` | Path tension + recommendation |
| `README.md` | User-facing install story |

---

*Phase: 31-v1-3-library-workspace-paths*
