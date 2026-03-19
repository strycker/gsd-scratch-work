---
phase: 13-v1-audit-verify-phases-7-11
plan: 01
type: execute
wave: 1
depends_on:
  - 12-v1-audit-verify-phases-4-6-01
files_modified:
  - .planning/REQUIREMENTS.md
  - .planning/ROADMAP.md
  - .planning/phases/07-portfolio-and-email-integration/07-portfolio-and-email-integration-VERIFICATION.md
  - .planning/phases/08-data-signals-diagnostics/08-data-signals-diagnostics-VERIFICATION.md
  - .planning/phases/09-tactics-and-diagnostics/09-tactics-and-diagnostics-VERIFICATION.md
  - .planning/phases/10-tactics-install/10-tactics-install-VERIFICATION.md
  - .planning/phases/11-core-cleanup/11-core-cleanup-VERIFICATION.md
  - .planning/phases/13-v1-audit-verify-phases-7-11/13-VALIDATION.md
autonomous: true
requirements:
  - PORT-04
  - REPORT-03
  - DATA-04
  - DIAG-01
  - DIAG-02
  - TACTICS-01
  - TACTICS-02
  - TACTICS-03
  - INSTALL-10
  - CORE-01
  - CORE-02
user_setup: []
must_haves:
  truths:
    - "Each phase directory 07–11 has exactly one canonical *-VERIFICATION.md (named {phase-slug}-VERIFICATION.md) with frontmatter status passed or gaps_found."
    - "Every VERIFICATION ties ROADMAP success criteria to run_pipeline.py steps, pipelines/*.py, src/trading_crab_lib modules, config paths, and known tests or smoke commands."
    - ".planning/REQUIREMENTS.md gains a traceability block extension for PORT-04, REPORT-03, DATA-04, DIAG-01, DIAG-02, TACTICS-01..03, INSTALL-10, CORE-01, CORE-02 (or documents gaps_found per row) — IDs must exist in the requirements narrative or be added with short definitions consistent with ROADMAP Phase 7–11."
    - "13-VALIDATION.md lists Wave 0 + quick pytest commands that cover email, tactics, diagnostics, and env scripts where tests already exist."
  artifacts:
    - path: ".planning/phases/07-portfolio-and-email-integration/07-portfolio-and-email-integration-VERIFICATION.md"
      provides: "PORT-04, REPORT-03 evidence"
      min_lines: 70
    - path: ".planning/phases/08-data-signals-diagnostics/08-data-signals-diagnostics-VERIFICATION.md"
      provides: "DATA-04, DIAG-01, DIAG-02 evidence"
      min_lines: 70
    - path: ".planning/phases/09-tactics-and-diagnostics/09-tactics-and-diagnostics-VERIFICATION.md"
      provides: "TACTICS-01, TACTICS-02 evidence"
      min_lines: 70
    - path: ".planning/phases/10-tactics-install/10-tactics-install-VERIFICATION.md"
      provides: "TACTICS-03, INSTALL-10 evidence"
      min_lines: 70
    - path: ".planning/phases/11-core-cleanup/11-core-cleanup-VERIFICATION.md"
      provides: "CORE-01, CORE-02 evidence"
      min_lines: 70
    - path: ".planning/phases/13-v1-audit-verify-phases-7-11/13-VALIDATION.md"
      provides: "Phase 13 Nyquist contract"
      min_lines: 45
  key_links:
    - from: "run_pipeline.py"
      to: "--send-email"
      via: "step7_dashboard + email helpers; argparse"
      pattern: "send.email|send_email"
    - from: "run_pipeline.py"
      to: "outputs/reports/diagnostics/"
      via: "step8_diagnostics"
      pattern: "step8_diagnostics"
    - from: "run_pipeline.py"
      to: "tactics_signals"
      via: "step9_tactics"
      pattern: "step9"
    - from: "scripts/check_env.sh"
      to: "trading_crab_lib"
      via: "INSTALL-10 smoke"
      pattern: "check_env"
---

