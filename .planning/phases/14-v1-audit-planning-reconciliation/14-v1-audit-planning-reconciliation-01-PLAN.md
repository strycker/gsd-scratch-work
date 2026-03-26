---
phase: 14-v1-audit-planning-reconciliation
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - .planning/ROADMAP.md
  - .planning/REQUIREMENTS.md
  - .planning/STATE.md
  - .planning/phases/01-data-and-constraints-foundations/01-data-and-constraints-foundations-VERIFICATION.md
  - .planning/phases/02-regime-clustering-interpretation/02-regime-clustering-interpretation-VERIFICATION.md
  - .planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-VERIFICATION.md
  - .planning/phases/14-v1-audit-planning-reconciliation/14-SUMMARY.md
autonomous: true
requirements: []
user_setup: []
must_haves:
  truths:
    - "ROADMAP completion language and Phase 1 plan list match .planning/REQUIREMENTS.md traceability (or REQUIREMENTS edited with explicit rationale where intentional divergence remains)."
    - ".planning/STATE.md frontmatter and narrative reflect Phase 14 as current focus, v1.0 milestone, and non-stale phase/plan counts vs ROADMAP Progress table."
    - "Phase 1 detail block in ROADMAP no longer lists Phase 3 plan filenames under Phase 1; it lists Phase 1 (01-data-and-constraints-foundations) plans or honest TBD."
    - "Bodies of 01-data-and-constraints-foundations, 02, and 03 *-VERIFICATION.md cite src/trading_crab_lib/ paths and trading_crab_lib import paths where they previously said market_regime."
    - "Phase 2 VERIFICATION explains why status gaps_found coexists with 02-VALIDATION.md nyquist_compliant true (different lenses: product gaps vs test-contract freshness)."
  artifacts:
    - path: ".planning/phases/14-v1-audit-planning-reconciliation/14-SUMMARY.md"
      provides: "Short record of edits and any remaining intentional doc debt"
      min_lines: 15
---

<objective>
Close **Phase 14: v1.0 Audit — Planning source reconciliation** with documentation-only edits: align ROADMAP, REQUIREMENTS, and STATE; fix misplaced Phase 1 plan references; refresh early-phase VERIFICATION bodies for the `trading_crab_lib` package layout; reconcile Phase 2 **VERIFICATION** (`gaps_found`) vs **VALIDATION** (`nyquist_compliant: true`) narratives. No production code changes unless a typo in docs must mirror code (unlikely).
</objective>

<execution_context>
@.planning/phases/14-v1-audit-planning-reconciliation/14-CONTEXT.md
@.planning/v1.0-MILESTONE-AUDIT.md
@.planning/ROADMAP.md
@.planning/REQUIREMENTS.md
@.planning/STATE.md
@.planning/phases/02-regime-clustering-interpretation/02-VALIDATION.md
@.planning/phases/02-regime-clustering-interpretation/02-regime-clustering-interpretation-VERIFICATION.md
@CLAUDE.md
</execution_context>

<context>
**Package layout (executor must confirm with `ls src/trading_crab_lib`):** Library lives under `src/trading_crab_lib/` with top-level modules `checkpoints.py`, `clustering.py`, `regime.py`, `transforms.py`, `prediction.py`, and package `prediction/` with `classifier.py`. Replace legacy `src/market_regime/` and `market_regime.*` references in verification docs accordingly.

**Phase 2 nuance:** `02-regime-clustering-interpretation-VERIFICATION.md` frontmatter `status: gaps_found` reflects *product* gaps (e.g. ETF rows in profiles, pinned names). `02-VALIDATION.md` frontmatter `nyquist_compliant: true` reflects *test/validation contract* status. Add a short subsection under Phase 2 VERIFICATION (or frontmatter-adjacent prose) so readers do not treat these as contradictory.

**ROADMAP hygiene:** Under "### Phase 1" details, the nested `Plans:` list must not point at `03-supervised-regime-behavior-models-*` files; correct targets are `.planning/phases/01-data-and-constraints-foundations/01-data-and-constraints-foundations-01-PLAN.md`, `01-data-and-constraints-foundations-02-PLAN.md`, `01-data-and-constraints-foundations-03-PLAN.md` with accurate checkmarks vs `.planning/ROADMAP.md` Progress table.
</context>

