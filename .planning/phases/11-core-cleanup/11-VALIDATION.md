---
phase: 11
slug: core-cleanup
status: complete
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-17
---

## Phase 11: Core Cleanup & Env Sanity

**Goal:** Ensure directory layout, date handling, and style consistency are sane on any machine so later phases rest on a clean foundation.

### Wave 0 (after execution) checklist

- **Directory layout**
  - [x] `scripts/setup.sh` creates:
    - [x] `data/raw`
    - [x] `data/processed`
    - [x] `data/regimes`
    - [x] `data/checkpoints`
    - [x] `outputs/plots`
    - [x] `outputs/models`
    - [x] `outputs/reports`
  - [x] `run_pipeline` steps 1–2 and 6–7 create their target dirs (raw, processed, regimes, outputs) before writing artifacts.

- **End date handling**
  - [x] `config/settings.yaml` uses `data.end_date: null` with a comment explaining that null means "use today's date".
  - [x] `ingestion/fred.py` uses `end = cfg["data"]["end_date"] or str(date.today())` so null correctly resolves to the current date at runtime.

- **Future imports / style**
  - [x] `src/market_regime/ingestion/fred.py` includes `from __future__ import annotations` at the top.
  - [x] `src/market_regime/ingestion/multpl.py` includes `from __future__ import annotations` at the top.

### Nyquist validation (required to mark complete)

- [x] Manual/checklist verification:
  - [x] Running `python run_pipeline.py --refresh --recompute --steps 1,2` completes successfully and writes `data/raw/macro_raw.parquet` and `data/processed/features.parquet` to the expected locations.
  - [x] `ls -R data outputs` shows the expected directory layout with no unexpected phantom dirs.
- [x] Tests:
  - [x] `pytest tests/test_pipelines_ingest_features.py::test_step01_ingest_writes_macro_raw_without_network -q`
  - [x] `pytest tests/test_models_regime.py::test_current_regime_models_and_probabilities -q`
- [x] This file updated:
  - [x] `status: complete`
  - [x] `nyquist_compliant: true`
  - [x] `wave_0_complete: true`

