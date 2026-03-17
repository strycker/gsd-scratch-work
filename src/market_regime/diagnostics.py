from __future__ import annotations

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

