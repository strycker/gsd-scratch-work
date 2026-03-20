"""Tests for partial macro_raw column merge (avoid full refresh when one source lags)."""

from __future__ import annotations

import pandas as pd
import pytest

from trading_crab_lib.ingestion import macro_partial


@pytest.fixture
def tiny_cfg():
    return {
        "data": {"start_date": "2000-01-01"},
        "fred": {
            "series": {
                "AAA": {"name": "fred_aaa", "shift": False},
            }
        },
        "multpl": {
            "datasets": [
                ["sp500", "x", "http://example.com", "num"],
            ]
        },
    }


def test_merge_missing_calls_only_multpl_when_only_multpl_gap(
    tiny_cfg, monkeypatch: pytest.MonkeyPatch
) -> None:
    idx = pd.date_range("2000-03-31", periods=2, freq="QE")
    base = pd.DataFrame(index=idx)
    base["fred_aaa"] = [1.0, 1.1]

    fred_calls = {"n": 0}
    multpl_calls = {"n": 0}

    def fake_fred(_cfg):
        fred_calls["n"] += 1
        return pd.DataFrame({"fred_aaa": [9.0, 9.0]}, index=idx)

    def fake_multpl(_cfg):
        multpl_calls["n"] += 1
        return pd.DataFrame({"sp500": [100.0, 101.0]}, index=idx)

    monkeypatch.setattr(
        "trading_crab_lib.ingestion.fred.fetch_all",
        fake_fred,
    )
    monkeypatch.setattr(
        "trading_crab_lib.ingestion.multpl.fetch_all",
        fake_multpl,
    )

    out = macro_partial.merge_missing_macro_columns(base, {"sp500"}, tiny_cfg)
    assert multpl_calls["n"] == 1
    assert fred_calls["n"] == 0
    assert "sp500" in out.columns
    assert out["fred_aaa"].tolist() == [1.0, 1.1]


def test_merge_missing_calls_fred_when_only_fred_gap(
    tiny_cfg, monkeypatch: pytest.MonkeyPatch
) -> None:
    idx = pd.date_range("2000-03-31", periods=2, freq="QE")
    base = pd.DataFrame({"sp500": [1.0, 2.0]}, index=idx)

    fred_calls = {"n": 0}
    multpl_calls = {"n": 0}

    def fake_fred(_cfg):
        fred_calls["n"] += 1
        return pd.DataFrame({"fred_aaa": [3.0, 4.0]}, index=idx)

    def fake_multpl(_cfg):
        multpl_calls["n"] += 1
        return pd.DataFrame(index=idx)

    monkeypatch.setattr("trading_crab_lib.ingestion.fred.fetch_all", fake_fred)
    monkeypatch.setattr("trading_crab_lib.ingestion.multpl.fetch_all", fake_multpl)

    out = macro_partial.merge_missing_macro_columns(base, {"fred_aaa"}, tiny_cfg)
    assert fred_calls["n"] == 1
    assert multpl_calls["n"] == 0
    assert out["fred_aaa"].tolist() == [3.0, 4.0]
