---
phase: 24-v1-0-brownfield-phase-readmes
plan: 01
type: execute
wave: 1
depends_on:
  - 23-v1-0-plan-summary-parity
files_modified:
  - .planning/phases/04-regime-conditional-etf-portfolio-behavior/README.md
  - .planning/phases/05-recommendations-machine-readable-outputs/README.md
  - .planning/phases/06-weekly-report-pipeline/README.md
  - .planning/phases/07-portfolio-and-email-integration/README.md
  - .planning/phases/08-data-signals-diagnostics/README.md
  - .planning/phases/09-tactics-and-diagnostics/README.md
  - .planning/phases/10-tactics-install/README.md
  - .planning/phases/11-core-cleanup/README.md
  - .planning/REQUIREMENTS.md
  - .planning/ROADMAP.md
  - .planning/phases/24-v1-0-brownfield-phase-readmes/24-SUMMARY.md
  - .planning/phases/24-v1-0-brownfield-phase-readmes/README.md
autonomous: true
requirements:
  - CLOSURE-02
user_setup:
  - None
must_haves:
  truths:
    - "Eight brownfield phase directories (04,05,06,07,08,09,10,11) each contain README.md linking VERIFICATION, VALIDATION, and RUNBOOK or run_pipeline."
    - "REQUIREMENTS.md marks CLOSURE-02 complete; ROADMAP Phase 24 progress reflects completion."
  artifacts:
    - path: ".planning/phases/*/README.md"
      provides: "discoverable v1.0 evidence index per CLOSURE-02"
---

<objective>
Close **CLOSURE-02**: add a short **`README.md`** in each of **`.planning/phases/`** directories **04–11** (eight dirs) so shipped v1.0 work is discoverable without historical `*-PLAN.md`. Each file points to that phase’s **`*-VERIFICATION.md`**, **`NN-VALIDATION.md`**, and primary ops entrypoints (**`RUNBOOK.md`** at repo root and/or **`run_pipeline.py`** / **`scripts/`** as appropriate per existing VERIFICATION text).
</objective>

**Non-goals:** Product code changes; **CLOSURE-03** (Phase 25).

<execution_context>
@.planning/phases/24-v1-0-brownfield-phase-readmes/24-CONTEXT.md
@.planning/REQUIREMENTS.md
@.planning/ROADMAP.md
</execution_context>

## Tasks

