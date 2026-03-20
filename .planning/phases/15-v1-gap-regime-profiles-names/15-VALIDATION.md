---
phase: 15
slug: v1-gap-regime-profiles-names
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-20
---

# Phase 15 — Validation strategy

## Quick commands

| Gate | Command |
|------|---------|
| ETF artifact test | `pytest tests/unit/test_regime_etf_profile_artifact.py -q` |
| Regime utils regression | `pytest tests/unit/test_regime.py -q` |
| YAML pins | `python -c "import yaml; from pathlib import Path; r=yaml.safe_load(Path('config/regime_labels.yaml').read_text()); assert set(r.keys())=={0,1,2,3,4}"` |

## Sampling

- After each task: run the row commands above.
- Before verify-work / milestone re-audit: both pytest lines + YAML assert.
