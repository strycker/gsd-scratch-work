---
phase: 17
slug: v1-2-expanded-macro-signals
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-24
validated: 2026-03-24
---

# Phase 17 — Validation Strategy

> DATA-10 — expanded macro & yield features; gap-closure **Phase 26** added this file for Nyquist parity with phases 20–25.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | `pyproject.toml` |
| **Quick run command** | `PYTHONPATH=src python -m pytest tests/unit/test_transforms.py tests/unit/test_fred_series_config.py -q` |
| **Full suite command** | Same as `17-VERIFICATION.md` automated block (includes `test_regime.py`) |

---

## Automated commands (from `17-VERIFICATION.md`)

```bash
. .venv/bin/activate
PYTHONPATH=src python -c "from trading_crab_lib.config import load; load(); print('ok', len(load()['features']['clustering_features']), 'clustering features')"
PYTHONPATH=src python -m pytest tests/unit/test_transforms.py tests/unit/test_fred_series_config.py tests/unit/test_regime.py -q
```

---

## Per-Task Verification Map

| Task | Requirement | Evidence |
|------|-------------|----------|
| Phase 26 gap closure | DATA-10 | `17-VERIFICATION.md` `status: passed` + pytest block above |
