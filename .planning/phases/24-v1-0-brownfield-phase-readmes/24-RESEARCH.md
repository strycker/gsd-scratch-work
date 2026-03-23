# Phase 24 — Research (CLOSURE-02 brownfield READMEs)

**Question:** What must each brownfield README contain so GSD hygiene and human auditors can find evidence?

## Findings

### Directory inventory (pre-plan)

| Phase dir | VERIFICATION (basename) | VALIDATION |
|-----------|-------------------------|------------|
| `04-regime-conditional-etf-portfolio-behavior` | `04-regime-conditional-etf-portfolio-behavior-VERIFICATION.md` | `04-VALIDATION.md` |
| `05-recommendations-machine-readable-outputs` | `05-recommendations-machine-readable-outputs-VERIFICATION.md` | `05-VALIDATION.md` |
| `06-weekly-report-pipeline` | `06-weekly-report-pipeline-VERIFICATION.md` | `06-VALIDATION.md` |
| `07-portfolio-and-email-integration` | `07-portfolio-and-email-integration-VERIFICATION.md` | `07-VALIDATION.md` |
| `08-data-signals-diagnostics` | `08-data-signals-diagnostics-VERIFICATION.md` | `08-VALIDATION.md` |
| `09-tactics-and-diagnostics` | `09-tactics-and-diagnostics-VERIFICATION.md` | `09-VALIDATION.md` |
| `10-tactics-install` | `10-tactics-install-VERIFICATION.md` | `10-VALIDATION.md` |
| `11-core-cleanup` | `11-core-cleanup-VERIFICATION.md` | `11-VALIDATION.md` |

None of these eight directories had a **`README.md`** at research time (only phase 24’s own folder had a stub README).

### Entrypoint patterns (from existing VERIFICATION files)

- **04 / 06 / assets:** `run_pipeline.py` steps, `pipelines/06_asset_returns.py`, `pipelines/07_dashboard.py`, `src/trading_crab_lib/asset_returns.py`, `reporting/`.
- **05:** Machine-readable outputs under `outputs/reports/`, dashboard CSV, weekly report hooks.
- **07 / email:** `scripts/run_weekly_report.py`, `RUNBOOK.md`, `trading_crab_lib/email.py`.
- **08:** `pipelines/08_diagnostics.py` (or `08_diagnostics` naming per repo), diagnostics config in `settings.yaml`.
- **09 / 10 / 11:** `tactics.py`, tactics parquet, `scripts/README.md`, `settings.yaml` tactics keys, tests cited in VERIFICATION.

Executors should **copy concrete paths from the target phase’s VERIFICATION** into that phase’s README (one paragraph + bullet list), not invent APIs.

## Risks

- **Link rot:** Relative links must match actual filenames (see table).
- **Duplication:** READMEs are indexes, not copies of VERIFICATION — keep under ~40 lines each.

## Validation Architecture

- **Type:** Documentation-only; no production code.
- **Primary gate:** `test -f` / `grep` on each new `README.md` for required substrings (`VERIFICATION`, `VALIDATION`, `RUNBOOK.md` or `run_pipeline.py`).
- **Secondary:** `node .codex/get-shit-done/bin/gsd-tools.cjs validate health` remains green (docs-only change).
- **Manual:** Spot-check relative links in a browser or IDE preview.

## RESEARCH COMPLETE
