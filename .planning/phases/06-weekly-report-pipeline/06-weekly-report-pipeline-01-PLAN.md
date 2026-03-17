---
phase: 06-weekly-report-pipeline
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - scripts/run_weekly_report.py (or run_pipeline.py --steps usage)
  - outputs/reports/ (timestamped copy behavior)
  - docs or README for weekly run
autonomous: true
requirements: []
user_setup: []
must_haves:
  truths:
    - "One command runs the pipeline for a weekly report (steps 2–7 or 1–7) without needing to remember flags."
    - "Each weekly run can produce a timestamped copy of weekly_report.md (and optionally key CSVs) for archiving."
    - "An email-ready plain-text body is available (e.g. outputs/reports/email_body.txt) for manual paste or sendmail."
  artifacts:
    - path: "scripts/run_weekly_report.py"
      provides: "Single entry point for weekly report run (calls run_pipeline or steps 2–7)."
    - path: "outputs/reports/weekly_YYYY-MM-DD.md"
      provides: "Timestamped copy of weekly report per run (when script is used)."
    - path: "outputs/reports/email_body.txt"
      provides: "Plain-text body derived from weekly_report.md for email paste or sendmail."
  key_links:
    - from: "scripts/run_weekly_report.py"
      to: "run_pipeline.py"
      via: "subprocess or import run_pipeline main with --steps 2,3,4,5,6,7"
---

<objective>
Provide a single-command weekly report run and archive each run with a timestamped report copy and an email-ready text body. No SMTP in this plan.
</objective>

<execution_context>
@.planning/PROJECT.md
@.planning/phases/06-weekly-report-pipeline/06-RESEARCH.md
@run_pipeline.py
@pipelines/07_dashboard.py
</execution_context>

<context>
- Step 7 already writes outputs/reports/weekly_report.md and recommendation_bundle.parquet.
- run_pipeline.py accepts --steps 2,3,4,5,6,7 (use cached ingest) or 1,2,3,4,5,6,7 (full refresh).
- User may run weekly with cached data (2–7) most of the time; occasional full refresh (1–7).
</context>

<tasks>

<task type="auto">
  <name>Task 1: Add scripts/run_weekly_report.py entry point</name>
  <files>scripts/run_weekly_report.py</files>
  <action>
    - Create scripts/ directory if missing.
    - Add run_weekly_report.py that:
      - By default runs steps 2,3,4,5,6,7 (cached ingest; no --refresh). Option: --full to run steps 1–7.
      - Invokes run_pipeline.main() or subprocess with the appropriate --steps and no --plots unless --plots is passed.
      - Accepts optional --plots and --verbose; passes them through.
    - Document in script docstring or README: "Run from repo root: python scripts/run_weekly_report.py"
  </action>
  <verify>
    - From repo root: python scripts/run_weekly_report.py (with cached data) runs steps 2–7 and exits 0.
    - python scripts/run_weekly_report.py --full runs steps 1–7 when network/config allow.
  </verify>
</task>

<task type="auto">
  <name>Task 2: Timestamped report copy and email_body.txt</name>
  <files>scripts/run_weekly_report.py, src/market_regime/reporting.py or pipelines/07_dashboard.py</files>
  <action>
    - After step 7 completes (either from run_weekly_report.py or inside 07_dashboard.py):
      - Copy outputs/reports/weekly_report.md to outputs/reports/weekly_YYYY-MM-DD.md (today's date).
      - Write outputs/reports/email_body.txt: plain-text version of the report (same content as weekly_report.md or a short preamble + report), suitable for pasting into email or "cat email_body.txt | sendmail ...".
    - Prefer implementing the copy and email_body write in the runner script (after invoking pipeline) so 07_dashboard.py stays unchanged; alternatively add a small helper in reporting.py and call it from 07 or from the script.
  </action>
  <verify>
    - After running scripts/run_weekly_report.py, outputs/reports/weekly_YYYY-MM-DD.md exists and outputs/reports/email_body.txt exists with readable content.
  </verify>
</task>

<task type="auto">
  <name>Task 3: Document weekly run in README or CLAUDE.md</name>
  <files>README.md or scripts/README.md or .planning/NEXT_STEPS.md</files>
  <action>
    - Add a short "Weekly report" section: command to run (python scripts/run_weekly_report.py), meaning of --full, where to find weekly_report.md and email_body.txt, and optional cron example (e.g. "0 9 * * 1" for Monday 9am).
  </action>
  <verify>
    - README or scripts/README or NEXT_STEPS contains the weekly run command and cron hint.
  </verify>
</task>

</tasks>

<success_criteria>
- One command runs the weekly pipeline (2–7 or 1–7).
- Timestamped weekly_YYYY-MM-DD.md and email_body.txt are produced each run.
- Docs mention how to run and optionally schedule.
</success_criteria>
