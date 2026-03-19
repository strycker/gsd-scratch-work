from __future__ import annotations

import logging
from pathlib import Path
from typing import Tuple

log = logging.getLogger(__name__)

FEATURES_SUPERVISED_FILENAME = "features_supervised.parquet"
FEATURES_NONCAUSAL_FILENAME = "features.parquet"


def select_step5_feature_path(
    processed_dir: Path,
    *,
    allow_noncausal_features: bool,
) -> Tuple[Path, str, bool]:
    """
    Select the feature parquet path for step 5.

    Locked behavior (Phase 3 plan-04):
      - Prefer/require `features_supervised.parquet` by default.
      - If missing, only fall back to `features.parquet` when
        `allow_noncausal_features=True`.
      - When falling back, emit a loud warning and return `noncausal_used=True`.
    """
    supervised_path = processed_dir / FEATURES_SUPERVISED_FILENAME
    if supervised_path.exists():
        return supervised_path, "features_supervised", False

    noncausal_path = processed_dir / FEATURES_NONCAUSAL_FILENAME
    if not allow_noncausal_features:
        raise FileNotFoundError(
            f"{supervised_path} not found.\n"
            "Step 5 leakage guardrail requires causal features.\n\n"
            "To generate them, run step 2:\n"
            "  python run_pipeline.py --steps 2\n\n"
            "If you intentionally want to run with non-causal features, re-run with:\n"
            "  --allow-noncausal-features\n\n"
            f"Fallback file would be: {noncausal_path}"
        )

    if not noncausal_path.exists():
        raise FileNotFoundError(
            f"Neither {supervised_path} nor {noncausal_path} exists.\n"
            "If you intended to use non-causal features, ensure step 2 output "
            "was written to data/processed/."
        )

    log.warning(
        "NONCAUSAL_USED=true — step 5 falling back from %s to %s.",
        supervised_path.name,
        noncausal_path.name,
    )
    return noncausal_path, "features", True