<objective>
Close **v1.0 milestone audit** verification debt for roadmap phases **7–11** by authoring five `*-VERIFICATION.md` files and extending **REQUIREMENTS.md** traceability for IDs that today appear only in ROADMAP success criteria (PORT-04, REPORT-03, DATA-04, DIAG-*, TACTICS-*, INSTALL-10,CORE-*).

**Output:** Executable evidence for `$gsd-audit-milestone` re-run; optional follow-up `$gsd-execute-phase 13` performs doc + table edits only unless execution finds **gaps_found** that require code fixes (separate micro-plan).
</objective>

<execution_context>
@.planning/v1.0-MILESTONE-AUDIT.md
@.planning/ROADMAP.md
@.planning/REQUIREMENTS.md
@.planning/phases/13-v1-audit-verify-phases-7-11/13-CONTEXT.md
@CLAUDE.md
@run_pipeline.py
@pipelines/07_dashboard.py
@pipelines/08_diagnostics.py
@pipelines/09_tactics.py
@scripts/run_weekly_report.py
@scripts/check_env.sh
@scripts/run_tests.sh
@src/trading_crab_lib/email.py
@src/trading_crab_lib/diagnostics.py
@src/trading_crab_lib/tactics.py
@config/settings.yaml
</execution_context>

<context>
**Discovery hints (re-validate during execute):**
- **Phase 7:** `config/portfolio.yaml`, `load_portfolio` / `config/portfolio.example.yaml`; `trading_crab_lib.email` (`load_email_config`, `send_weekly_email`, `build_weekly_email_body`); `run_pipeline.py` flags (`--send-email`); `recommendation_bundle.parquet` path from Phase 12 step 7 parity.
- **Phase 8:** `config/settings.yaml` `fred.series` + `diagnostics` sections; `run_pipeline.step8_diagnostics`; `pipelines/08_diagnostics.py`; artifacts `outputs/reports/diagnostics/*.parquet`.
- **Phase 9:** `run_pipeline.step9_tactics`; `pipelines/09_tactics.py`; `compute_tactics_metrics`, `classify_tactics`; weekly report tactics section in `reporting.write_weekly_report_md` (optional tail).
- **Phase 10:** tactics thresholds in `settings.yaml`; `tests/test_tactics.py` if present; `scripts/check_env.sh`, `scripts/README.md`, installer/smoke docs.
- **Phase 11:** `data.end_date` null handling in `config` / ingestion; `tests` for end_date; `__future__` annotations convention per CLAUDE.md.

Use **`src/trading_crab_lib`** paths in all new prose (not `market_regime`).
</context>

<tasks>

<task type="auto" tdd="false">
  <name>Task 1: Extend REQUIREMENTS.md v1 traceability table</name>
  <files>.planning/REQUIREMENTS.md</files>
  <behavior>
    Add rows for PORT-04, REPORT-03, DATA-04, DIAG-01, DIAG-02, TACTICS-01, TACTICS-02, TACTICS-03, INSTALL-10, CORE-01, CORE-02 with Phase column `13` (gap-closure tracking) and Status `Pending` until VERIFICATION passes. If any ID lacks a bullet definition in the narrative body, add a minimal **v1 Requirements** subsection (1–2 lines each) aligned with ROADMAP Phase 7–11 wording — avoid contradicting existing v1.2 aspirational sections.
  </behavior>
  <verify>
    `grep` finds each new REQ-ID in the traceability table; no duplicate ID rows.
  </verify>
</task>

<task type="auto" tdd="false">
  <name>Task 2: 07-portfolio-and-email-integration-VERIFICATION.md</name>
  <files>.planning/phases/07-portfolio-and-email-integration/07-portfolio-and-email-integration-VERIFICATION.md</files>
  <behavior>
    Map PORT-04 (portfolio file consumed; bundle deltas) and REPORT-03 (email config + send path). Cite `load_portfolio`, `run_pipeline` / `step7`, `scripts/run_weekly_report.py --send-email`, `src/trading_crab_lib/email.py`, `tests/test_scripts_weekly_report.py` (if covers send path).
  </behavior>
  <verify>
    Frontmatter + requirements table + key_links ≥ 3 rows.
  </verify>
