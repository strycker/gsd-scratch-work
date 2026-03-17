# Scripts

## run_weekly_report.py

Single entry point for the **weekly regime + recommendation report**.

**Usage (from repo root):**

```bash
python scripts/run_weekly_report.py              # steps 2–7 (cached ingest)
python scripts/run_weekly_report.py --full       # steps 1–7 (full refresh)
python scripts/run_weekly_report.py --plots      # also save figures
python scripts/run_weekly_report.py --verbose   # DEBUG logging
```

**Outputs:**

- Runs the pipeline (steps 2–7 by default, or 1–7 with `--full`).
- Copies `outputs/reports/weekly_report.md` → `outputs/reports/weekly_YYYY-MM-DD.md`.
- Writes `outputs/reports/email_body.txt` (plain text for email paste or sendmail).

**Cron example** (e.g. every Monday 9am):

```cron
0 9 * * 1 cd /path/to/gsd-scratch-work && python scripts/run_weekly_report.py
```

Replace `/path/to/gsd-scratch-work` with your repo root. Ensure your environment (venv, `FRED_API_KEY` in `.env` if using `--full`) is active or sourced in the cron job if needed.
