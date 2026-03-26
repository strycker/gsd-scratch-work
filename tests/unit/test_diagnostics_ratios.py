from __future__ import annotations

import numpy as np
import pandas as pd

from trading_crab_lib.diagnostics import (
    compute_ratios_diagnostics,
    evaluate_ratio_triggers,
    merge_trigger_config,
)


def test_merge_trigger_config_overrides_defaults() -> None:
    m = merge_trigger_config({"z_abs_min": 2.0}, {"z_abs_min": 3.0})
    assert m["z_abs_min"] == 3.0


def test_evaluate_ratio_triggers_stretched() -> None:
    t, d = evaluate_ratio_triggers(2.5, 0.5, {"z_abs_min": 2.0, "percentile_high": 0.9}, None)
    assert t == "stretched"
    assert "2.50" in d or "2.5" in d


def test_evaluate_ratio_triggers_elevated_percentile() -> None:
    t, d = evaluate_ratio_triggers(0.1, 0.95, {"z_abs_min": 5.0, "percentile_high": 0.9}, None)
    assert t == "elevated"


def test_evaluate_ratio_triggers_neutral() -> None:
    t, d = evaluate_ratio_triggers(0.2, 0.5, {"z_abs_min": 2.0, "percentile_high": 0.99}, None)
    assert t == "neutral"
    assert d == ""


def test_evaluate_ratio_triggers_no_rules() -> None:
    t, d = evaluate_ratio_triggers(99.0, 0.5, None, None)
    assert t == "neutral"
    assert "no trigger" in d.lower()


def test_compute_ratios_diagnostics_columns() -> None:
    idx = pd.date_range("2020-01-01", periods=80, freq="W")
    prices = pd.DataFrame(
        {
            "USO": np.linspace(10, 12, 80),
            "GLD": np.linspace(100, 102, 80),
            "TLT": np.linspace(90, 91, 80),
            "XLB": np.linspace(50, 52, 80),
        },
        index=idx,
    )
    cfg = {
        "diagnostics": {
            "trigger_defaults": {
                "z_abs_min": 0.01,
                "percentile_high": 0.99,
                "percentile_low": 0.01,
            },
            "ratios": [
                {"name": "Oil:Gold", "numerator": "USO", "denominator": "GLD"},
            ],
        }
    }
    df = compute_ratios_diagnostics(prices, cfg)
    assert not df.empty
    assert "trigger" in df.columns
    assert "trigger_detail" in df.columns
    assert df.iloc[0]["trigger"] in ("neutral", "stretched", "elevated", "depressed")
