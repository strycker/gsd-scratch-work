---
phase: 29-v1-3-submodule-comparison-matrix
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - .planning/research/SUBMODULE_COMPARISON_MATRIX.md
  - .planning/phases/29-v1-3-submodule-comparison-matrix/29-v1-3-submodule-comparison-matrix-01-SUMMARY.md
  - .planning/phases/29-v1-3-submodule-comparison-matrix/29-SUMMARY.md
  - .planning/phases/29-v1-3-submodule-comparison-matrix/29-VALIDATION.md
  - .planning/REQUIREMENTS.md
  - .planning/STATE.md
autonomous: true
requirements:
  - SYNC-10
user_setup:
  - Optional — `git submodule update --init --recursive` to refresh mirrors before inventory (read-only thereafter).
must_haves:
  truths:
    - "`.planning/research/SUBMODULE_COMPARISON_MATRIX.md` exists and is cited from `29-SUMMARY.md`."
    - "Artifact documents canonical root + all three submodule paths from `.gitmodules` with comparison tables for layout, library package, modules-by-area, tests, config, planning."
    - "Artifact includes explicit merge order (lib mirror → claude-scratch → trading-crab) and read-only / no-edit constraint for submodule trees."
    - "`REQUIREMENTS.md` SYNC-10 marked complete after execute with pointer to `29-SUMMARY.md`."
  artifacts:
    - path: ".planning/research/SUBMODULE_COMPARISON_MATRIX.md"
      provides: "single authoritative SYNC-10 comparison for Phase 30"
---

<objective>
Deliver **SYNC-10**: one **markdown comparison matrix** under **`.planning/research/SUBMODULE_COMPARISON_MATRIX.md`**, mapping **canonical root** vs **`trading-crab-lib-repo-copy`**, **`claude-scratch-work-repo-copy`**, and **`trading-crab-repo-copy`** — **read-only** inspection only (see **29-CONTEXT.md**).
</objective>

**Non-goals:** Editing code inside mirrors or `legacy/`; unification batches (**Phase 30**).

<execution_context>
@.planning/phases/29-v1-3-submodule-comparison-matrix/29-CONTEXT.md
@.planning/phases/29-v1-3-submodule-comparison-matrix/29-RESEARCH.md
@.planning/REQUIREMENTS.md
@.planning/ROADMAP.md
@.planning/research/FEATURES.md
@.gitmodules
</execution_context>

<tasks>

