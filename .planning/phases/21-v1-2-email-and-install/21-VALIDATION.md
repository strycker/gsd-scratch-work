---
phase: 21
slug: v1-2-email-and-install
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-23
---

# Phase 21 — Validation Strategy

> EMAIL-10 + INSTALL-20 (email path hardening + setup parity).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | `pyproject.toml` |
| **Quick run command** | `PYTHONPATH=src python -m pytest tests/test_gitignore_secrets.py tests/test_email_weekly.py -q` |
| **Email + script** | `PYTHONPATH=src python -m pytest tests/test_scripts_weekly_report.py -q` |

---

## Per-Task Verification Map

| Task | Requirement | Automated Command | Status |
|------|-------------|-------------------|--------|
| 21-01-01 | INSTALL-20 | `grep -q email.example.yaml scripts/setup.sh` | ⬜ |
| 21-01-02 | EMAIL-10 docs | `grep -n send-email RUNBOOK.md` | ⬜ |
| 21-01-03 | Gitignore test | `pytest tests/test_gitignore_secrets.py -q` | ⬜ |

---

## Manual-Only

| Behavior | Why manual |
|----------|------------|
| SMTP delivery to real inbox | Network + credentials |

---

## Validation Sign-Off

- [ ] `nyquist_compliant: true` when phase execute complete

**Approval:** pending
