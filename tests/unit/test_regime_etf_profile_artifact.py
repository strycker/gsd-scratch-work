"""
Regression guard for REGIME-02 ETF / proxy return profiling by regime.

Canonical runtime artifact: data/regimes/etf_behavior_by_regime.parquet (step 6, behavior_tables).
Macro-feature profiles remain data/regimes/profiles.parquet (build_profiles, step 4).
"""

from __future__ import annotations

import pandas as pd

from trading_crab_lib.asset_returns import behavior_tables

EXPECTED_COLS = (
    "regime",
    "asset",
    "median_return",
    "q25",
    "q75",
    "hit_rate",
    "n_quarters",
    "signal_absolute",
    "tertile",
    "signal_display",
    "score_relative",
    "score_absolute",
    "rank",
)


def test_behavior_tables_column_contract_for_regime_etf_artifact() -> None:
    idx = pd.period_range("2020Q1", periods=12, freq="Q")
    rng = pd.Series([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1], index=idx, dtype=int)
    spy = pd.Series(range(12), index=idx, dtype=float) * 0.01
    gld = pd.Series(range(11, -1, -1), index=idx, dtype=float) * 0.005
    returns = pd.DataFrame({"SPY": spy, "GLD": gld}, index=idx)

    out = behavior_tables(returns, rng)
    assert not out.empty
    for col in EXPECTED_COLS:
        assert col in out.columns, f"missing column {col!r}"
