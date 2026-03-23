#!/usr/bin/env python3
"""
Merge missing macro_raw columns into ``data/raw/macro_raw.parquet`` using FRED/multpl.

Use when step 1 logs "cached macro_raw missing … trying partial FRED/multpl merge"
but you want to persist the repair without a full ``--refresh`` ingest, or to
retry a targeted merge after fixing network/credentials.

  PYTHONPATH=src python scripts/repair_macro_raw.py

Requires the same environment as the pipeline (``FRED_API_KEY`` in ``.env`` for FRED).
If columns are still missing after this script, run:

  python run_pipeline.py --steps 1 --refresh
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO / "src") not in sys.path:
    sys.path.insert(0, str(REPO / "src"))


def main() -> int:
    import pandas as pd

    from trading_crab_lib.checkpoints import CheckpointManager
    from trading_crab_lib.config import load
    from trading_crab_lib.ingestion.macro_partial import (
        REQUIRED_MACRO_RAW_FOR_STEP2,
        merge_missing_macro_columns,
    )

    cfg = load()
    raw_path = REPO / "data" / "raw" / "macro_raw.parquet"
    if not raw_path.exists():
        print(f"No {raw_path} — run: python run_pipeline.py --steps 1", file=sys.stderr)
        return 1

    df = pd.read_parquet(raw_path)
    missing = REQUIRED_MACRO_RAW_FOR_STEP2 - set(df.columns)
    if not missing:
        print("macro_raw already has all required columns for step 2.")
        return 0

    print(f"Merging missing columns ({len(missing)}): {sorted(missing)}")
    try:
        out = merge_missing_macro_columns(df, missing, cfg)
    except Exception as exc:
        print(f"merge_missing_macro_columns failed: {exc}", file=sys.stderr)
        return 1

    still = REQUIRED_MACRO_RAW_FOR_STEP2 - set(out.columns)
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_parquet(raw_path)
    CheckpointManager().save(out, "macro_raw")
    added = set(out.columns) - set(df.columns)
    print(f"Wrote {raw_path} (+{len(added)} columns: {sorted(added)})")
    if still:
        print(
            f"Still missing ({len(still)}): {sorted(still)} — "
            "try: python run_pipeline.py --steps 1 --refresh",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
