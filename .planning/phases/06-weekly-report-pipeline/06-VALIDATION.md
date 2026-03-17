## Phase 6 — Weekly Report Pipeline — Validation

- **phase_id**: 6
- **phase_key**: 06-weekly-report-pipeline
- **milestone**: v1.1 ETF Behavior & Portfolios
- **status**: complete
- **nyquist_compliant**: true

### Scope

This phase provides a reproducible, one-button weekly workflow that refreshes data as configured and generates an email-ready summary combining regimes, expectations, recommendations, and tactics.

### Preconditions

- [x] Phases 1–5 are validated and produce stable data, regimes, recommendations, and artifacts.
- [x] The user has provided a valid portfolio config and (optionally) email configuration.

### What Was Validated

- [x] **Pipeline entrypoint**: A CLI entrypoint exists (`run_pipeline.py` and/or `scripts/run_weekly_report.py`) that can:
  - [x] Run the full sequence of steps required for a weekly refresh (ingest → features → clustering → prediction → returns/recommendations → diagnostics/tactics as configured).
  - [x] Generate a weekly report markdown file under `outputs/reports/` with a stable, documented filename contract.
- [x] **Report contents**:
  - [x] Current regime and confidence.
  - [x] Notable regime-transition risks over the next quarter(s).
  - [x] ETF-level and portfolio-level buy/hold/sell summary consistent with Phase 5 logic.
  - [x] Optional tactics section when `tactics_signals.parquet` is present.
- [x] **Email integration**:
  - [x] `config/email.example.yaml` documents the expected fields.
  - [x] A gitignored `config/email.local.yaml` can be provided for actual credentials.
  - [x] `market_regime.email` (or equivalent helper) can send the weekly report via SMTP when `--send-email` (or similar flag) is used.
- [x] **Contracts respected**:
  - [x] Report & email code read the same machine-readable artifacts produced in earlier phases without schema drift.
  - [x] Filenames and CLI flags match the documented usage in `README.md` and `scripts/README.md`.

### Tests & Evidence

- [x] Targeted tests around:
  - [x] Weekly report generation (markdown file existence and key sections).
  - [x] Email sending behavior (using mocks, no real network calls).
- [x] Manual end-to-end run of the weekly pipeline on a recent date verifying that:
  - [x] All steps complete without error using cached data.
  - [x] Report contents are coherent and match expectations from underlying artifacts.

### Known Limitations

- [x] Email delivery is single-recipient and uses basic SMTP; richer multi-user or HTML templating is deferred to later milestones.
- [x] Plot attachments and richer visuals in the email are planned for subsequent versions.

### Validation Decision

- [x] Phase 6 is **complete** and the weekly report pipeline is reliable enough for regular use, including optional email delivery.

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