<task type="auto" tdd="false">
  <name>29-01-01 — Preflight inventory commands</name>
  <read_first>
    - `.gitmodules`
    - `.planning/research/FEATURES.md` (comparison dimensions)
    - `pyproject.toml` (root package name / `src` layout)
  </read_first>
  <action>
    From **repository root**, for **each** of: `.` (canonical), `trading-crab-lib-repo-copy/`, `claude-scratch-work-repo-copy/`, `trading-crab-repo-copy/`:

    1. Record whether **`src/`** exists and the **Python package dir name** under `src/` (e.g. `trading_crab_lib`) — use `ls` / `find src -maxdepth 2 -type d` as needed.
    2. Record **`pyproject.toml`** / **`setup.cfg`** presence and **`[project].name`** (or equivalent) if present.
    3. Count `*.py` files: `find <path> -name '*.py' -not -path '*/\.*' 2>/dev/null | wc -l` (document counts in the matrix appendix).
    4. Note **nested** foreign roots (e.g. `*/gsd-scratch-work-repo-copy/*`) if observed — single **“Layout caveats”** subsection.

    Do **not** modify any file under the three `*_repo-copy/` directories.
  </action>
  <acceptance_criteria>
    - Phase **29-SUMMARY.md** (written in task 29-01-03) lists **four** inventory targets and includes **at least one** numeric **`.py` count** line per target **or** explains `find` failure (empty submodule) verbatim.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>29-01-02 — Write SUBMODULE_COMPARISON_MATRIX.md</name>
  <read_first>
    - `.planning/phases/29-v1-3-submodule-comparison-matrix/29-CONTEXT.md`
    - `.planning/research/FEATURES.md`
  </read_first>
  <action>
    Create **`.planning/research/SUBMODULE_COMPARISON_MATRIX.md`** with **exact** top-level sections:

    1. `# Submodule comparison matrix (v1.3 — SYNC-10)`  
    2. `## Operational constraint` — paragraph containing **both** substrings: **`do not edit`** and **`read-only`** (case-insensitive OK) and naming the three mirror directories.  
    3. `## Repository inventory` — table: columns **Root**, **trading-crab-lib-repo-copy**, **claude-scratch-work-repo-copy**, **trading-crab-repo-copy**; rows at minimum: **Has `src/`**, **Package name under `src/`**, **`pyproject` project name**, **Approx `.py` file count** (from 29-01-01).  
    4. `## Module areas` — table or bullet grid covering **ingestion**, **feature/transforms**, **clustering / regime**, **prediction**, **reporting / diagnostics / tactics**, **assets** — mark **Present / Absent / Unknown** per repo (use findings from tree / `find` / prior knowledge from FEATURES).  
    5. `## Tests` — per repo: **test directory paths** (`tests/`, `tests/unit/`, etc.) and **approx test file count** or **“none found”**.  
    6. `## Config and entrypoints` — `config/`, `run_pipeline.py`, `pipelines/` presence per repo.  
    7. `## Planning and docs` — `.planning/` or equivalent; key markdown (`README`, `CLAUDE.md`) per repo.  
    8. `## Merge order (locked for Phase 30+)` — numbered list: **(1)** `trading-crab-lib-repo-copy` **(2)** `claude-scratch-work-repo-copy` **(3)** `trading-crab-repo-copy`, each with **one-line** dependency/risk note.  
    9. `## Notable deltas and follow-ups` — 3–10 bullets for Phase **30** consumption.
  </action>
  <acceptance_criteria>
    - `test -f .planning/research/SUBMODULE_COMPARISON_MATRIX.md` exits 0
    - `grep -qi 'do not edit' .planning/research/SUBMODULE_COMPARISON_MATRIX.md` exits 0
    - `grep -qi 'read-only' .planning/research/SUBMODULE_COMPARISON_MATRIX.md` exits 0
    - `grep -q 'trading-crab-lib-repo-copy' .planning/research/SUBMODULE_COMPARISON_MATRIX.md` exits 0
    - `grep -q 'claude-scratch-work-repo-copy' .planning/research/SUBMODULE_COMPARISON_MATRIX.md` exits 0
    - `grep -q 'trading-crab-repo-copy' .planning/research/SUBMODULE_COMPARISON_MATRIX.md` exits 0
    - `grep -qi 'Merge order' .planning/research/SUBMODULE_COMPARISON_MATRIX.md` exits 0
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>29-01-03 — Evidence, REQUIREMENTS trace, validation sign-off</name>
  <read_first>
    - `.planning/REQUIREMENTS.md` (SYNC-10 row)
    - `.planning/ROADMAP.md` (Phase 29 checklist)
    - `.planning/research/SUBMODULE_COMPARISON_MATRIX.md`
  </read_first>
  <action>
    1. Write **`.planning/phases/29-v1-3-submodule-comparison-matrix/29-SUMMARY.md`**: execution date, pointer to **`SUBMODULE_COMPARISON_MATRIX.md`**, inventory commands run, `git submodule status` output excerpt (optional).
    2. Update **`.planning/REQUIREMENTS.md`**: mark **SYNC-10** checkbox `[x]`; traceability table **SYNC-10** → **Complete** with pointer to **`29-SUMMARY.md`**.
    3. Update **`.planning/ROADMAP.md`**: Phase **29** checklist from `- [ ]` to `- [x]`.
    4. Update **`.planning/phases/29-v1-3-submodule-comparison-matrix/29-VALIDATION.md`**: `nyquist_compliant: true`, `status: approved`, approval line with date.
    5. Update **`.planning/STATE.md`**: next action **`$gsd-plan-phase 30`** (or execute 30 after plan); reflect Phase **29** complete in narrative.
  </action>
  <acceptance_criteria>
    - `test -f .planning/phases/29-v1-3-submodule-comparison-matrix/29-SUMMARY.md` exits 0
    - `grep -q 'SUBMODULE_COMPARISON_MATRIX.md' .planning/phases/29-v1-3-submodule-comparison-matrix/29-SUMMARY.md` exits 0
    - `grep -q '- [x] \\*\\*SYNC-10\\*\\*' .planning/REQUIREMENTS.md || grep -q '- [x] **SYNC-10**' .planning/REQUIREMENTS.md` — exit 0 (either pattern)
    - `grep -q 'SYNC-10 | 29 | Complete' .planning/REQUIREMENTS.md` exits 0
    - `grep -q '- [x] \\*\\*Phase 29:' .planning/ROADMAP.md || grep -q '- [x] **Phase 29:' .planning/ROADMAP.md` exits 0
  </acceptance_criteria>
</task>

</tasks>

## Plan metadata

| Field | Value |
|-------|-------|
| Roadmap | Phase 29 — SYNC-10 |
| Primary artifact | `.planning/research/SUBMODULE_COMPARISON_MATRIX.md` |

## PLANNING COMPLETE
</think>


<｜tool▁calls▁begin｜><｜tool▁call▁begin｜>
StrReplace