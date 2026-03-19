---
phase: 06-weekly-report-pipeline
verified: 2026-03-19T00:00:00Z
status: passed
score: 2/2 requirements satisfied (REPORT-01..02)
human_verification:
  - test: "Run scripts/run_weekly_report.py --full or default and open outputs/reports/weekly_report.md"
    expected: "Report includes regime, confidence, BUY/SELL ideas, transition note; suitable as email draft."
    why_human: "Tone and completeness for your advisory workflow."
---

# Phase 6: Weekly Report Pipeline — Verification

**Phase goal (ROADMAP):** One-command weekly flow + email-ready summary.  
**Audit closure:** Phase 12 — evidence for REPORT-01..02.  
**Status:** **passed**.

## Requirement coverage

| ID | Description | Status | Evidence |
|----|-------------|--------|----------|
| REPORT-01 | Reproducible weekly report pipeline (CLI/script) | ✓ | `scripts/run_weekly_report.py` subprocesses `run_pipeline.py` with `--steps 2,3,4,5,6,7` (default) or `1,2,3,4,5,6,7` (`--full`). Optional `--plots`, `--verbose`, `--send-email`. |
| REPORT-02 | Compact text summary for weekly email | ✓ | `write_weekly_report_md` in `trading_crab_lib.reporting` writes `outputs/reports/weekly_report.md`. `archive_weekly_report` copies to `weekly_YYYY-MM-DD.md` and `email_body.txt`. `trading_crab_lib.email.build_weekly_email_body` consumes reports dir for HTML/text email. |

## Artifact map

| Artifact | Producer |
|----------|----------|
| `outputs/reports/weekly_report.md` | `step7_dashboard` / `pipelines/07_dashboard.py` |
| `outputs/reports/email_body.txt` | `scripts/run_weekly_report.archive_weekly_report` |
| `outputs/reports/weekly_*.md` | archive step |

## Note

SMTP send (`--send-email`) is **Phase 7** scope (PORT-04 / REPORT-03); REPORT-02 here is satisfied by **body content** generation, not delivery.
