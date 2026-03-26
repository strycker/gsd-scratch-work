---
phase: 34
title: Library documentation pass — research
status: complete
---

# Phase 34 — RESEARCH.md

**Question:** How do we document **`src/trading_crab_lib/`** for **DOCS-10** without comment rot?

**Requirement:** **DOCS-10** — Google-style (or equivalent) **module + public API** docstrings, **file-level “why”**, **major-block rationale** — **not** line-by-line “what” narration.

---

## Conventions (target)

| Element | Guidance |
|---------|----------|
| **Module docstring** | 3–12 lines: purpose, non-obvious dependencies, link to pipeline step or config if relevant. |
| **Public functions/classes** | Google style: **`Args`**, **`Returns`**, **`Raises`** where useful; first line imperative summary. |
| **Private helpers** | One-line or omitted unless non-obvious invariant. |
| **Major blocks** | Short `# ---` or comment before non-obvious branches (e.g. publication lag, checkpoint policy). |

**Avoid:** Restating the next line of code; duplicating type hints in prose unless clarifying units or semantics.

---

## Tooling

- **`pytest tests/ -q`** — required after edits (no import breakage).
- **`python -m compileall -q src/trading_crab_lib`** — syntax check docstring edits did not break parsing.
- **`ruff check`:** Not currently in **`pyproject.toml`**. If **`ruff`** is absent, **do not** add it as a phase requirement unless CONTEXT says so; use **compileall + pytest** and note in **SUMMARY**.

---

## Inventory

~**30** **`.py`** files under **`src/trading_crab_lib/`** (including **`ingestion/`**, **`prediction/`**). **Coverage checklist** in **`34-SUMMARY.md`** must list each path **touched** or **waived** (e.g. thin **`__init__.py`** re-export only).

**Roadmap spot-check modules (expanded module docstrings):** **`config`**, **`checkpoints`**, **`transforms`**, **`prediction/classifier`**.

---

## Validation Architecture

1. **Automated:** **`pytest tests/ -q`** after each wave or at end.
2. **Automated:** **`compileall`** on **`src/trading_crab_lib`**.
3. **Checklist:** Every **`.py`** in SUMMARY → **done** or **waived** + reason.
4. **Spot-check:** Four named modules have measurably richer opening module docstrings (grep/line count or human read in VERIFICATION).

---

## RESEARCH COMPLETE

Ready for **`34-*-PLAN.md`** with batched file tasks and checklist closure.