<task type="auto" tdd="false">
  <name>Task 1 — README: phases 04 and 05</name>
  <read_first>
    - `.planning/phases/04-regime-conditional-etf-portfolio-behavior/04-regime-conditional-etf-portfolio-behavior-VERIFICATION.md`
    - `.planning/phases/04-regime-conditional-etf-portfolio-behavior/04-VALIDATION.md`
    - `.planning/phases/05-recommendations-machine-readable-outputs/05-recommendations-machine-readable-outputs-VERIFICATION.md`
    - `.planning/phases/05-recommendations-machine-readable-outputs/05-VALIDATION.md`
    - `RUNBOOK.md` (repo root, first 80 lines sufficient for linking)
  </read_first>
  <action>
    Create **`.planning/phases/04-regime-conditional-etf-portfolio-behavior/README.md`** with:
    - H1 title including "Phase 4" and portfolio/regime behavior theme.
    - One paragraph stating v1.0 work is **shipped**; this folder is a **brownfield** GSD anchor (no historical `*-PLAN.md` for the original delivery).
    - Bullets with **relative** markdown links: `./04-regime-conditional-etf-portfolio-behavior-VERIFICATION.md`, `./04-VALIDATION.md`.
    - Bullets citing **at least two** of: `run_pipeline.py`, `pipelines/06_asset_returns.py`, `pipelines/07_dashboard.py` (use backticks, paths as in VERIFICATION).
    - Line `RUNBOOK.md` (repo root) mentioned once as operational context.

    Create **`.planning/phases/05-recommendations-machine-readable-outputs/README.md`** with the same structure, using `./05-recommendations-machine-readable-outputs-VERIFICATION.md`, `./05-VALIDATION.md`, and entrypoints from the 05 VERIFICATION (e.g. `outputs/reports/`, dashboard paths — copy exact strings from VERIFICATION).
  </action>
  <acceptance_criteria>
    - `test -f .planning/phases/04-regime-conditional-etf-portfolio-behavior/README.md` exits 0.
    - `grep -F "04-regime-conditional-etf-portfolio-behavior-VERIFICATION.md" .planning/phases/04-regime-conditional-etf-portfolio-behavior/README.md` exits 0.
    - `grep -F "04-VALIDATION.md" .planning/phases/04-regime-conditional-etf-portfolio-behavior/README.md` exits 0.
    - `grep -E 'run_pipeline\.py|RUNBOOK\.md' .planning/phases/04-regime-conditional-etf-portfolio-behavior/README.md` exits 0.
    - `test -f .planning/phases/05-recommendations-machine-readable-outputs/README.md` exits 0.
    - `grep -F "05-recommendations-machine-readable-outputs-VERIFICATION.md" .planning/phases/05-recommendations-machine-readable-outputs/README.md` exits 0.
    - `grep -F "05-VALIDATION.md" .planning/phases/05-recommendations-machine-readable-outputs/README.md` exits 0.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 2 — README: phases 06 and 07</name>
  <read_first>
    - `.planning/phases/06-weekly-report-pipeline/06-weekly-report-pipeline-VERIFICATION.md`
    - `.planning/phases/06-weekly-report-pipeline/06-VALIDATION.md`
    - `.planning/phases/07-portfolio-and-email-integration/07-portfolio-and-email-integration-VERIFICATION.md`
    - `.planning/phases/07-portfolio-and-email-integration/07-VALIDATION.md`
  </read_first>
  <action>
    Create **`.planning/phases/06-weekly-report-pipeline/README.md`**: links `./06-weekly-report-pipeline-VERIFICATION.md`, `./06-VALIDATION.md`; cite `scripts/run_weekly_report.py` and `RUNBOOK.md` per 06 VERIFICATION; note CLOSURE-01 **`06-weekly-report-pipeline-01-SUMMARY.md`** exists beside **`06-weekly-report-pipeline-01-PLAN.md`** for plan–summary parity.

    Create **`.planning/phases/07-portfolio-and-email-integration/README.md`**: links `./07-portfolio-and-email-integration-VERIFICATION.md`, `./07-VALIDATION.md`; cite email weekly path from 07 VERIFICATION (`trading_crab_lib/email.py`, `scripts/run_weekly_report.py`, etc. — copy from file).
  </action>
  <acceptance_criteria>
    - `grep -F "06-weekly-report-pipeline-VERIFICATION.md" .planning/phases/06-weekly-report-pipeline/README.md` exits 0.
    - `grep -F "06-VALIDATION.md" .planning/phases/06-weekly-report-pipeline/README.md` exits 0.
    - `grep -F "06-weekly-report-pipeline-01-SUMMARY.md" .planning/phases/06-weekly-report-pipeline/README.md` exits 0.
    - `grep -F "07-portfolio-and-email-integration-VERIFICATION.md" .planning/phases/07-portfolio-and-email-integration/README.md` exits 0.
    - `grep -F "07-VALIDATION.md" .planning/phases/07-portfolio-and-email-integration/README.md` exits 0.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 3 — README: phases 08 and 09</name>
  <read_first>
    - `.planning/phases/08-data-signals-diagnostics/08-data-signals-diagnostics-VERIFICATION.md`
    - `.planning/phases/08-data-signals-diagnostics/08-VALIDATION.md`
    - `.planning/phases/09-tactics-and-diagnostics/09-tactics-and-diagnostics-VERIFICATION.md`
    - `.planning/phases/09-tactics-and-diagnostics/09-VALIDATION.md`
  </read_first>
  <action>
    Create **`.planning/phases/08-data-signals-diagnostics/README.md`**: links `./08-data-signals-diagnostics-VERIFICATION.md`, `./08-VALIDATION.md`; mention **`08-data-signals-diagnostics-01-SUMMARY.md`** for plan parity; cite diagnostics pipeline / config from 08 VERIFICATION.

    Create **`.planning/phases/09-tactics-and-diagnostics/README.md`**: links `./09-tactics-and-diagnostics-VERIFICATION.md`, `./09-VALIDATION.md`; cite `src/trading_crab_lib/tactics.py` and `outputs/reports/tactics_signals.parquet` if present in VERIFICATION.
  </action>
  <acceptance_criteria>
    - `grep -F "08-data-signals-diagnostics-VERIFICATION.md" .planning/phases/08-data-signals-diagnostics/README.md` exits 0.
    - `grep -F "08-VALIDATION.md" .planning/phases/08-data-signals-diagnostics/README.md` exits 0.
    - `grep -F "08-data-signals-diagnostics-01-SUMMARY.md" .planning/phases/08-data-signals-diagnostics/README.md` exits 0.
    - `grep -F "09-tactics-and-diagnostics-VERIFICATION.md" .planning/phases/09-tactics-and-diagnostics/README.md` exits 0.
    - `grep -F "09-VALIDATION.md" .planning/phases/09-tactics-and-diagnostics/README.md` exits 0.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 4 — README: phases 10 and 11</name>
  <read_first>
    - `.planning/phases/10-tactics-install/10-tactics-install-VERIFICATION.md`
    - `.planning/phases/10-tactics-install/10-VALIDATION.md`
    - `.planning/phases/11-core-cleanup/11-core-cleanup-VERIFICATION.md`
    - `.planning/phases/11-core-cleanup/11-VALIDATION.md`
  </read_first>
  <action>
    Create **`.planning/phases/10-tactics-install/README.md`**: links `./10-tactics-install-VERIFICATION.md`, `./10-VALIDATION.md`; cite `scripts/README.md`, `scripts/setup.sh` or `check_env.sh` per 10 VERIFICATION.

    Create **`.planning/phases/11-core-cleanup/README.md`**: links `./11-core-cleanup-VERIFICATION.md`, `./11-VALIDATION.md`; summarize cleanup scope from 11 VERIFICATION in one short paragraph.
  </action>
  <acceptance_criteria>
    - `grep -F "10-tactics-install-VERIFICATION.md" .planning/phases/10-tactics-install/README.md` exits 0.
    - `grep -F "10-VALIDATION.md" .planning/phases/10-tactics-install/README.md` exits 0.
    - `grep -F "11-core-cleanup-VERIFICATION.md" .planning/phases/11-core-cleanup/README.md` exits 0.
    - `grep -F "11-VALIDATION.md" .planning/phases/11-core-cleanup/README.md` exits 0.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 5 — REQUIREMENTS, ROADMAP, phase 24 README + SUMMARY stub</name>
  <read_first>
    - `.planning/REQUIREMENTS.md`
    - `.planning/ROADMAP.md`
    - `.planning/phases/24-v1-0-brownfield-phase-readmes/README.md`
    - `.planning/phases/23-v1-0-plan-summary-parity/23-SUMMARY.md`
  </read_first>
  <action>
    1. In **`.planning/REQUIREMENTS.md`**: set **CLOSURE-02** checkbox to `[x]`; update traceability row **CLOSURE-02 | Phase 24 | Done** (or equivalent table wording).
    2. In **`.planning/ROADMAP.md`**: mark Phase 24 checklist complete; set progress row for phase 24 to **Complete** with CLOSURE-02 satisfied.
    3. Expand **`.planning/phases/24-v1-0-brownfield-phase-readmes/README.md`** with links to **`24-CONTEXT.md`**, **`24-RESEARCH.md`**, **`24-VALIDATION.md`**, **`24-v1-0-brownfield-phase-readmes-01-PLAN.md`**, and a bullet list of the eight target directories (relative paths).
    4. Create **`.planning/phases/24-v1-0-brownfield-phase-readmes/24-SUMMARY.md`**: execution date, commands run (`validate health`), table of eight README paths, pointer to CLOSURE-02.
  </action>
  <acceptance_criteria>
    - `grep -E '\[x\].*CLOSURE-02|CLOSURE-02.*Done' .planning/REQUIREMENTS.md` returns at least one match.
    - `grep '| 24 |' .planning/ROADMAP.md | grep -i Complete` exits 0 (progress table row for phase 24).
    - `test -f .planning/phases/24-v1-0-brownfield-phase-readmes/24-SUMMARY.md` exits 0.
    - `grep -F "24-v1-0-brownfield-phase-readmes-01-PLAN.md" .planning/phases/24-v1-0-brownfield-phase-readmes/README.md` exits 0.
  </acceptance_criteria>
</task>

## Verification checklist (pre-merge)

- [ ] Eight brownfield `README.md` files exist
- [ ] `node .codex/get-shit-done/bin/gsd-tools.cjs validate health` exits 0
- [ ] CLOSURE-02 complete in REQUIREMENTS.md

## Plan metadata

| Field | Value |
|-------|-------|
| Roadmap | Phase 24 — v1.0 brownfield phase READMEs |
| Nyquist | Doc + grep; see `24-VALIDATION.md` |
