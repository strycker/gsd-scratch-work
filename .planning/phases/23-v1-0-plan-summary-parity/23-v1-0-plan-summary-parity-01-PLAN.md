---
phase: 23-v1-0-plan-summary-parity
plan: 01
type: execute
wave: 1
depends_on:
  - 22-v1-2-providers-universe
files_modified:
  - .planning/phases/06-weekly-report-pipeline/06-weekly-report-pipeline-01-SUMMARY.md
  - .planning/phases/08-data-signals-diagnostics/08-data-signals-diagnostics-01-SUMMARY.md
  - .planning/phases/12-v1-audit-verify-phases-4-6/12-v1-audit-verify-phases-4-6-01-SUMMARY.md
  - .planning/phases/13-v1-audit-verify-phases-7-11/13-v1-audit-verify-phases-7-11-01-SUMMARY.md
  - .planning/phases/15-v1-gap-regime-profiles-names/15-v1-gap-regime-profiles-names-01-SUMMARY.md
  - .planning/phases/16-v1-gap-e2e-integration-runbook/16-v1-gap-e2e-integration-runbook-01-SUMMARY.md
  - .planning/phases/23-v1-0-plan-summary-parity/23-v1-0-plan-summary-parity-01-SUMMARY.md
  - .planning/REQUIREMENTS.md
  - .planning/ROADMAP.md
  - .planning/phases/23-v1-0-plan-summary-parity/23-SUMMARY.md
  - .planning/phases/23-v1-0-plan-summary-parity/23-VALIDATION.md
  - .planning/phases/23-v1-0-plan-summary-parity/README.md
autonomous: true
requirements:
  - CLOSURE-01
user_setup:
  - None
must_haves:
  truths:
    - "Six per-plan SUMMARY files exist (or pointer stubs) matching the CLOSURE-01 plan basenames."
    - "`gsd-tools validate health` reports no I001 for those plan paths, or 23-SUMMARY documents the accepted exception."
    - "REQUIREMENTS.md marks CLOSURE-01 complete with pointer to 23-SUMMARY.md."
  artifacts:
    - path: ".planning/phases/*/*-01-SUMMARY.md"
      provides: "plan–summary basename parity for CLOSURE-01 list"
---

<objective>
Close **CLOSURE-01**: add **`*-SUMMARY.md`** files aligned with each plan in the **known I001 gap list** (same basename as `*-PLAN.md`, replacing `PLAN` with `SUMMARY`), satisfy **`validate health`** expectations, and update **REQUIREMENTS** traceability — **no product code** unless a summary uncovers a documentation fix.
</objective>

**Non-goals:** `03-supervised-regime-behavior-models-04-PLAN.md` (Phase **25**). New feature work.

<execution_context>
@.planning/phases/23-v1-0-plan-summary-parity/23-CONTEXT.md
@.planning/REQUIREMENTS.md
@.planning/ROADMAP.md
</execution_context>

<context>
**CLOSURE-01 plan files (create matching `*-SUMMARY.md` in the same directory):**

| # | Plan file |
|---|-----------|
| 1 | `06-weekly-report-pipeline/06-weekly-report-pipeline-01-PLAN.md` |
| 2 | `08-data-signals-diagnostics/08-data-signals-diagnostics-01-PLAN.md` |
| 3 | `12-v1-audit-verify-phases-4-6/12-v1-audit-verify-phases-4-6-01-PLAN.md` |
| 4 | `13-v1-audit-verify-phases-7-11/13-v1-audit-verify-phases-7-11-01-PLAN.md` |
| 5 | `15-v1-gap-regime-profiles-names/15-v1-gap-regime-profiles-names-01-PLAN.md` |
| 6 | `16-v1-gap-e2e-integration-runbook/16-v1-gap-e2e-integration-runbook-01-PLAN.md` |

**Regression / verification:**  
`node .codex/get-shit-done/bin/gsd-tools.cjs validate health` (or project’s documented health command) after adding summaries.

**Stub pattern (when phase-level `NN-SUMMARY.md` is canonical):** 5–15 lines — link to plan, link to `NN-SUMMARY.md`, one paragraph on outcomes + verification pointer.
</context>

<tasks>

<task type="auto" tdd="false">
  <name>Task 1 — Summaries for phases 06, 08, 12, 13, 15</name>
  <read_first>
    - Each directory’s `*-01-PLAN.md` and any existing `NN-SUMMARY.md` / `*-VERIFICATION.md`
  </read_first>
  <action>
    For each path in rows 1–5 of the table above, create **`{basename}-SUMMARY.md`** next to the plan (e.g. `06-weekly-report-pipeline-01-SUMMARY.md`). Include: execution date (approximate OK), what shipped vs plan objectives, pointers to scripts/pipelines/outputs/tests, and link to phase-level `NN-SUMMARY.md` if it exists and is richer.
  </action>
  <acceptance_criteria>
    - Five new files exist with correct basenames.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 2 — Summary for phase 16 (pointer or full)</name>
  <read_first>
    - `16-v1-gap-e2e-integration-runbook/16-SUMMARY.md`
    - `16-v1-gap-e2e-integration-runbook-01-PLAN.md`
  </read_first>
  <action>
    Add **`16-v1-gap-e2e-integration-runbook-01-SUMMARY.md`**. If **`16-SUMMARY.md`** remains the canonical narrative, use a short stub that links to it and lists verification artifacts (`*-VERIFICATION.md`, RUNBOOK, smoke commands).
  </action>
  <acceptance_criteria>
    - Sixth SUMMARY file exists; no contradiction with `16-SUMMARY.md`.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 3 — Health check + REQUIREMENTS</name>
  <read_first>
    - `.codex/get-shit-done/workflows/health.md` (I001)
  </read_first>
  <action>
    1. Run **`gsd-tools validate health`** from repo root; confirm **I001** cleared for the six plan paths (or document why not, in `23-SUMMARY.md`).
    2. Update **`.planning/REQUIREMENTS.md`**: mark **CLOSURE-01** complete; refresh traceability table row for Phase 23.
    3. Update **`.planning/ROADMAP.md`**: Phase 23 checklist + progress row when execute completes.
  </action>
  <acceptance_criteria>
    - `validate health` clean for I001 on target paths **or** documented waiver in `23-SUMMARY.md`.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 4 — Phase 23 evidence</name>
  <action>
    Write **`23-SUMMARY.md`** (execution narrative + commands run). Update **`23-VALIDATION.md`** (Nyquist: manual doc review + health command). Update phase **`README.md`** with links.
  </action>
  <acceptance_criteria>
    - `23-SUMMARY.md` exists post-execute.
  </acceptance_criteria>
</task>

</tasks>

## Verification checklist (pre-merge)

- [ ] Six `*-01-SUMMARY.md` files present beside their plans
- [ ] `node .codex/get-shit-done/bin/gsd-tools.cjs validate health` (adjust if CLI differs)
- [ ] `CLOSURE-01` checked in REQUIREMENTS.md

## Plan metadata

| Field | Value |
|-------|-------|
| Roadmap | Phase 23 — v1.0 plan ↔ summary parity |
| Nyquist | Mostly manual / tooling; see `23-VALIDATION.md` |
