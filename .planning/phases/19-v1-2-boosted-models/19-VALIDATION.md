---
phase: 19
slug: v1-2-boosted-models
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-24
validated: 2026-03-24
---

# Phase 19 — Validation Strategy

> MODEL-10 / MODEL-11 — boosted models; gap-closure **Phase 26** added this file for Nyquist parity.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | `pyproject.toml` |
| **Quick run command** | `PYTHONPATH=src python -m pytest tests/test_models_boosting.py tests/test_models_interpret_tree.py -q` |

---

## Automated commands (from `19-VERIFICATION.md`)

```bash
. .venv/bin/activate
export PYTHONPATH=src
python -m pytest tests/test_models_boosting.py tests/test_models_interpret_tree.py -q
python -c "from trading_crab_lib.config import load; load(); print('ok')"
```

---

## Per-Task Verification Map

| Task | Requirement | Evidence |
|------|-------------|----------|
| Phase 26 gap closure | MODEL-10, MODEL-11 | `19-VERIFICATION.md` + pytest block above |
