---
phase: 33-v1-3-root-prune
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - .planning/phases/33-v1-3-root-prune/33-ROOT-INVENTORY.md
  - CLAUDE.md
  - README.md
  - RUNBOOK.md
  - ARCHITECTURE.md
  - .planning/phases/33-v1-3-root-prune/33-SUMMARY.md
  - .planning/phases/33-v1-3-root-prune/33-v1-3-root-prune-01-SUMMARY.md
  - .planning/REQUIREMENTS.md
  - .planning/ROADMAP.md
  - .planning/STATE.md
autonomous: true
requirements:
  - PRUNE-10
user_setup:
  - Review inventory table before bulk deletes; executor records final actions in SUMMARY.
must_haves:
  truths:
    - "Phase artifact includes a **PR list / table** (inventory): each pruned or merged path with **rationale**; git history preserves deleted content via normal commits."
    - "**`CLAUDE.md`**, **`RUNBOOK.md`**, **`ARCHITECTURE.md`** links remain valid or are updated in the same phase."
    - "**SUMMARY** documents verification that **no** deletions occurred under **`legacy/`** or **`*_repo-copy*/`**."
    - "**`REQUIREMENTS.md`** **PRUNE-10** → **Complete** with evidence paths."
  artifacts:
    - path: ".planning/phases/33-v1-3-root-prune/33-ROOT-INVENTORY.md"
      provides: "inventory → action table"
---

<objective>
Deliver **PRUNE-10:** remove or consolidate **redundant root-only** assets (duplicate markdown, scratch notebooks/paths, obsolete docs), produce **inventory → action** with rationale, preserve **`legacy/`** and submodule mirrors untouched, keep canonical doc links working.
</objective>

**Non-goals:** Editing **`legacy/`**; editing inside **`*_repo-copy/`**; large **`src/`** docstring work (**Phase 34**).

<execution_context>
@.planning/ROADMAP.md
@.planning/REQUIREMENTS.md
@.planning/STATE.md
@.planning/phases/33-v1-3-root-prune/33-RESEARCH.md
@CLAUDE.md
@README.md
</execution_context>

<tasks>

