---
phase: 15-v1-gap-regime-profiles-names
plan: 01
completed: 2026-03-20
---

# 15-v1-gap-regime-profiles-names-01 — Execution summary

**Plan:** `15-v1-gap-regime-profiles-names-01-PLAN.md`  
**Canonical phase narrative:** [`15-SUMMARY.md`](15-SUMMARY.md).

## Outcomes

- **REGIME-02** — Documented split: macro **`profiles.parquet`** (step 4) vs ETF behavior **`etf_behavior_by_regime.parquet`** (step 6); docstrings in **`src/trading_crab_lib/regime.py`** and **`pipelines/04_regime_label.py`**.
- **REGIME-03** — **`config/regime_labels.yaml`** pins clusters **0–4** only (`balanced_k: 5`); removed invalid key **5**.
- **Tests** — **`tests/unit/test_regime_etf_profile_artifact.py`** for `behavior_tables()` contract.
- **Phase 2 VERIFICATION** — **`02-regime-clustering-interpretation-VERIFICATION.md`** → **passed** for audit.

## Verification

```bash
pytest tests/unit/test_regime_etf_profile_artifact.py tests/unit/test_regime.py -q
python -c "import yaml; from pathlib import Path; r=yaml.safe_load(Path('config/regime_labels.yaml').read_text()); assert set(r.keys())=={0,1,2,3,4}"
```

See **15-SUMMARY.md** for full detail.
