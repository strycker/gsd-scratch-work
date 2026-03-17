---
phase: 6
slug: weekly-report-pipeline
status: complete
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-16
---

## Phase 6: Weekly Report Pipeline

**Goal:** One-command weekly run, timestamped report copy, email-ready body; no SMTP.

### Wave 0 (after execution)

- [x] `scripts/run_weekly_report.py` exists and runs steps 2–7 (or 1–7 with --full).
- [x] `outputs/reports/weekly_YYYY-MM-DD.md` and `outputs/reports/email_body.txt` produced per run.
- [x] Docs updated (README.md Weekly report section + scripts/README.md) with weekly run command and cron example.

### Validation sign-off

- [x] All tasks have automated verify steps or manual check.
- [x] nyquist_compliant: tests added in tests/test_scripts_weekly_report.py (archive logic + CLI argv).
