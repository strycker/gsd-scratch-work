# Project Research Summary — Milestone v1.3

**Project:** Trading-Crab / `trading-crab-lib`  
**Domain:** Python quant research library + monorepo sync + PyPI OSS  
**Researched:** 2026-03-25  
**Confidence:** HIGH on packaging/process; MEDIUM on merge effort until submodule diffs are executed

## Executive Summary

v1.3 centers on **engineering hygiene and consolidation**: close GSD **PLAN/SUMMARY** gaps with **hybrid** narratives (as-built + promised + delta), **diff three read-only submodule mirrors** against the canonical root in a **fixed order** (library → claude-scratch → trading-crab) while refining order by **dependency/risk**, and **publish a single OSS wheel** (`trading-crab-lib`) sourced from **`src/`** only. The repo already uses **setuptools** + `src` layout; the **blocking architectural gap** for real PyPI consumers is **`ROOT`/`CONFIG_DIR`/`DATA_DIR`** assuming a checkout layout — v1.3 should introduce an explicit **workspace/path configuration** and tests for editable vs installed use.

Secondary themes: **root-only pruning** (notebooks, scratch, duplicate docs), **extensive rationale comments** (Google-style + file-level “why”), and **merge policy** that picks the **better-tested** implementation with **explicit human confirmation** before replacing code. **legacy/** and **submodule trees** stay read-only aside from **git refresh**.

## Key Findings

### Recommended stack (release)

- Keep **setuptools**; use **`python -m build`** + **Twine**; prefer **PyPI Trusted Publishing (OIDC)** from GitHub Actions.
- CI matrix **Python 3.10–3.14** before declaring support; extend **classifiers** / **`requires-python`** upper bound as 3.14 stabilizes.
- Document **optional extras** (`dev`, `data-extras`, `clustering-extras`) for OSS users.

### Feature / merge strategy

- **Order:** `trading-crab-lib-repo-copy` → `claude-scratch-work-repo-copy` → `trading-crab-repo-copy`, then **reconcile** with dependency-aware batches.
- **Superset:** Union of valuable capability with **one** implementation path; port tests from mirrors when they encode desired behavior.
- **I001 closure:** Hybrid summaries only — no reopened product scope unless delta finds a defect.

### Architecture

- Draw a hard line: **library in wheel** vs **pipeline/notebooks repo-only** (stakeholder intent).
- Fix **path coupling** before marketing the library to strangers on PyPI.

### Critical pitfalls

1. **`pip install` path bug** via implicit repo `ROOT`.
2. **Editing submodules** by mistake — enforce discipline.
3. **Nested mirror directories** misleading diffs — refresh and pin canonical paths.
4. **Superset creep** — confirm each merge chunk.
5. **Comment rot** — emphasize *why* and invariants, not line-by-line narration that duplicates code.

## Roadmap implications (for gsd-roadmapper)

Suggested requirement **themes** (to be REQ-ID’d next):

| Theme | Notes |
|-------|-------|
| **PLAN/SUMMARY** | Hybrid files for all current I001 plans |
| **Submodule analysis** | Matrix + ordered unification plan (execution phased) |
| **Workspace paths** | Explicit config/data API for library consumers |
| **PyPI** | Build, TestPyPI, PyPI, trusted publishing, README “install vs dev clone” |
| **Prune** | Root-only redundancy removal |
| **Narration** | Docstrings + file headers + major-block rationale |

**Starting phase number:** **28** (after v1.2 phase **27**).

## Clarifications captured (stakeholder)

- **A:** Three mirrors only; local clones suffice.  
- **B:** Hybrid summaries; phased merge order; prefer more tested impl **with confirm**; mirrors read-only except git pull.  
- **C:** One package `trading-crab-lib` from `src/`; public OSS; Python 3.10–3.14.  
- **D:** Breakage OK; extensive comments; prune root redundancy except legacy + mirrors.

---

*Next GSD step:* **`$gsd-new-milestone` continuation — Define Requirements** from this summary, then roadmap approval.
