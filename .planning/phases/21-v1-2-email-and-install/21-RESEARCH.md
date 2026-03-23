# Phase 21 — Technical research (EMAIL-10 / INSTALL-20)

**Date:** 2026-03-23  
**Question:** What is already implemented vs what v1.2 requirements still need?

## Already in repo (v1.0 / Phase 7)

| Capability | Location |
|------------|----------|
| SMTP send | `trading_crab_lib/email.py` — `load_email_config`, `send_weekly_email`, `build_weekly_email_body` |
| CLI | `run_pipeline.py` — `--weekly-report`, `--send-email`; `step7_dashboard` writes `weekly_report.md` |
| Script | `scripts/run_weekly_report.py` — subprocess pipeline + archive + optional `--send-email` |
| Template | `config/email.example.yaml` |
| Gitignore | `config/email.local.yaml`, `config/email.yaml` |
| Installer | `scripts/install_trading_crab.sh` copies `email.example.yaml` → `email.local.yaml` |
| Tests | `tests/test_email_weekly.py`, `tests/test_scripts_weekly_report.py` (mocked send) |

## Gap vs REQUIREMENTS

1. **INSTALL-20:** `scripts/setup.sh` (primary “venv + pip” path) does **not** copy `email.example.yaml` — only `.env.example` → `.env`. **Fix:** add optional copy step (non-destructive if `email.local.yaml` exists).
2. **EMAIL-10:** Traceability + operator docs — **RUNBOOK** should have an explicit **SMTP weekly report** subsection (today scattered under REPORT-03 / env-only notes).
3. **Success criterion “.gitignore verified”** — add a **unit test** that asserts `email.local.yaml` and `.env` appear in `.gitignore` (read file, no git binary).

## Validation Architecture

| Dimension | Approach |
|-----------|----------|
| Unit | `pytest tests/test_gitignore_secrets.py` (new) + existing email/weekly script tests |
| Config | `load()` + `load_email_config` return empty/missing without crashing |
| Manual | Optional: configure Gmail app password + `run_weekly_report.py --send-email` on real run |

Automated gate: **`pytest tests/test_gitignore_secrets.py tests/test_email_weekly.py tests/test_scripts_weekly_report.py -q`**

---

## Validation Architecture (Nyquist)

- After each task: quick pytest subset above.
- Before merge: full suite or project convention.

---

## RESEARCH COMPLETE
