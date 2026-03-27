# Phase 37: Fork & dependency docs — Context

**Gathered:** 2026-03-26  
**Status:** Ready for planning  
**Source:** `.planning/ROADMAP.md` (v1.5) + `.planning/REQUIREMENTS.md` (**TMPL-01**)

## Phase boundary

Deliver **clear documentation** so forks and new clones know:

- Which file is **authoritative** for package metadata and dependency lists (**`pyproject.toml`**).
- How **`requirements.txt`** / **`requirements-dev.txt`** relate to it (convenience / `pip install -r` parity).
- How **`scripts/setup.sh`**, **`make setup`**, and **`pip install -e ".[dev]"`** fit together.

**Non-goals:** Changing dependency versions; refactoring CI; editing `legacy/`.

## Implementation decisions (locked)

- **Canonical source:** `[project]` and `[project.optional-dependencies]` in **`pyproject.toml`** define the installable package `trading-crab-lib` and extras (`dev`, `data-extras`, `clustering-extras`).
- **Pinned `-r` installs:** **`requirements.txt`** and **`requirements-dev.txt`** exist for `pip install -r` workflows and already state they align with **`pyproject.toml`** (see header comments in `requirements.txt`).
- **New doc:** Add **`docs/DEPENDENCIES.md`** as the single deep-dive; link from **`README.md`** (Installation) and **`docs/CURSOR.md`** (first-run).

## Canonical references

- `pyproject.toml` — `[project]`, `[project.optional-dependencies]`, `[build-system]`
- `requirements.txt`, `requirements-dev.txt` — headers and purpose
- `scripts/setup.sh` — uses `-r requirements*.txt`
- `README.md` — Installation, Makefile, Conda sections
- `docs/CURSOR.md` — IDE setup; already mentions `pip install -e ".[dev]"`

## Deferred

- Lockfile generation (`pip-compile`) — mentioned in `requirements.txt` header only; no new automation in this phase.