<task type="auto" tdd="false">
  <name>33-01-01 — Build root inventory table (33-ROOT-INVENTORY.md)</name>
  <read_first>
    - `.planning/phases/33-v1-3-root-prune/33-RESEARCH.md`
    - `README.md` (first 5 lines — canonical entrypoints)
  </read_first>
  <action>
    Create **`.planning/phases/33-v1-3-root-prune/33-ROOT-INVENTORY.md`** with a markdown **table**:

    Columns: **`path`**, **`kind`** (file/dir), **`classification`** (canonical | duplicate | obsolete | scratch | keep-with-note), **`proposed_action`** (keep | merge | delete | move-to-notebooks), **`rationale`** (one sentence).

    **Scan** at minimum: all root **`*.md`**; contents of **`notebooks/`** (list names only if no duplicates); **`docs/`**; any other **root-level** non-hidden files that look like duplicate docs (exclude **`pyproject.toml`**, **`requirements*.txt`**, **`Makefile`**, **`MANIFEST.in`**, **`run_pipeline.py`**, **`LICENSE`** — never delete).

    **Explicit exclusions** (do not list for deletion): **`legacy/**`**, **`**/claude-scratch-work-repo-copy/**`**, **`**/trading-crab-lib-repo-copy/**`**, **`**/trading-crab-repo-copy/**`**, **`.planning/**`**, **`.codex/**`**.

    **Document** distinction: **`STATE.md`** (root) vs **`.planning/STATE.md`** — default **keep both** unless a true duplicate file is found.

    If no safe deletes: table may be **keep**-heavy; SUMMARY will state **“no redundant paths found”** (PRUNE-10 still satisfied by inventory + rationale).
  </action>
  <acceptance_criteria>
    - `test -f .planning/phases/33-v1-3-root-prune/33-ROOT-INVENTORY.md` exits 0
    - `grep -q "|" .planning/phases/33-v1-3-root-prune/33-ROOT-INVENTORY.md` exits 0
    - `grep -qi "rationale" .planning/phases/33-v1-3-root-prune/33-ROOT-INVENTORY.md` exits 0
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>33-01-02 — Link audit before edits</name>
  <read_first>
    - `.planning/phases/33-v1-3-root-prune/33-ROOT-INVENTORY.md`
    - `CLAUDE.md`
    - `RUNBOOK.md`
    - `ARCHITECTURE.md`
  </read_first>
  <action>
    For every path marked **merge** or **delete** in the inventory, run **`rg -n`** (or **`grep -R`**) from repo root for **basename** and **relative path** references in:
    - **`CLAUDE.md`**, **`README.md`**, **`RUNBOOK.md`**, **`ARCHITECTURE.md`**, **`docs/`**

    Append a short **“Link audit”** subsection to **`33-ROOT-INVENTORY.md`** with findings (paths to update vs safe to delete).

    Update **merge** or **delete** tasks only after links are accounted for (update doc first, then remove file).
  </action>
  <acceptance_criteria>
    - `grep -q "Link audit" .planning/phases/33-v1-3-root-prune/33-ROOT-INVENTORY.md` exits 0
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>33-01-03 — Apply merges and deletes</name>
  <read_first>
    - `.planning/phases/33-v1-3-root-prune/33-ROOT-INVENTORY.md`
  </read_first>
  <action>
    Execute **only** actions approved in the inventory **Link audit** section:

    - **Merge:** move essential content into **`README.md`**, **`CLAUDE.md`**, or **`docs/`**; then remove redundant file if applicable.
    - **Delete:** `git rm` or delete tracked files **only** under allowed roots (repo root, **`notebooks/`**, **`docs/`** as listed) — **never** under **`legacy/`** or **`*_repo-copy*/`**.

    If **no** deletes: note **“no files removed”** in working notes for SUMMARY.

    **Runtime junk** (e.g. root **`__pycache__`**, **`build/`**, **`dist/`**): prefer **`.gitignore`** + remove from working tree if accidentally committed; do not delete **`data/`** or **`outputs/`** content.
  </action>
  <acceptance_criteria>
    - After changes: `git diff --name-only HEAD 2>/dev/null; git diff --cached --name-only 2>/dev/null` — no line starts with `legacy/` and no line contains `repo-copy` (forbidden deletes)
    - If no file removals: **01-SUMMARY** states **“no files removed”** explicitly
  </acceptance_criteria>
</task>

<task type="auto" tdd="true">
  <name>33-01-04 — Regression: pytest + validate health</name>
  <read_first>
    - `pyproject.toml`
  </read_first>
  <action>
    1. Run **`pytest tests/ -q`** — must pass.

    2. Run **`node .codex/get-shit-done/bin/gsd-tools.cjs validate health`** — capture output; if **errors** unrelated to this phase, document in SUMMARY.
  </action>
  <acceptance_criteria>
    - `pytest tests/ -q` exits 0
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>33-01-05 — Traceability: REQUIREMENTS, ROADMAP, STATE, SUMMARYs</name>
  <read_first>
    - `.planning/REQUIREMENTS.md`
  </read_first>
  <action>
    1. In **`.planning/REQUIREMENTS.md`**: **PRUNE-10** → **Complete** with evidence paths (**`33-ROOT-INVENTORY.md`**, **`33-SUMMARY.md`**).

    2. **`.planning/ROADMAP.md`**: Phase **33** checkbox **\[x]** when complete.

    3. **`.planning/STATE.md`**: next phase **34**; completed phases count.

    4. Write **`33-SUMMARY.md`** and **`33-v1-3-root-prune-01-SUMMARY.md`**: As-built, plan fidelity, **forbidden-path verification** (one line: “no changes under `legacy/` or `*_repo-copy/`”).
  </action>
  <acceptance_criteria>
    - `grep -q "PRUNE-10" .planning/REQUIREMENTS.md` and line shows Complete or `[x]`
    - `grep -q "33-ROOT-INVENTORY" .planning/REQUIREMENTS.md` or evidence in `33-SUMMARY.md` cited from REQUIREMENTS
  </acceptance_criteria>
</task>

</tasks>

---

## Verification criteria (phase)

- **`33-ROOT-INVENTORY.md`** is the **PR table** for roadmap success criterion 1.
- **Link** validity for **CLAUDE / RUNBOOK / ARCHITECTURE** (criterion 2).
- **Forbidden paths** assertion in **SUMMARY** (criterion 3).

---

## PLANNING COMPLETE
