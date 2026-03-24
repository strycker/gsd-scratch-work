---
phase: 21-v1-2-email-and-install
verified: 2026-03-24T18:00:00Z
status: passed
requirements:
  - EMAIL-10
  - INSTALL-20
---

# Phase 21: Email delivery & install hardening — Verification Report

**Phase goal (ROADMAP):** Reliable optional SMTP send for weekly report; improved setup docs/scripts for secrets.

**Requirements:** EMAIL-10, INSTALL-20

**Verified:** 2026-03-24

**Overall status:** `passed` — evidence matches `21-SUMMARY.md` and automated commands below.

---

## Observable truths

| # | Truth | Status | Evidence |
|---|--------|--------|----------|
| 1 | Optional SMTP send path exists for weekly report output (`email.local.yaml`, templates, `--send-email`). | ✓ | `src/trading_crab_lib/email.py`; `run_pipeline.py` + `scripts/run_weekly_report.py` `--send-email`; `config/email.example.yaml`. |
| 2 | Setup script scaffolds secrets and `email.local.yaml` when missing. | ✓ | `scripts/setup.sh` section 5b (see `21-SUMMARY.md`). |
| 3 | `.gitignore` covers secrets (`tests/test_gitignore_secrets.py`). | ✓ | `tests/test_gitignore_secrets.py`. |
| 4 | Docs: `RUNBOOK.md` SMTP section; `scripts/README.md` happy path. | ✓ | `RUNBOOK.md` *SMTP / weekly email (EMAIL-10)*; `scripts/README.md`. |
| 5 | Regression tests for email/weekly script wiring. | ✓ | `tests/test_email_weekly.py`, `tests/test_scripts_weekly_report.py` (see `21-SUMMARY.md`). |

---

## Requirements coverage

| Requirement | Status | Evidence |
|-------------|--------|----------|
| **EMAIL-10** | ✓ SATISFIED | `email.py`, `--send-email`, `RUNBOOK.md`, commands in `21-SUMMARY.md` |
| **INSTALL-20** | ✓ SATISFIED | `scripts/setup.sh`, `scripts/README.md`, `test_gitignore_secrets.py` |

---

## Milestone audit note (integration)

**`.planning/v1.2-MILESTONE-AUDIT.md`** reported **step order** (weekly report step **7** vs diagnostics **8** / tactics **9**) and **`scripts/run_weekly_report.py`** scope (steps 1–7) as cross-phase integration gaps. Those are **deferred to Phase 27** — not in scope for Phase 21 product delivery or this verification file.

---

## Automated verification commands (re-run)

```bash
PYTHONPATH=src python -m pytest tests/test_gitignore_secrets.py tests/test_email_weekly.py tests/test_scripts_weekly_report.py -q
bash -n scripts/setup.sh
```
