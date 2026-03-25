# Plan 01 — Hybrid summary (Phase 27 — gap closure)

**Plan:** `27-v1-2-pipeline-weekly-e2e-01-PLAN.md`  
**Phase narrative:** `27-SUMMARY.md`

## As-built

- `run_pipeline.py`: `resolve_pipeline_step_order` runs **8** and **9** before **7** when all are requested; logged execution order.
- `src/trading_crab_lib/prediction/dashboard_model.py`: `resolve_current_regime_model_path` for **`dashboard.regime_model`** `rf` \| `gb`.
- `config/settings.yaml`: `dashboard.regime_model` (default `rf`); step 7 / `pipelines/07_dashboard.py` use resolver.
- `scripts/run_weekly_report.py`: default steps include **8, 9** before **7**; docs in `RUNBOOK.md`, `scripts/README.md`.
- `tests/unit/test_run_pipeline_step_order.py`: order + model path behavior.

## Plan fidelity

- Close **`v1.2-MILESTONE-AUDIT.md`** integration gaps: weekly path includes diagnostics/tactics in same run; weekly script defaults aligned; dashboard loads correct regime pickle when GB enabled.

## Delta from plan

- **Complete:** Per `27-SUMMARY.md` shipped list and pytest command.
- **Deferred to v1.3:** Milestone **`$gsd-audit-milestone`** / v1.3 consolidation (PyPI, submodule parity, etc.) — out of phase 27 scope.
