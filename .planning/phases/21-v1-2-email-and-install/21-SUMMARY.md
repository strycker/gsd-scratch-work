# Phase 21 — Execution summary (EMAIL-10, INSTALL-20)

**Plan:** `21-v1-2-email-and-install-01-PLAN.md`  
**Executed:** 2026-03-23  
**Requirements:** EMAIL-10, INSTALL-20

## What shipped

- **`scripts/setup.sh`** — After `.env` scaffold, **section 5b**: `mkdir -p config/`; copy **`config/email.example.yaml` → `config/email.local.yaml`** when local missing; Gmail app-password hint; **Next steps** echo includes optional `--send-email` commands.
- **`tests/test_gitignore_secrets.py`** — Asserts `.env` and `email.local.yaml` patterns appear in **`.gitignore`** (no `git` subprocess).
- **`RUNBOOK.md`** — New **SMTP / weekly email (EMAIL-10)** section: `email.py`, templates, `run_pipeline.py` / `run_weekly_report.py` flags, gitignore test pointer.
- **`scripts/README.md`** — **Happy path (new machine)** — four-step flow (`setup.sh` → edit secrets → activate → `run_weekly_report.py`).

## What was already present (unchanged core)

- **`src/trading_crab_lib/email.py`**, **`run_pipeline.py --weekly-report --send-email`**, **`scripts/run_weekly_report.py --send-email`**, **`config/email.example.yaml`**.

## Verification

- `PYTHONPATH=src python -m pytest tests/test_gitignore_secrets.py tests/test_email_weekly.py tests/test_scripts_weekly_report.py -q`
- `bash -n scripts/setup.sh`

## Manual

- Configure `config/email.local.yaml` and run `python scripts/run_weekly_report.py --send-email` after a successful weekly report generation.
