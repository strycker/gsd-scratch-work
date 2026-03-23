# Phase 7 — Portfolio & email integration

The v1.0 work for **`config/portfolio.yaml`–aware outputs** and **optional SMTP delivery** of the weekly report is **shipped**. This directory is a **brownfield** GSD anchor.

**Evidence**

- [Verification](./07-portfolio-and-email-integration-VERIFICATION.md) — PORT-04, REPORT-03.
- [Validation](./07-VALIDATION.md).

**Primary entrypoints**

- `run_pipeline.py` — `step7_dashboard`; flags `--weekly-report`, `--send-email`.
- `pipelines/07_dashboard.py` — loads portfolio, writes dashboard and bundle paths.
- `scripts/run_weekly_report.py` — subprocess runner; `--send-email`.
- `src/trading_crab_lib/email.py` — `load_email_config`, `send_weekly_email`, `build_weekly_email_body`.
- `src/trading_crab_lib/config.py` — `load_portfolio()`.

Templates: `config/portfolio.example.yaml`, `config/email.example.yaml` → user `email.local.yaml`. See **`RUNBOOK.md`**.
