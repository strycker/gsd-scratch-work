from __future__ import annotations

import numpy as np
import pandas as pd

from market_regime.config import load
from market_regime.tactics import compute_tactics_metrics, classify_tactics


def test_tactics_classification_basic() -> None:
    cfg = load()
    cfg.setdefault("tactics", {})
    cfg["tactics"]["vol_windows"] = [2, 4, 8]
    cfg["tactics"]["vol_bands"] = {"low": 0.01, "high": 0.05}
    cfg["tactics"]["trend_windows"] = [4]
    cfg["tactics"]["trend_min_slope"] = 0.0
    cfg["tactics"]["corr_lookback"] = 8

    idx = pd.date_range("2000-01-01", periods=50, freq="D")
    # Smooth strong uptrend → buy_hold
    p_bh = pd.Series(np.linspace(100, 150, len(idx)), index=idx)
    # Medium-vol uptrend → swing / buy_hold (either is acceptable)
    rng = np.random.default_rng(0)
    p_sw = pd.Series(
        np.linspace(100, 140, len(idx)) + rng.normal(scale=1.0, size=len(idx)),
        index=idx,
    )
    # High-vol flat → stand_aside
    p_sa = pd.Series(120 + rng.normal(scale=5.0, size=len(idx)), index=idx)

    prices = pd.DataFrame({"BH": p_bh, "SW": p_sw, "SA": p_sa})
    regimes = pd.Series(0, index=pd.date_range("2000-03-31", periods=10, freq="QE"))

    metrics = compute_tactics_metrics(prices, regimes, cfg)
    assert {"vol_2", "vol_4", "slope_4", "corr_spy"}.issubset(metrics.columns)

    tactics_df = classify_tactics(metrics, cfg)
    labels = tactics_df["tactics_label"].to_dict()

    assert labels["BH"] == "buy_hold"
    assert labels["SA"] == "stand_aside"
    assert labels["SW"] in {"buy_hold", "swing"}

