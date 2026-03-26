---
phase: 36-v1-4-root-docs-import-alignment
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - CLAUDE.md
  - README.md
  - PITFALLS.md
  - ARCHITECTURE.md
  - STATE.md
  - .planning/phases/34-v1-3-library-documentation-pass/34-VALIDATION.md
  - .planning/phases/34-v1-3-library-documentation-pass/34-VERIFICATION.md
  - .planning/REQUIREMENTS.md
autonomous: true
requirements:
  - DOC-ALIGN-10
user_setup:
  - `pip install -e ".[dev]"` from repo root for import smoke tests.
must_haves:
  truths:
    - "`grep -E 'from market_regime|market_regime\\.io' CLAUDE.md README.md` returns no matches (after edits)."
    - "`python -c \"from trading_crab_lib.checkpoints import CheckpointManager; from trading_crab_lib.config import load\"` exits 0 from repo root with dev install."
    - "`.planning/phases/34-v1-3-library-documentation-pass/34-VALIDATION.md` frontmatter has `nyquist_compliant: true`."
    - "`.planning/REQUIREMENTS.md` lists **DOC-ALIGN-10** as `[x]` with evidence; traceability row **Complete** for Phase **36**."
  artifacts:
    - path: CLAUDE.md
      provides: Root guide; package name `trading_crab_lib`; tree matches `src/trading_crab_lib/`
    - path: README.md
      provides: CheckpointManager copy-paste uses `trading_crab_lib.checkpoints`
    - path: PITFALLS.md
      provides: Code paths use `src/trading_crab_lib/`
    - path: ARCHITECTURE.md
      provides: Plotting path uses `trading_crab_lib`
    - path: STATE.md
      provides: Feature inventory paths use `src/trading_crab_lib/`
---

<objective>
Deliver **DOC-ALIGN-10**: replace stale **`market_regime`** / wrong module paths in **root onboarding docs** with **`trading_crab_lib`** and paths that match **`src/trading_crab_lib/`** (e.g. **`CheckpointManager`** in **`checkpoints.py`**, not **`io.checkpoints`**). Refresh Phase **34** validation/verification; complete **REQUIREMENTS** traceability.
</objective>

**Non-goals:** Editing **`legacy/`**; bulk-editing historical **`.planning/phases/*`** or **`.planning/research/*`** (out of scope for this phase); changing **application code** except if a doc-linked example requires it (not expected).

<execution_context>
@.planning/phases/36-v1-4-root-docs-import-alignment/36-CONTEXT.md
@.planning/v1.3-MILESTONE-AUDIT.md
@.planning/ROADMAP.md
@.planning/REQUIREMENTS.md
@src/trading_crab_lib/__init__.py
@src/trading_crab_lib/checkpoints.py
</execution_context>

<tasks>

