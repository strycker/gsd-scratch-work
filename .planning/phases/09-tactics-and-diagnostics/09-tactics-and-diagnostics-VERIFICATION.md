---
phase: 09-tactics-and-diagnostics
verified: 2026-03-19T00:00:00Z
status: passed
score: 2/2 requirements satisfied (TACTICS-01, TACTICS-02)
human_verification:
  - test: "Run steps through 9 or `python pipelines/09_tactics.py`; open outputs/reports/tactics_signals.parquet"
    expected: "Rows per ETF with tactics_label in {buy_hold, swing, stand_aside}."
    why_human: "Labels depend on live price volatility/trend shapes."
  - test: "Generate weekly_report.md after tactics file exists"
    expected: "Markdown includes ## Tactics section listing buckets when parquet readable."
    why_human: "Optional section is best validated by eye."
---

# Phase 9: Tactics & Diagnostics Integration — Verification

**Phase goal (ROADMAP):** Tactics layer integrated into the core pipeline and weekly narrative.  
**Audit closure:** Phase 13 — evidence for TACTICS-01, TACTICS-02.  
**Status:** **passed**.

## Requirement coverage

| ID | Description | Status | Evidence |
|----|-------------|--------|----------|
| TACTICS-01 | Pipeline step computes per-asset tactics metrics/labels and writes a stable machine-readable artifact | ✓ | `run_pipeline.py` defines **`step9_tactics`** as `STEPS[9]`. `pipelines/09_tactics.py` loads `data/raw/asset_prices.parquet` and `data/regimes/cluster_labels.parquet` (`balanced_cluster`), calls `trading_crab_lib.tactics.compute_tactics_metrics` and `classify_tactics`, writes **`outputs/reports/tactics_signals.parquet`** (column `tactics_label` among others). Skips gracefully with log if inputs missing. |
| TACTICS-02 | Weekly report surfaces tactics consistent with diagnostics/recommendations | ✓ | `trading_crab_lib.reporting.write_weekly_report_md` (optional block): if `outputs/reports/tactics_signals.parquet` exists, reads parquet and appends **## Tactics** with bullet lists for `buy_hold`, `swing`, `stand_aside`; swallow read errors so a bad file does not break the report. |

## Artifact (canonical filename)

| File | Producer |
|------|----------|
| `outputs/reports/tactics_signals.parquet` | `pipelines/09_tactics.py` line `out_path = out_dir / "tactics_signals.parquet"` |

Matches code reference and `reporting.write_weekly_report_md` path: `OUTPUT_DIR / "reports" / "tactics_signals.parquet"`.

## Code map

| Module / script | Role |
|-----------------|------|
| `trading_crab_lib.tactics` | `compute_tactics_metrics`, `classify_tactics` |
| `pipelines/09_tactics.py` | Standalone CLI parity with step 9 |
| `run_pipeline.py` | Orchestration + `STEPS[9]` |

## Tests

| Test file | Coverage |
|-----------|----------|
| `tests/test_tactics.py` | Metrics columns + classification smoke on synthetic prices |

## `key_links`

| From | To | Via |
|------|----|-----|
| `run_pipeline.py --steps …,9` | `tactics_signals.parquet` | `step9_tactics` |
| `tactics_signals.parquet` | `weekly_report.md` | `write_weekly_report_md` optional tactics section |
| `config/settings.yaml` (`tactics`) | Label thresholds | Passed into `compute_tactics_metrics` / `classify_tactics` (see Phase 10 for test + config depth) |

## Notes

- Diagnostics parquet from step 8 and tactics from step 9 are **separate** artifacts; the weekly report ties them together at the **narrative** layer (tactics section + prior regime/recommendation content).

## Evidence checklist (audit)

- [x] `STEPS[9]` registered in `run_pipeline.py` with label “Tactics signals”.
- [x] `pipelines/09_tactics.py` writes exactly `outputs/reports/tactics_signals.parquet`.
- [x] `write_weekly_report_md` reads the same path under `trading_crab_lib` `OUTPUT_DIR` layout.
- [x] Classification functions live in `src/trading_crab_lib/tactics.py`.
- [x] `tests/test_tactics.py` exercises metrics + labels on synthetic data.

## Ordering

- Recommended: run step 9 **after** steps 3 (cluster labels) and 6 (prices), consistent with `pipelines/09_tactics.py` inputs.

## Revision history

- 2026-03-19 — Phase 13 audit: initial `*-VERIFICATION.md` for roadmap Phase 9.
