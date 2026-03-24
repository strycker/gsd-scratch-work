---
phase: 18
slug: v1-2-signal-diagnostics
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-24
validated: 2026-03-24
---

# Phase 18 — Validation Strategy

> SIGNAL-10 / SIGNAL-11 — diagnostics layer; gap-closure **Phase 26** added this file for Nyquist parity.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | `pyproject.toml` |
| **Quick run command** | `PYTHONPATH=src python -m pytest tests/unit/test_diagnostics_ratios.py tests/unit/test_diagnostics_rrg.py -q` |

---

## Automated commands (from `18-VERIFICATION.md`)

```bash
. .venv/bin/activate
PYTHONPATH=src python -m pytest tests/unit/test_diagnostics_ratios.py tests/unit/test_diagnostics_rrg.py tests/unit/test_weekly_report_diagnostics.py tests/unit/test_phase12_gsd_validation.py -q
PYTHONPATH=src python -c "from trading_crab_lib.config import load; load(); print('ok')"
```

---

## Per-Task Verification Map

| Task | Requirement | Evidence |
|------|-------------|----------|
| Phase 26 gap closure | SIGNAL-10, SIGNAL-11 | `18-VERIFICATION.md` + pytest block above |
