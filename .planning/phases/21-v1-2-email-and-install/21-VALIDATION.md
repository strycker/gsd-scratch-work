---
phase: 21
slug: v1-2-email-and-install
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-23
validated: 2026-03-23
---

# Phase 21 — Validation Strategy

> EMAIL-10 + INSTALL-20 (email path hardening + setup parity).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | `pyproject.toml` |
| **Full regression (phase 21)** | `PYTHONPATH=src python -m pytest tests/test_gitignore_secrets.py tests/test_email_weekly.py tests/test_scripts_weekly_report.py -q` |
| **Gitignore only** | `PYTHONPATH=src python -m pytest tests/test_gitignore_secrets.py -q` |

---

## Per-Task Verification Map

| Task | Requirement | Automated Command | Status |
|------|-------------|-------------------|--------|
| 21-01-01 | INSTALL-20 | `grep -q email.example.yaml scripts/setup.sh` | ✅ |
| 21-01-02 | EMAIL-10 docs | `grep -n send-email RUNBOOK.md` | ✅ |
| 21-01-03 | Gitignore + email regression | `pytest tests/test_gitignore_secrets.py tests/test_email_weekly.py tests/test_scripts_weekly_report.py -q` | ✅ |
| — | `setup.sh` syntax | `bash -n scripts/setup.sh` | ✅ |

---

## Manual-Only

| Behavior | Why manual |
|----------|------------|
| SMTP delivery to real inbox | Network + credentials |

---

## Validation Audit 2026-03-23

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Requirements with automated verification | 4 (incl. `bash -n`) |
| Manual-only | 1 (SMTP to real inbox) |

**Commands run:** `grep` / `pytest` (19 passed) / `bash -n` — all green.

---

## Validation Sign-Off

- [x] `nyquist_compliant: true` when phase execute complete

**Approval:** automated verification complete; SMTP smoke remains operator manual-only.
