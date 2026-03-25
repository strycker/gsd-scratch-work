# Plan 01 — Hybrid summary (Phase 21, EMAIL-10 / INSTALL-20)

**Plan:** `21-v1-2-email-and-install-01-PLAN.md`  
**Phase narrative:** `21-SUMMARY.md`

## As-built

- `scripts/setup.sh` scaffolds `config/email.local.yaml` from `config/email.example.yaml` when missing; hints for operator setup.
- `tests/test_gitignore_secrets.py` asserts `.gitignore` ignores `.env` and `email.local.yaml` patterns.
- `RUNBOOK.md` SMTP / weekly email section; `scripts/README.md` happy path with `--send-email`.
- Core SMTP remains `src/trading_crab_lib/email.py` + existing CLI flags (`run_pipeline`, `run_weekly_report.py`).

## Plan fidelity

- Close **EMAIL-10** and **INSTALL-20** via docs + setup parity + gitignore contract test without re-implementing `email.py` unless bug found.

## Delta from plan

- **Complete:** All plan `must_haves` addressed per `21-SUMMARY.md`.
- **Deferred to Phase 27 (integration):** Audit noted weekly script step sets — **Phase 27** updated `scripts/run_weekly_report.py` defaults to run **8, 9** before **7**; not claimed as EMAIL-10 code change in phase 21 narrative.