<task type="auto" tdd="false">
  <name>36-01-01 — CLAUDE.md package name, imports, and repository tree</name>
  <read_first>
    - `CLAUDE.md` (full file)
    - `src/trading_crab_lib/__init__.py`
    - `pyproject.toml` (`[project].name`)
  </read_first>
  <action>
    1. Globally replace **installable package** references: `market_regime` → `trading_crab_lib` in import lines, fenced code, and prose where it denotes the **current** library (not historical “legacy comparison” sentences — those should say **`trading_crab_lib`** as the modular package name).

    2. Fix **wrong paths** called out by audit:
       - **`from market_regime.io.checkpoints import CheckpointManager`** → **`from trading_crab_lib.checkpoints import CheckpointManager`** (there is **no** `io.` package; see **`checkpoints.py`** at package root).

    3. Rewrite the **Repository Layout** ASCII tree (`## Repository Layout`) so the package directory is **`src/trading_crab_lib/`** and the structure matches the **actual** tree:
       - **`checkpoints.py`** at package root (not `io/checkpoints.py`).
       - **`regime.py`** — profiler helpers live here (no `regime/` subdir in current tree unless present on disk).
       - **`reporting.py`**, **`asset_returns.py`**, **`prediction/`** as in repo.
       Use `ls` / `find src/trading_crab_lib -maxdepth 2 -type f` if needed to avoid inventing files.

    4. Update **`python -c` verify** example to:  
       `python -c "from trading_crab_lib.config import load; print(load()['data'])"`

    5. Scan remainder of **CLAUDE.md** for `src/market_regime` and replace with **`src/trading_crab_lib`**.
  </action>
  <acceptance_criteria>
    - `! grep -E 'from market_regime|market_regime\\.io|src/market_regime' CLAUDE.md` (exit 1 = no matches). Use `grep -E` ; if **zero** lines is required: `grep -E 'market_regime' CLAUDE.md` returns exit **1**.
    - `grep -q 'trading_crab_lib.checkpoints import CheckpointManager' CLAUDE.md` OR `grep -q 'trading_crab_lib import' CLAUDE.md` for the list-checkpoints story.
    - `grep -q 'src/trading_crab_lib' CLAUDE.md` in the repository layout section.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>36-01-02 — README.md checkpoint snippet</name>
  <read_first>
    - `README.md` (section “To list all available `market_code` checkpoints”)
    - `src/trading_crab_lib/checkpoints.py` (module docstring import line)
  </read_first>
  <action>
    Replace the fenced Python block so it uses:
    `from trading_crab_lib.checkpoints import CheckpointManager`
    (not `market_regime.io.checkpoints`). Keep behavior identical (list `market_code_*` entries).
  </action>
  <acceptance_criteria>
    - `! grep -E 'market_regime' README.md` (no matches).
    - `grep -q 'trading_crab_lib.checkpoints import CheckpointManager' README.md`.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>36-01-03 — PITFALLS.md, ARCHITECTURE.md, STATE.md path strings</name>
  <read_first>
    - `PITFALLS.md`
    - `ARCHITECTURE.md`
    - `STATE.md`
  </read_first>
  <action>
    Replace **`src/market_regime/`** with **`src/trading_crab_lib/`** everywhere in these three files. If a path references a file that moved (e.g. portfolio helpers), align to the actual module under **`trading_crab_lib`** (e.g. **`reporting.py`**) — verify with `grep -r portfolio src/trading_crab_lib` if needed.
  </action>
  <acceptance_criteria>
    - `! grep -q 'src/market_regime' PITFALLS.md ARCHITECTURE.md STATE.md` (grep exits 1).
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>36-01-04 — Phase 34 VALIDATION / VERIFICATION + quality bar</name>
  <read_first>
    - `.planning/phases/34-v1-3-library-documentation-pass/34-VALIDATION.md`
    - `.planning/phases/34-v1-3-library-documentation-pass/34-VERIFICATION.md`
  </read_first>
  <action>
    1. Set **`nyquist_compliant: true`** in **`34-VALIDATION.md`** frontmatter (doc-alignment + refreshed verification complete the Nyquist story for Phase 34).

    2. Run **`make lint`** (or **`bash scripts/lint.sh`**) and **`pytest tests/ -q`** from repo root; append or replace the **Actual output** / metrics subsection in **`34-VERIFICATION.md`** with current pass/skip counts and date.

    3. If **`34-VERIFICATION.md`** references stale **`market_regime`** in command logs only, leave logs as historical **or** add a one-line note that doc imports are now **`trading_crab_lib`** (minimal edit).
  </action>
  <acceptance_criteria>
    - `grep -q '^nyquist_compliant: true' .planning/phases/34-v1-3-library-documentation-pass/34-VALIDATION.md`.
    - `34-VERIFICATION.md` contains updated pytest (or lint) counts dated 2026-03 or later execute date.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>36-01-05 — REQUIREMENTS, phase summaries, health</name>
  <read_first>
    - `.planning/REQUIREMENTS.md`
    - `.planning/phases/35-v1-4-phase-28-verification-parity/35-SUMMARY.md` (tone reference)
  </read_first>
  <action>
    1. **REQUIREMENTS.md:** Mark **DOC-ALIGN-10** **`[x]`**; evidence: **`36-SUMMARY.md`**, **`CLAUDE.md`**, **`README.md`**; traceability **Complete** / Phase **36**.

    2. Write **`36-SUMMARY.md`** (execution summary: what changed, verification commands).

    3. Write **`36-v1-4-root-docs-import-alignment-01-SUMMARY.md`** (hybrid As-built / Plan fidelity / Delta) beside **`01-PLAN.md`** for **I001** parity.

    4. Run **`node .codex/get-shit-done/bin/gsd-tools.cjs validate health`** — expect **`"status": "healthy"`**, **`"info": []`**.
  </action>
  <acceptance_criteria>
    - `grep -q '\[x\] \*\*DOC-ALIGN-10' .planning/REQUIREMENTS.md`.
    - `test -f .planning/phases/36-v1-4-root-docs-import-alignment/36-SUMMARY.md`.
    - `test -f .planning/phases/36-v1-4-root-docs-import-alignment/36-v1-4-root-docs-import-alignment-01-SUMMARY.md`.
    - `node .codex/get-shit-done/bin/gsd-tools.cjs validate health 2>&1 | grep -q '"status": "healthy"'`.
  </acceptance_criteria>
</task>

</tasks>

## Success criteria (roadmap)

1. No misleading **`from market_regime`** / **`market_regime.io`** in **README** / **CLAUDE** (grep spot-check).
2. Import smoke passes with **`pip install -e ".[dev]"`**.
3. **34-VALIDATION** / **34-VERIFICATION** updated.
4. **DOC-ALIGN-10** → **Complete** in **REQUIREMENTS.md**.

## Risks

| Risk | Mitigation |
|------|------------|
| Over-editing legacy narrative | Touch only listed root files + Phase 34 planning artifacts |
| Tree drift vs future refactors | Executor re-lists `src/trading_crab_lib` before finalizing CLAUDE tree |

## PLANNING COMPLETE

**Requirement coverage:** **DOC-ALIGN-10** in frontmatter `requirements` and in task outcomes.
