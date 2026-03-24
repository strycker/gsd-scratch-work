# Phase 27 — Execution summary

**Plan:** `27-v1-2-pipeline-weekly-e2e-01-PLAN.md`  
**Executed:** 2026-03-24  
**Requirements:** SIGNAL-10, SIGNAL-11, TACTICS-10, MODEL-10, MODEL-11, EMAIL-10, INSTALL-20

## Shipped

- **`run_pipeline.py`:** `resolve_pipeline_step_order` — steps **8**/**9** before **7** when **7** is requested with **8**/**9**; `log.info` + console print actual order.
- **`src/trading_crab_lib/prediction/dashboard_model.py`:** `resolve_current_regime_model_path` — **`dashboard.regime_model`** `rf` \| `gb`.
- **`config/settings.yaml`:** `dashboard.regime_model: rf`.
- **`step7_dashboard` + `pipelines/07_dashboard.py`:** use resolver; GB missing → RF warning.
- **`scripts/run_weekly_report.py`:** default **`2,3,4,5,6,8,9,7`** / **`1,2,3,4,5,6,8,9,7`** (`--full`).
- **`RUNBOOK.md`**, **`scripts/README.md`:** document order + `regime_model`.
- **`tests/unit/test_run_pipeline_step_order.py`:** step order + model path tests.

## Verification

```bash
PYTHONPATH=src python3 -m pytest tests/unit/test_run_pipeline_step_order.py -q
```

## Next

`$gsd-audit-milestone` — confirm **v1.2** milestone audit **passed**.