</task>

<task type="auto" tdd="false">
  <name>Task 3: 08-data-signals-diagnostics-VERIFICATION.md</name>
  <files>.planning/phases/08-data-signals-diagnostics/08-data-signals-diagnostics-VERIFICATION.md</files>
  <behavior>
    Map DATA-04 (FRED expansion / ingestion), DIAG-01 (ratios), DIAG-02 (RRG artifacts). Cite `config/settings.yaml`, `pipelines/01_ingest.py` / FRED module, `step8_diagnostics`, `pipelines/08_diagnostics.py`, diagnostic parquet paths.
  </behavior>
  <verify>
    Explicit **gaps_found** if any roadmap series from ROADMAP is not in `settings.yaml` (do not lie — audit honesty).
  </verify>
</task>

<task type="auto" tdd="false">
  <name>Task 4: 09-tactics-and-diagnostics-VERIFICATION.md</name>
  <files>.planning/phases/09-tactics-and-diagnostics/09-tactics-and-diagnostics-VERIFICATION.md</files>
  <behavior>
    Map TACTICS-01 (artifact `tactics_signals` / parquet name in repo), TACTICS-02 (weekly tactics section). Cite `step9_tactics`, `pipelines/09_tactics.py`, `trading_crab_lib.tactics`, `reporting.write_weekly_report_md` optional block.
  </behavior>
  <verify>
    Artifact filename(s) on disk match code references.
  </verify>
</task>

<task type="auto" tdd="false">
  <name>Task 5: 10-tactics-install-VERIFICATION.md</name>
  <files>.planning/phases/10-tactics-install/10-tactics-install-VERIFICATION.md</files>
  <behavior>
    Map TACTICS-03 (config-driven tactics + tests) and INSTALL-10 (check_env / run_tests / docs). Cite `tests/test_tactics.py` (or note if missing), `settings.yaml` tactics keys, `scripts/check_env.sh`, `scripts/run_tests.sh`, `scripts/README.md`.
  </behavior>
  <verify>
    Test file paths verified to exist or marked gaps_found.
  </verify>
</task>

<task type="auto" tdd="false">
  <name>Task 6: 11-core-cleanup-VERIFICATION.md</name>
  <files>.planning/phases/11-core-cleanup/11-core-cleanup-VERIFICATION.md</files>
  <behavior>
    Map CORE-01 (dirs created), CORE-02 (end_date null → today + tests). Cite `market_regime`/`trading_crab_lib` config.load, ingestion date handling, relevant tests (search `end_date` in tests).
  </behavior>
  <verify>
    Status passed only if evidence exists; else gaps_found with next action.
  </verify>
</task>

<task type="auto" tdd="false">
  <name>Task 7: 13-VALIDATION.md + ROADMAP plan checkbox</name>
  <files>.planning/phases/13-v1-audit-verify-phases-7-11/13-VALIDATION.md, .planning/ROADMAP.md, .planning/phases/13-v1-audit-verify-phases-7-11/13-v1-audit-verify-phases-7-11-01-PLAN.md</files>
  <behavior>
    Create **13-VALIDATION.md** (Nyquist: Test Infrastructure, per-task map for Tasks 1–6, manual-only for full E2E diagnostics). Update ROADMAP Phase **13** **Plans:** `1 plan` with `[ ] 13-v1-audit-verify-phases-7-11-01-PLAN.md` → flip to `[x]` only after `$gsd-execute-phase 13`.
  </behavior>
  <verify>
    `gsd-tools phases list` includes `13-v1-audit-verify-phases-7-11`.
  </verify>
</task>

</tasks>

<notes>
- This plan is **documentation-first**. If VERIFICATION reveals false “Complete” claims in REQUIREMENTS, **leave Pending** and describe the gap.
- After execute + validate: `$gsd-audit-milestone` then Phase **14** (planning reconciliation).
</notes>
