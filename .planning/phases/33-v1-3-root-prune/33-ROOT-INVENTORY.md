# Phase 33 — Root inventory → action

**Generated:** 2026-03-26 (execute phase 33)  
**Purpose:** PRUNE-10 — redundant root-only assets; **no** changes under `legacy/` or `*_repo-copy/`.

## Distinction: `STATE.md` vs `.planning/STATE.md`

| File | Role |
|------|------|
| **`STATE.md`** (root) | Human-readable **product** snapshot: pipeline status, tests, pitfalls pointers. |
| **`.planning/STATE.md`** | **GSD** orchestration: phase, milestone, next actions. |

**Action:** **keep both** — not duplicates.

## Distinction: `ROADMAP.md` vs `.planning/ROADMAP.md`

| File | Role |
|------|------|
| **`ROADMAP.md`** (root) | **Product** backlog (tiers, features, data sources). |
| **`.planning/ROADMAP.md`** | **Milestone** v1.3 phase list (28–34). |

**Action:** **keep both**.

## Inventory table

| path | kind | classification | proposed_action | rationale |
|------|------|----------------|-----------------|-----------|
| `ARCHITECTURE.md` | file | canonical | keep | Design reference for `src/` + pipeline. |
| `CLAUDE.md` | file | canonical | keep | Agent/project guide; update notebook tree if notebooks change. |
| `PITFALLS.md` | file | canonical | keep | Known gotchas. |
| `README.md` | file | canonical | keep | Primary user-facing entry; PyPI + install story. |
| `ROADMAP.md` | file | canonical | keep | Product roadmap (different from `.planning/ROADMAP.md`). |
| `RUNBOOK.md` | file | canonical | keep | Operations / pipeline runbook. |
| `STATE.md` | file | canonical | keep | Product state snapshot (≠ `.planning/STATE.md`). |
| `docs/RELEASING.md` | file | canonical | keep | Maintainer release checklist (Phase 32). |
| `notebooks/01_ingestion.ipynb` … `07_pairplot.ipynb` | file | canonical | keep | Numbered pipeline exploration. |
| `notebooks/08_diagnostics.ipynb` | file | canonical | keep | Diagnostics notebook (Phase 18). |
| `notebooks/09_raw_series.ipynb` | file | canonical (was `08_raw_series.ipynb`) | **renamed** (execute) | Two `08_*.ipynb` files were confusing; sequential **09** for raw-series exploration. |
| `build/`, `dist/` (if present) | dir | runtime | keep ignored | Listed in `.gitignore`; not committed. |
| `legacy/` | dir | **excluded** | **no touch** | Contract: reference-only. |
| `*_repo-copy/` | dir | **excluded** | **no touch** | Read-only mirrors. |

## Link audit

**Rename:** `08_raw_series.ipynb` → `09_raw_series.ipynb`

| Search | Result |
|--------|--------|
| `rg -n "08_raw_series"` in `CLAUDE.md`, `README.md`, `RUNBOOK.md`, `ARCHITECTURE.md`, `docs/` | **No matches** (filename not cited in prose). |
| **Action:** Safe rename; update **notebook count** strings in `CLAUDE.md` and `README.md` (`01–08` → `01–09`) where they describe the full set. |

**No other** merge/delete targets required for this pass — root `*.md` set is non-redundant.
