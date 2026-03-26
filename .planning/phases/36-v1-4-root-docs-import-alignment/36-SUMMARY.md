# Phase 36 — Execution summary (DOC-ALIGN-10)

**Plan:** `36-v1-4-root-docs-import-alignment-01-PLAN.md`  
**Executed:** 2026-03-26  
**Requirement:** DOC-ALIGN-10

## What shipped

- **`CLAUDE.md`** — Package **`trading_crab_lib`**; repository layout under **`src/trading_crab_lib/`**; **`CheckpointManager`** from **`trading_crab_lib.checkpoints`**; legacy gap pointer **`regime.py`** (not `regime/profiler.py`).
- **`README.md`** — Checkpoint listing snippet uses **`from trading_crab_lib.checkpoints import CheckpointManager`**.
- **`PITFALLS.md`**, **`ARCHITECTURE.md`**, **`STATE.md`** — Path strings **`src/trading_crab_lib/`**; portfolio reference **`reporting.py`**.
- **`.planning/phases/34-v1-3-library-documentation-pass/34-VALIDATION.md`** — **`nyquist_compliant: true`** (with approval note).
- **`.planning/phases/34-v1-3-library-documentation-pass/34-VERIFICATION.md`** — Automated checks / pytest counts refreshed (this execute).
- **`.planning/REQUIREMENTS.md`** — **DOC-ALIGN-10** complete; traceability row **Complete**.
- **`36-v1-4-root-docs-import-alignment-01-SUMMARY.md`** — hybrid **I001** summary beside **`01-PLAN.md`**.
- **`tests/unit/test_phase14_planning_validation.py`** — Accept **`milestone: v1.4`** in **`.planning/STATE.md`** (Nyquist hook).

## Verification

```bash
grep -E 'from market_regime|market_regime\.io' CLAUDE.md README.md
# exit 1 (no matches)

python -c "from trading_crab_lib.checkpoints import CheckpointManager; from trading_crab_lib.config import load"

make lint
pytest tests/ -q

node .codex/get-shit-done/bin/gsd-tools.cjs validate health
```

Expect **`validate health`**: `"status": "healthy"`, `info` [].
