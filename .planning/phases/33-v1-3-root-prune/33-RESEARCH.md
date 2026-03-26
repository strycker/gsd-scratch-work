---
phase: 33
title: Root prune — research
status: complete
---

# Phase 33 — RESEARCH.md

**Question:** What must we know to **PRUNE-10** safely — redundant root-only assets without touching **`legacy/`** or **`*_repo-copy/`**?

**Requirement:** **PRUNE-10** — Remove redundant root notebooks/scratch/duplicate docs (excluding **`legacy/`**, **`*_repo-copy/`**).

---

## Scope boundaries (hard)

| In scope | Out of scope |
|----------|----------------|
| Files/dirs at **repository root** (and **root-level** patterns like stray **`*.ipynb`** if any) | **`legacy/`** — never delete |
| **`notebooks/`** (canonical exploration; may **dedupe** vs root if duplicates exist) | **`claude-scratch-work-repo-copy/`**, **`trading-crab-lib-repo-copy/`**, **`trading-crab-repo-copy/`** — read-only |
| **`docs/`** (new **`docs/RELEASING.md`**; other root markdown that duplicates **`.planning/`** or **`README`**) | **`.planning/`**, **`.codex/`** — GSD tooling trees |
| Cross-links in **`CLAUDE.md`**, **`RUNBOOK.md`**, **`ARCHITECTURE.md`**, **`README.md`** | **`src/`**, **`pipelines/`** code refactors (Phase 34 docstrings) |

**Two “state” files:** Root **`STATE.md`** is a **human-readable product snapshot**; **`.planning/STATE.md`** is **GSD orchestration**. They are **not** redundant — pruning should **not** merge them without explicit stakeholder decision; at most add a one-line cross-reference.

**Two “roadmap” files:** Root **`ROADMAP.md`** = **product/feature** backlog; **`.planning/ROADMAP.md`** = **milestone v1.3 phases**. Keep both; document distinction in inventory if confusion is the issue.

---

## Inventory methodology (execute phase)

1. **List** root: `*.md`, `*.ipynb`, loose dirs (exclude `.git`, `.venv`, `data`, `outputs`, `build`, `dist` if present).
2. **Classify** each path: canonical doc | duplicate | scratch | obsolete | keep-with-rationale.
3. **Grep** repo docs for relative links to each candidate path **before** delete.
4. **Prefer** delete only when **superseded** (e.g. empty stub, exact duplicate file) or **merge** one paragraph into **`README.md`**, **`CLAUDE.md`**, or **`docs/`**.
5. **Preserve history:** deletions via normal `git rm` / commit — **git** retains blobs.

---

## Risk: link rot

After any removal, run:

- `rg -n "FILENAME|relative/path" CLAUDE.md README.md RUNBOOK.md ARCHITECTURE.md docs/`
- **`pytest tests/ -q`**
- **`node .codex/get-shit-done/bin/gsd-tools.cjs validate health`** (if project uses it)

---

## Validation Architecture

Automated verification for PRUNE-10:

1. **No forbidden paths touched:** SUMMARY / script asserts **no** `git rm` under **`legacy/`** or **`*_repo-copy*/`** (allowlist check).
2. **Tests:** **`pytest tests/ -q`** green after edits.
3. **Docs:** Required links in **`CLAUDE.md` / `RUNBOOK.md` / `ARCHITECTURE.md`** still resolve (grep or manual spot-check per plan).
4. **Artifact:** **`33-*-INVENTORY.md`** (or equivalent table in **SUMMARY**) lists every path with **action + rationale**.

Dimension 8: **`33-VALIDATION.md`** tracks sampling; execution uses grep + pytest per wave.

---

## RESEARCH COMPLETE

Ready for **`33-*-PLAN.md`**: inventory-first, link checks, minimal deletes, **PRUNE-10** closure in **REQUIREMENTS.md**.
