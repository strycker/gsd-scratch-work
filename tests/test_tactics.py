from __future__ import annotations

import numpy as np
import pandas as pd

from trading_crab_lib.config import load
from trading_crab_lib.tactics import classify_tactics, compute_tactics_metrics


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
    assert "as_of" in metrics.columns and "quarter_end" in metrics.columns
    assert "last_price" in metrics.columns
    assert "soft_stop_z" in metrics.columns
    assert "entry_bias_score" in metrics.columns
    assert pd.Timestamp(metrics["as_of"].iloc[0]) == pd.Timestamp(idx.max())

    tactics_df = classify_tactics(metrics, cfg)
    labels = tactics_df["tactics_label"].to_dict()

    assert labels["BH"] == "buy_hold"
    assert labels["SA"] == "stand_aside"
    assert labels["SW"] in {"buy_hold", "swing"}


def test_entry_bias_score_in_unit_interval() -> None:
    cfg = load()
    cfg.setdefault("tactics", {})
    cfg["tactics"]["vol_windows"] = [5, 20]
    cfg["tactics"]["trend_windows"] = [5, 20]
    cfg["tactics"]["entry_bias"] = {"short_slope_window": 5, "long_slope_window": 20}
    idx = pd.date_range("2000-01-01", periods=80, freq="D")
    p = pd.Series(np.linspace(100, 200, len(idx)), index=idx)
    prices = pd.DataFrame({"X": p})
    regimes = pd.Series(0, index=pd.date_range("2000-03-31", periods=10, freq="QE"))
    metrics = compute_tactics_metrics(prices, regimes, cfg)
    eb = float(metrics.loc["X", "entry_bias_score"])
    assert -1.0 - 1e-9 <= eb <= 1.0 + 1e-9


def test_v1_2_max_vol_can_stand_aside_when_v1_buy_hold() -> None:
    """Multi-horizon max vol can classify stand_aside while legacy v1 uses mid window only."""
    cfg = load()
    cfg.setdefault("tactics", {})
    cfg["tactics"]["vol_bands"] = {"low": 0.01, "high": 0.25}
    cfg["tactics"]["trend_min_slope"] = 0.0
    cfg["tactics"]["vol_aggregate"] = "max"

    metrics = pd.DataFrame(
        {
            "vol_2": [0.50],
            "vol_4": [0.02],
            "vol_8": [0.02],
            "slope_4": [0.01],
            "corr_spy": [0.5],
        },
        index=["X"],
    )

    cfg["tactics"]["classification_version"] = "v1_2"
    out_v12 = classify_tactics(metrics, cfg)
    assert out_v12.loc["X", "tactics_label"] == "stand_aside"

    cfg["tactics"]["classification_version"] = "v1"
    out_v1 = classify_tactics(metrics, cfg)
    assert out_v1.loc["X", "tactics_label"] == "swing"


def test_min_corr_spy_forces_stand_aside() -> None:
    cfg = load()
    cfg.setdefault("tactics", {})
    cfg["tactics"]["vol_bands"] = {"low": 0.01, "high": 0.99}
    cfg["tactics"]["min_corr_spy"] = 0.99
    metrics = pd.DataFrame(
        {
            "vol_4": [0.02],
            "slope_4": [0.05],
            "corr_spy": [0.1],
        },
        index=["X"],
    )
    out = classify_tactics(metrics, cfg)
    assert out.loc["X", "tactics_label"] == "stand_aside"
