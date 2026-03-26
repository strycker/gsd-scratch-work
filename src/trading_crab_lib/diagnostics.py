"""Ratio and relative-rotation (RRG-style) diagnostics for weekly reporting.

Builds z-scores, percentile ranks, and trigger classifications for configured
price ratios, plus simplified RS-Ratio / RS-Momentum quadrants vs a benchmark.
Outputs are consumed by ``reporting`` (embedded in markdown reports) and are
deterministic given price history — they do not drive model training.
"""

# Interpretation: z-scores and RRG quadrants describe *relative* positioning — not causal macro forecasts.

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


def rolling_zscore(series: pd.Series) -> pd.Series:
    """Return a simple z-score over the full history (mean/std)."""
    clean = series.dropna()
    if clean.empty:
        return pd.Series(index=series.index, dtype=float)
    mu = clean.mean()
    sigma = clean.std()
    if sigma == 0 or np.isnan(sigma):
        return pd.Series(0.0, index=series.index)
    return (series - mu) / sigma


def percentile_rank(series: pd.Series) -> float:
    """Percentile rank of the last non-NaN observation vs history (0–1)."""
    clean = series.dropna()
    if clean.empty:
        return float("nan")
    last = clean.iloc[-1]
    # Use strictly-less-than so the last observation is below 100% even when
    # it is the maximum, which is often more intuitive for diagnostics and
    # matches the unit test expectation.
    return float((clean < last).mean())


def normalize_100(series: pd.Series) -> pd.Series:
    """Normalize series to have mean 100 and std 10 (roughly JdK-style scale)."""
    clean = series.dropna()
    if clean.empty:
        return pd.Series(100.0, index=series.index)
    mu = clean.mean()
    sigma = clean.std()
    if sigma == 0 or np.isnan(sigma):
        return pd.Series(100.0, index=series.index)
    return 100.0 + 10.0 * (series - mu) / sigma


def rrg_for_benchmark(
    prices: pd.DataFrame,
    benchmark: str,
    lookback: int = 52,
) -> pd.DataFrame:
    """
    Compute basic RS-Ratio and RS-Momentum for each asset vs a benchmark.

    Uses a simple smoothing + normalization scheme that is deterministic and
    easy to test; it does not attempt to exactly match proprietary RRG math.
    """
    if benchmark not in prices.columns:
        return pd.DataFrame()
    if len(prices) < lookback:
        lookback = len(prices)
    window_prices = prices.iloc[-lookback:]
    rs = window_prices.divide(window_prices[benchmark], axis=0)
    rs_smooth = rs.rolling(window=min(13, lookback), min_periods=1).mean()
    rs_ratio = rs_smooth.apply(normalize_100, axis=0)
    rs_mom_raw = rs_ratio.diff()
    rs_momentum = rs_mom_raw.apply(normalize_100, axis=0)

    as_of = window_prices.index[-1]
    records: list[dict] = []
    for col in prices.columns:
        if col == benchmark:
            continue
        rr = rs_ratio[col].dropna()
        mm = rs_momentum[col].dropna()
        if rr.empty or mm.empty:
            continue
        rr_last = rr.iloc[-1]
        mm_last = mm.iloc[-1]
        if rr_last >= 100 and mm_last >= 100:
            quadrant = "LEADING"
        elif rr_last >= 100 and mm_last < 100:
            quadrant = "WEAKENING"
        elif rr_last < 100 and mm_last < 100:
            quadrant = "LAGGING"
        else:
            quadrant = "IMPROVING"
        records.append(
            {
                "as_of": as_of,
                "asset": col,
                "benchmark": benchmark,
                "rs_ratio": rr_last,
                "rs_momentum": mm_last,
                "quadrant": quadrant,
            }
        )
    return pd.DataFrame.from_records(records)


def merge_trigger_config(
    defaults: dict[str, Any] | None,
    overrides: dict[str, Any] | None,
) -> dict[str, Any]:
    """Merge per-ratio `triggers` overrides onto `trigger_defaults` from settings."""
    out = dict(defaults or {})
    for k, v in (overrides or {}).items():
        out[k] = v
    return out


def evaluate_ratio_triggers(
    latest_zscore: float,
    percentile: float,
    defaults: dict[str, Any] | None,
    overrides: dict[str, Any] | None = None,
) -> tuple[str, str]:
    """
    Classify a ratio reading using YAML-first rules.

    Priority:
      1. |z| >= z_abs_min  → trigger ``stretched``, detail cites threshold
      2. percentile >= percentile_high → ``elevated``
      3. percentile <= percentile_low → ``depressed``
      4. else → ``neutral``

    If ``trigger_defaults`` is missing or empty, returns (``neutral``, ``no trigger rules configured``).
    """
    rules = merge_trigger_config(defaults, overrides)
    if not rules:
        return "neutral", "no trigger rules configured"

    z = latest_zscore
    p = percentile
    z_min = rules.get("z_abs_min")
    p_hi = rules.get("percentile_high")
    p_lo = rules.get("percentile_low")

    if z_min is not None and not np.isnan(z) and abs(z) >= float(z_min):
        return "stretched", f"|z|={abs(z):.2f} (threshold {z_min})"
    if p_hi is not None and not np.isnan(p) and p >= float(p_hi):
        return "elevated", f"percentile={p:.2f} (high ≥ {p_hi})"
    if p_lo is not None and not np.isnan(p) and p <= float(p_lo):
        return "depressed", f"percentile={p:.2f} (low ≤ {p_lo})"
    return "neutral", ""


def compute_ratios_diagnostics(prices: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    """
    Build the ratio diagnostics table (latest value, z-score, percentile, triggers).

    Reads ``cfg['diagnostics']['ratios']`` and optional ``trigger_defaults`` /
    per-ratio ``triggers`` overrides.
    """
    diag_cfg = cfg.get("diagnostics") or {}
    ratios_cfg = diag_cfg.get("ratios") or []
    defaults = diag_cfg.get("trigger_defaults")
    if prices.empty or not ratios_cfg:
        return pd.DataFrame()

    records: list[dict[str, Any]] = []
    for item in ratios_cfg:
        name = item.get("name")
        num = item.get("numerator")
        den = item.get("denominator")
        if not name or not num or not den:
            continue
        if num not in prices.columns or den not in prices.columns:
            continue
        ratio_series = prices[num] / prices[den]
        z = rolling_zscore(ratio_series)
        pct = percentile_rank(ratio_series)
        latest = ratio_series.dropna().iloc[-1] if not ratio_series.dropna().empty else float("nan")
        latest_z = z.dropna().iloc[-1] if not z.dropna().empty else float("nan")
        ov = item.get("triggers") or item.get("trigger_overrides")
        trig, detail = evaluate_ratio_triggers(latest_z, pct, defaults, ov)
        row: dict[str, Any] = {
            "name": name,
            "numerator": num,
            "denominator": den,
            "latest_value": latest,
            "latest_zscore": latest_z,
            "percentile": pct,
            "trigger": trig,
            "trigger_detail": detail,
        }
        records.append(row)
    return pd.DataFrame.from_records(records)
