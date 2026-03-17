from __future__ import annotations

import pandas as pd

from market_regime.diagnostics import (
    normalize_100,
    percentile_rank,
    rolling_zscore,
    rrg_for_benchmark,
)


def test_rolling_zscore_constant_series() -> None:
    s = pd.Series([1.0, 1.0, 1.0])
    z = rolling_zscore(s)
    assert (z == 0.0).all()


def test_percentile_rank_simple() -> None:
    s = pd.Series([1.0, 2.0, 3.0, 4.0])
    pct = percentile_rank(s)
    assert 0.99 >= pct >= 0.74  # last point near 100th percentile


def test_normalize_100_centering() -> None:
    s = pd.Series([1.0, 2.0, 3.0, 4.0])
    norm = normalize_100(s)
    assert abs(norm.mean() - 100.0) < 1e-6


def test_rrg_for_benchmark_quadrants() -> None:
    idx = pd.date_range("2000-01-01", periods=60, freq="W")
    prices = pd.DataFrame(
        {
            "SPY": 100 + pd.Series(range(60), index=idx),
            "TLT": 90 + pd.Series(range(60), index=idx),
            "GLD": 80 + pd.Series(range(0, 120, 2), index=idx),
        }
    )
    df = rrg_for_benchmark(prices, "SPY", lookback=52)
    # Should produce entries for TLT and GLD
    assets = set(df["asset"])
    assert {"TLT", "GLD"} <= assets
    assert set(df["quadrant"]).issubset({"LEADING", "WEAKENING", "LAGGING", "IMPROVING"})

