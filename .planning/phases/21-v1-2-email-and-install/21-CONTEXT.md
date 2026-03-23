# Phase 21: v1.2 — Email delivery & install hardening (EMAIL-10, INSTALL-20)

**Gathered:** 2026-03-23  
**Status:** Ready for planning  
**Source:** `.planning/ROADMAP.md` Phase 21, **REQUIREMENTS.md**; existing **`trading_crab_lib/email.py`**, **`run_pipeline.py --send-email`**, **`scripts/run_weekly_report.py`**, **`scripts/install_trading_crab.sh`**

## Phase boundary

**EMAIL-10:** Optional SMTP send of `weekly_report.md` (or derived body) using **local untracked** config — no secrets in git. Product code for SMTP largely **shipped in v1.0 Phase 7**; Phase 21 **documents, verifies, and hardens** the path (RUNBOOK, tests, failure messaging if needed).

**INSTALL-20:** **Scaffold** `.env` + **email** config templates and **smoke** checks — extend **`scripts/setup.sh`** to parity with **`install_trading_crab.sh`** (copy `config/email.example.yaml` → `email.local.yaml` when missing), document a **two-command happy path** in **`scripts/README.md`**, and add a **lightweight automated check** that secret paths stay gitignored.

Out of scope: SendGrid OAuth, HTML-only templates as mandatory, changing SMTP library.

## Implementation decisions (locked)

- **Do not duplicate** `email.py` — extend docs/tests only unless a real bug is found.
- **Secrets:** Continue using **`config/email.local.yaml`** (gitignored) from **`config/email.example.yaml`**; keep **`.env`** for FRED only unless we document optional overlap.
- **Happy path:** Document e.g. `bash scripts/setup.sh` then `python scripts/run_weekly_report.py --send-email` with prerequisite: edit `email.local.yaml` + pipeline outputs exist.
- **Tests:** Prefer **no network** — mock SMTP or assert file/gitignore contracts; existing `tests/test_scripts_weekly_report.py` patterns apply.

## Canonical references

- `src/trading_crab_lib/email.py`
- `run_pipeline.py` (`--weekly-report`, `--send-email`)
- `scripts/run_weekly_report.py`
- `config/email.example.yaml`
- `.gitignore` (email.local.yaml)
- `.planning/phases/07-portfolio-and-email-integration/07-portfolio-and-email-integration-VERIFICATION.md`

## Deferred

- Third-party transactional APIs (SendGrid API key flow) — post–v1.2 unless pulled in.

---

*Phase: 21-v1-2-email-and-install*
