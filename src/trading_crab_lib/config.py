"""
Configuration loading for the trading-crab pipeline.

**Why a single loader:** ``settings.yaml`` holds tunable parameters; secrets
(``FRED_API_KEY``) must never be committed. :func:`load` merges YAML with
environment variables after :func:`dotenv.load_dotenv`, so local ``.env`` and
CI env vars both work. Call :func:`load` once at process entry (``run_pipeline.py``
or a notebook kernel) and pass the resulting ``dict`` through the pipeline.
"""

# Economics: FRED series are official U.S. macro statistics (St. Louis Fed API).
# The API key is free; we never embed it in YAML so repos stay shareable.

from __future__ import annotations

import logging
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

from trading_crab_lib import CONFIG_DIR

log = logging.getLogger(__name__)


def load(settings_path: Path | None = None) -> dict:
    """Load ``settings.yaml`` and inject ``FRED_API_KEY`` from the environment.

    Args:
        settings_path: Explicit path to YAML. Defaults to ``CONFIG_DIR / "settings.yaml"``.

    Returns:
        Parsed configuration dict (same structure as ``config/settings.yaml``),
        with ``cfg["fred"]["api_key"]`` set from ``FRED_API_KEY`` (possibly ``None``).
    """
    load_dotenv()  # reads .env if present; env vars already set take priority

    # settings.yaml holds *tunable* knobs (dates, feature lists, ETF tickers).
    # Economic content lives there too: which macro series feed ratios, PCA width, cluster search bounds.
    path = settings_path or CONFIG_DIR / "settings.yaml"
    with open(path) as f:
        cfg = yaml.safe_load(f)

    # FRED key lives only in env — required for live macro download in step 1.
    fred_key = os.getenv("FRED_API_KEY")
    if not fred_key:
        log.warning("FRED_API_KEY not set — FRED ingestion will fail")
    cfg.setdefault("fred", {})["api_key"] = fred_key

    return cfg


def load_portfolio(portfolio_path: Path | None = None) -> dict[str, float]:
    """
    Load current portfolio weights from YAML (ticker -> weight fraction).
    Weights are normalized to sum to 1. Missing or empty file returns {}.
    """
    # Portfolio weights are fractions of capital (not dollar notionals); used in
    # reporting / recommendations, not in unsupervised clustering.
    path = portfolio_path or CONFIG_DIR / "portfolio.yaml"
    if not path.exists():
        log.debug("No portfolio file at %s", path)
        return {}
    with open(path) as f:
        raw = yaml.safe_load(f)
    if not raw or not isinstance(raw, dict):
        return {}
    # Accept numeric values only; normalize to sum = 1 so weights read as portfolio fractions.
    weights = {}
    for k, v in raw.items():
        if str(k).startswith("#"):
            continue
        try:
            w = float(v)
            if w > 0:
                weights[str(k).strip()] = w
        except (TypeError, ValueError):
            continue
    if not weights:
        return {}
    total = sum(weights.values())
    if total <= 0:
        return {}
    return {t: w / total for t, w in weights.items()}


def setup_logging(level: str = "INFO") -> None:
    """Configure the root logger with a consistent timestamped format.

    Args:
        level: Log level name (e.g. ``"INFO"``, ``"DEBUG"``).
    """
    logging.basicConfig(
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=getattr(logging, level.upper()),
    )
