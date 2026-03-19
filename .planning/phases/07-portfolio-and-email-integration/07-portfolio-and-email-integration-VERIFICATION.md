---
phase: 07-portfolio-and-email-integration
verified: 2026-03-19T00:00:00Z
status: passed
score: 2/2 roadmap requirements satisfied (PORT-04, REPORT-03)
human_verification:
  - test: "Place weights in config/portfolio.yaml; run step 7; inspect recommendation_bundle.parquet"
    expected: "Bundle reflects loaded portfolio and includes portfolio-aware fields."
    why_human: "Confirm real weights match your YAML without only trusting unit mocks."
  - test: "Configure config/email.local.yaml and run scripts/run_weekly_report.py --send-email (or run_pipeline with --send-email)"
    expected: "Email sends or fails gracefully with logged reason; no secrets in repo."
    why_human: "SMTP depends on real network/credentials."
---

# Phase 7: Portfolio & Email Integration — Verification

**Phase goal (ROADMAP):** Portfolio-aware pipeline and optional SMTP delivery of the weekly report.  
**Audit closure:** Phase 13 — evidence for PORT-04, REPORT-03.  
**Status:** **passed**.

## Requirement coverage

| ID | Description (ROADMAP-aligned) | Status | Evidence |
|----|------------------------------|--------|----------|
| PORT-04 | `config/portfolio.yaml` defines tickers/weights; machine-readable outputs include portfolio-aware deltas/metrics | ✓ | `trading_crab_lib.config.load_portfolio()` reads normalized weights from `config/portfolio.yaml` (or empty dict if missing). `pipelines/07_dashboard.py` calls `load_portfolio()` and passes weights into dashboard / bundle paths. `run_pipeline.py` `step7_dashboard` invokes `save_recommendation_bundle(..., portfolio_weights=..., path=.../recommendation_bundle.parquet)`. Example template: `config/portfolio.example.yaml`. |
| REPORT-03 | Local email config + CLI path to send the generated report | ✓ | `trading_crab_lib.email.load_email_config` loads `config/email.local.yaml` (see `config/email.example.yaml`). `send_weekly_email`, `build_weekly_email_body` build MIME from `outputs/reports/`. `run_pipeline.py`: `--weekly-report` archives `weekly_report.md`; `--send-email` calls email helpers after pipeline steps. `scripts/run_weekly_report.py` supports `--send-email` and uses the same email module. |

## Code & entrypoint map

| Entrypoint | Role |
|------------|------|
| `run_pipeline.py` | `step7_dashboard`; flags `--weekly-report`, `--send-email`; `STEPS[7]` |
| `pipelines/07_dashboard.py` | Loads portfolio, runs dashboard, saves `dashboard.csv`, bundle, `weekly_report.md` when invoked from runner |
| `scripts/run_weekly_report.py` | Subprocesses `run_pipeline.py` with steps 2–7 (or 1–7 `--full`); optional `--send-email` |
| `src/trading_crab_lib/email.py` | `load_email_config`, `send_weekly_email`, `build_weekly_email_body` |
| `src/trading_crab_lib/config.py` | `load_portfolio()` |

## Artifacts

| Path | Producer |
|------|----------|
| `outputs/reports/recommendation_bundle.parquet` | `save_recommendation_bundle` from step 7 path in `run_pipeline.py` |
| `outputs/reports/weekly_report.md` | `write_weekly_report_md` |
| `outputs/reports/email_body.txt` | `archive_weekly_report` (after `--weekly-report` or script archive) |
| `config/portfolio.yaml` | User-maintained (optional) |
| `config/email.local.yaml` | User-maintained secrets (gitignored pattern per docs) |

## Tests

| Test file | Coverage |
|-----------|----------|
| `tests/test_scripts_weekly_report.py` | `TestScriptSendEmail` — `--send-email` calls `send_weekly_email` when config valid; skips send when config missing |
| `tests/test_email_weekly.py` | Email body construction / fallbacks for report paths |

## `key_links` (audit)

| From | To | Via |
|------|----|-----|
| `config/portfolio.yaml` | `recommendation_bundle.parquet` | `load_portfolio` → step 7 `save_recommendation_bundle` |
| `config/email.local.yaml` | SMTP send | `load_email_config` → `send_weekly_email` |
| `scripts/run_weekly_report.py` | `run_pipeline.py` | `subprocess.run` with `--steps` and optional `--send-email` |

## Notes

- Phase 6 verification (`06-weekly-report-pipeline-VERIFICATION.md`) scoped REPORT-02 to **content**; Phase 7 closes **delivery** (REPORT-03) and **portfolio wiring** (PORT-04).

## Evidence checklist (audit)

- [x] Portfolio loader implemented in `src/trading_crab_lib/config.py` (`load_portfolio`).
- [x] Dashboard step references portfolio weights when building recommendations / bundle (`pipelines/07_dashboard.py`).
- [x] `run_pipeline.py` step 7 path saves `recommendation_bundle.parquet` under `outputs/reports/`.
- [x] Email config load + send helpers live in `src/trading_crab_lib/email.py`.
- [x] CLI surfaces `--send-email` and `--weekly-report` post-steps.
- [x] Automated tests exist for weekly script send path (`tests/test_scripts_weekly_report.py`).

## Non-goals (Phase 7)

- Email provider-specific OAuth flows (SMTP only).
- Portfolio optimization beyond provided weights + regime-aware recommendations from upstream steps.

## Revision history

- 2026-03-19 — Phase 13 audit: initial `*-VERIFICATION.md` for roadmap Phase 7.
