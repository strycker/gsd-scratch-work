# Phase 6 — Weekly Report Pipeline: Research

## Goal

Make the weekly regime + recommendation report **runnable in one shot** and **easy to schedule** (e.g. cron). Optionally support **delivery** (e.g. email or a file ready to paste into an email).

## Current state (post Phase 5)

- **run_pipeline.py** already runs steps 1–7 with `--steps 1,2,3,4,5,6,7` (or subset).
- Step 7 writes **outputs/reports/weekly_report.md** and **recommendation_bundle.parquet**, **trade_recommendations.csv**.
- No dedicated "weekly run" entry point; no timestamped outputs; no email or send step.

## Options

| Option | Description | Effort |
|--------|-------------|--------|
| **Runner script** | Single script (e.g. `scripts/run_weekly_report.sh` or `python -m market_regime.weekly`) that invokes the pipeline with a fixed step list (e.g. 2–7 using cached ingest, or 1–7 full). | Low |
| **Timestamped outputs** | Copy or write `weekly_report.md` (and optionally bundle CSV) to a dated path (e.g. `outputs/reports/weekly_2026-03-16.md`) so each run is archived. | Low |
| **Email-ready body** | Produce a plain-text or HTML body (e.g. `outputs/reports/email_body.txt`) from `weekly_report.md` so the user can paste into Gmail/Outlook or pipe to `sendmail`. | Low |
| **Send email** | Integrate with SMTP or a provider (SendGrid, etc.) to send the report to a configured address. Requires secrets and dependency. | Medium |

## Recommendation

- **In scope for Phase 6:** Runner script + timestamped report copy + optional email_body.txt (no SMTP).
- **Defer:** Actual SMTP/send (can be Phase 6.1 or later when user wants it).

## Dependencies

- Phases 1–5 (ingest, features, cluster, regime label, predict, asset returns, dashboard) must run successfully.
- `config/portfolio.yaml` and `config/regime_labels.yaml` in place.
- Optional: `FRED_API_KEY` and network for step 1 if full refresh; otherwise steps 2–7 can use cached data.
