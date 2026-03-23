# Phase 6 — Weekly report pipeline

The v1.0 **one-command weekly flow** (subprocess of `run_pipeline.py` + archived markdown/email body) is **shipped**. This folder is a **brownfield** GSD anchor.

**Plan–summary parity (CLOSURE-01)**

- [`06-weekly-report-pipeline-01-PLAN.md`](./06-weekly-report-pipeline-01-PLAN.md) ↔ [`06-weekly-report-pipeline-01-SUMMARY.md`](./06-weekly-report-pipeline-01-SUMMARY.md).

**Evidence**

- [Verification](./06-weekly-report-pipeline-VERIFICATION.md) — REPORT-01..02.
- [Validation](./06-VALIDATION.md).

**Primary entrypoints**

- `scripts/run_weekly_report.py` — default steps 2–7 or `--full` 1–7; optional `--send-email`.
- `RUNBOOK.md` (repo root) — weekly ops and email notes.
