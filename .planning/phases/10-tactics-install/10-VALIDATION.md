---
phase: 10
slug: tactics-install
status: complete
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-17
---

## Phase 10: Tactics Layer + Install & Env Automation

**Goal:** Add a per-asset tactics layer (buy-and-hold / swing-trade / stand-aside) and provide a one-shot installer + environment health check for Trading-Crab.

### Wave 0 (after execution) checklist

- **Tactics layer (10A)**
  - [x] `config/settings.yaml` includes a `tactics` section with vol/trend/corr thresholds.
  - [x] `src/market_regime/tactics.py` exists and computes:
    - [x] Volatility metrics (`vol_<window>`)
    - [x] Trend slopes (`slope_<window>`)
    - [x] Correlation vs SPY (`corr_spy`)
    - [x] `current_regime`
    - [x] `tactics_label` ∈ {`buy_hold`, `swing`, `stand_aside`}.
  - [x] Step 9 in `run_pipeline.py` (`step9_tactics`) reads ETF prices + cluster labels and writes:
    - [x] `outputs/reports/tactics_signals.parquet`
  - [x] `write_weekly_report_md` in `reporting.py` appends a **Tactics** section when `tactics_signals.parquet` is present.

- **Install & env automation (10B)**
  - [x] `scripts/install_trading_crab.sh` exists and:
    - [x] Uses conda `${TRADING_CRAB_CONDA_ENV:-py310}` when available, else `.venv/`.
    - [x] Installs the project with dev extras via `pip install -e ".[dev]"`.
    - [x] Scaffolds `.env` and `config/email.local.yaml` from example files when missing.
    - [x] Runs a small pytest smoke set (ingest + model) and reports success/failure.
  - [x] `scripts/check_env.sh` exists and:
    - [x] Prints Python and pytest paths/versions.
    - [x] Verifies `market_regime` can be imported.
    - [x] Runs a tiny pytest smoke test.
  - [x] `README.md` documents:
    - [x] One-shot install via `bash scripts/install_trading_crab.sh`.
    - [x] Env health check via `bash scripts/check_env.sh`.
  - [x] `scripts/README.md` documents both new scripts and their behavior.

### Nyquist validation (required to mark complete)

- [x] Add/extend unit tests:
  - [x] `tests/test_tactics.py` covers metrics + label behavior on synthetic series.
  - [x] Existing ingest/model tests remain green under the new install/CI flow.
- [x] Manual verification:
  - [x] `python run_pipeline.py --steps 9` writes `tactics_signals.parquet` without error once upstream steps are run.
  - [x] Weekly report includes a **Tactics** section when `tactics_signals.parquet` is present.
- [x] All relevant tests pass under the supported environment (e.g. conda `py310`):
  - [x] `pytest tests/test_tactics.py -q`
  - [x] `pytest tests/test_models_regime.py::test_current_regime_models_and_probabilities -q`
  - [x] `pytest tests/test_pipelines_ingest_features.py::test_step01_ingest_writes_macro_raw_without_network -q`
- [x] This file updated:
  - [x] `status: complete`
  - [x] `nyquist_compliant: true`
  - [x] `wave_0_complete: true`