<tasks>

<task type="auto" tdd="false">
  <name>Task 1 — ROADMAP Phase 1 plan list + global consistency scan</name>
  <read_first>
    - .planning/ROADMAP.md
    - .planning/REQUIREMENTS.md (Traceability table)
    - .planning/phases/01-data-and-constraints-foundations/01-data-and-constraints-foundations-01-PLAN.md
    - .planning/phases/01-data-and-constraints-foundations/01-data-and-constraints-foundations-02-PLAN.md
    - .planning/phases/01-data-and-constraints-foundations/01-data-and-constraints-foundations-03-PLAN.md
  </read_first>
  <action>
    1. In **ROADMAP.md**, under `### Phase 1: Data & Constraints Foundations`, replace the `Plans:` bullets that reference `03-supervised-regime-behavior-models-*` with the three `01-data-and-constraints-foundations-0*-PLAN.md` filenames (paths relative to `.planning/phases/01-data-and-constraints-foundations/` or full repo-relative paths — match the style used for Phase 12/13 plan lists). Set `[x]` / `[ ]` per whether those plans are actually complete (infer from ROADMAP Progress row "Phase 1 | 2/3" and plan SUMMARY files if needed).
    2. Scan ROADMAP top-level checkboxes (`- [ ] **Phase 1**` vs `- [x] **Phase 2**` …) and Progress table **Status** column; align Phase 1 checkbox and any "Complete" language with REQUIREMENTS rows DATA-01..03 and CONSTR-01..02 all **Complete** (either mark Phase 1 complete in ROADMAP or add a one-line NOTE in ROADMAP if Phase 1 is intentionally still open — must not silently contradict the traceability table without explanation).
  </action>
  <acceptance_criteria>
    - `grep -n "03-supervised-regime-behavior-models" .planning/ROADMAP.md` returns no matches inside the `### Phase 1` section (lines from `### Phase 1:` through the line before `### Phase 2:`).
    - `.planning/ROADMAP.md` contains literal substring `01-data-and-constraints-foundations-01-PLAN.md` at least once in the Phase 1 details block.
    - If Phase 1 remains `- [ ]` at the top of ROADMAP, the Phase 1 details block includes an explicit sentence explaining why (e.g. one remaining plan incomplete); otherwise top checkbox matches Progress table.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 2 — REQUIREMENTS traceability vs ROADMAP wording</name>
  <read_first>
    - .planning/REQUIREMENTS.md
    - .planning/ROADMAP.md
  </read_first>
  <action>
    Verify each requirement ID in the Traceability table (DATA-01 through CORE-02) has a matching story in ROADMAP: phases marked complete in ROADMAP should not pair with **Pending** in REQUIREMENTS without a footnote. If everything through Phase 13 is shipped, ensure no row still says Pending unless intentional; if Pending remains, add a `> **Note:**` block under Traceability explaining the exception, or update the row to Complete with evidence pointer (existing VERIFICATION path).
  </action>
  <acceptance_criteria>
    - `grep "| Pending |" .planning/REQUIREMENTS.md` inside the Traceability table: either **zero matches** or each Pending row is cited in the same Requirements file with a one-line rationale within 20 lines of the table.
    - `.planning/REQUIREMENTS.md` Traceability table still lists all IDs from DATA-01 through CORE-02 with no duplicate Requirement column entries.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 3 — Refresh .planning/STATE.md</name>
  <read_first>
    - .planning/STATE.md
    - .planning/ROADMAP.md (Progress table at bottom)
  </read_first>
  <action>
    Update YAML frontmatter: `current_phase: 14`, sensible `status` (e.g. `planning` or `in_progress`), `last_updated` to execution date (ISO-8601), `progress.total_phases` and `completed_phases` consistent with how many roadmap phases exist and which are marked complete in ROADMAP (count from Progress table). Replace narrative bullets that still say "Current Phase: 03" or "11 phases complete; next 12–15" with text matching ROADMAP reality: Phases 12–13 audit closure done, Phase 14 in progress, Phase 1 status aligned with ROADMAP after Task 1.
  </action>
  <acceptance_criteria>
    - `.planning/STATE.md` contains `current_phase: 14` (or `current_phase: "14"` if YAML quoted — consistent with file style).
    - `grep "Current Phase: 03" .planning/STATE.md` returns no matches.
    - `.planning/STATE.md` mentions Phase 14 or "planning reconciliation" in the Current Position / milestone narrative.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 4 — VERIFICATION path renames (phases 01–03)</name>
  <read_first>
    - .planning/phases/01-data-and-constraints-foundations/01-data-and-constraints-foundations-VERIFICATION.md
    - .planning/phases/02-regime-clustering-interpretation/02-regime-clustering-interpretation-VERIFICATION.md
    - .planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-VERIFICATION.md
    - List actual files: run `ls src/trading_crab_lib`; confirm legacy tree is absent (`test ! -d src/market_regime`).
  </read_first>
  <action>
    In each of the three VERIFICATION files:
    - Replace every `src/market_regime/` path with the correct `src/trading_crab_lib/` path (including subpaths: `ingestion/`, `prediction/classifier.py`, top-level `regime.py`, `clustering.py`, etc.).
    - Replace prose/import references `market_regime.` with `trading_crab_lib.` where they refer to the installable package (keep the word "market_regime" only if it refers to a conceptual label, not the Python package).
    - For Phase 02, tables that say `src/market_regime/regime.py` must become `src/trading_crab_lib/regime.py` (single module file, not a directory — verify on disk).
  </action>
  <acceptance_criteria>
    - `grep -r "src/market_regime" .planning/phases/01-data-and-constraints-foundations/01-data-and-constraints-foundations-VERIFICATION.md .planning/phases/02-regime-clustering-interpretation/02-regime-clustering-interpretation-VERIFICATION.md .planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-VERIFICATION.md` exits 1 (no matches).
    - `grep -n "trading_crab_lib" .planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-VERIFICATION.md | head -5` prints at least one line (file demonstrates new package name).
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 5 — Phase 2 VERIFICATION vs VALIDATION narrative</name>
  <read_first>
    - .planning/phases/02-regime-clustering-interpretation/02-regime-clustering-interpretation-VERIFICATION.md
    - .planning/phases/02-regime-clustering-interpretation/02-VALIDATION.md
  </read_first>
  <action>
    Add a subsection **## Notes: VERIFICATION vs VALIDATION`** (or equivalent) near the top of `02-regime-clustering-interpretation-VERIFICATION.md` after frontmatter: 3–6 bullets stating (1) VERIFICATION `gaps_found` = roadmap truth table / product evidence gaps; (2) VALIDATION `nyquist_compliant: true` = automated test contract per `02-VALIDATION.md`; (3) point readers to both files. Optionally add one sentence in `02-VALIDATION.md` header pointing back to VERIFICATION for requirement-level status — only if it avoids circular confusion.
  </action>
  <acceptance_criteria>
    - `.planning/phases/02-regime-clustering-interpretation/02-regime-clustering-interpretation-VERIFICATION.md` contains literal heading `## Notes: VERIFICATION vs VALIDATION` (exact string).
    - Same file contains both substrings `gaps_found` and `nyquist` in the new section body.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 6 — Phase 14 summary artifact</name>
  <read_first>
    - .planning/phases/14-v1-audit-planning-reconciliation/14-CONTEXT.md
  </read_first>
  <action>
    Create `.planning/phases/14-v1-audit-planning-reconciliation/14-SUMMARY.md` listing files touched, any intentional remaining doc debt, and confirmation that success criteria from ROADMAP Phase 14 are met.
  </action>
  <acceptance_criteria>
    - `test -f .planning/phases/14-v1-audit-planning-reconciliation/14-SUMMARY.md` is true.
    - File contains markdown heading `# Phase 14 Summary` as first line after optional frontmatter, and lists at least three bullet points under a `## Changes` section.
  </acceptance_criteria>
</task>

</tasks>

<verification_criteria>
- All six task acceptance_criteria blocks satisfied (run listed grep/test commands).
- No accidental edits under `legacy/` or `src/` unless a doc explicitly required a code citation fix (Phase 14 default: docs only).
- Optional: `git diff --stat .planning/` shows only expected paths.
</verification_criteria>

## PLANNING COMPLETE
