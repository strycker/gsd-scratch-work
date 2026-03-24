"""DATA-11: config-driven asset providers + ingestion contract (network-free)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

_INGEST = Path(__file__).resolve().parents[2] / "src" / "trading_crab_lib" / "ingestion"


def _load_assets():
    path = _INGEST / "assets.py"
    qualname = "_tc_assets_providers_test"
    spec = importlib.util.spec_from_file_location(qualname, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[qualname] = mod
    spec.loader.exec_module(mod)
    return mod


_assets_mod = _load_assets()
fetch_all = _assets_mod.fetch_all


def _qe_series(name: str, v: float = 100.0) -> pd.Series:
    qe = pd.Timestamp("2020-03-31")
    return pd.Series([v], index=pd.DatetimeIndex([qe]), name=name)


def test_stooq_disabled_never_calls_stooq_functions(monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = {
        "assets": {
            "etfs": ["SPY"],
            "providers": {"yfinance": False, "stooq": False, "openbb": False},
        },
        "data": {"start_date": "2018-01-01", "end_date": "2020-12-31"},
    }
    def _no_stooq_one(*_a, **_k):
        raise AssertionError("_fetch_ticker_stooq should not be called")

    def _no_stooq_bulk(*_a, **_k):
        raise AssertionError("_fetch_tickers_stooq should not be called")

    monkeypatch.setattr(_assets_mod, "_fetch_ticker_stooq", _no_stooq_one)
    monkeypatch.setattr(_assets_mod, "_fetch_tickers_stooq", _no_stooq_bulk)
    out = fetch_all(cfg)
    assert out.empty


def test_fetch_all_index_name_and_columns_subset() -> None:
    spy = _qe_series("SPY", 101.0)
    cfg = {
        "assets": {"etfs": ["SPY"], "providers": {"yfinance": True, "stooq": False, "openbb": False}},
        "data": {"start_date": "2018-01-01", "end_date": "2020-12-31"},
    }
    with patch.object(_assets_mod, "_batch_yfinance", return_value=({"SPY": spy}, False)):
        with patch.object(_assets_mod, "_ssl_bypass_curl_session", return_value=None):
            out = fetch_all(cfg)
    assert out.index.name == "date"
    assert list(out.columns) == ["SPY"]


def test_partial_yahoo_then_stooq_fills_second_ticker() -> None:
    spy = _qe_series("SPY", 100.0)
    qqq = _qe_series("QQQ", 200.0)
    cfg = {
        "assets": {
            "etfs": ["SPY", "QQQ"],
            "providers": {"yfinance": True, "stooq": True, "openbb": False},
        },
        "data": {"start_date": "2018-01-01", "end_date": "2020-12-31"},
    }

    def fake_batch(tickers, start, end, session=None):
        assert tickers == ["SPY", "QQQ"]
        return ({"SPY": spy}, False)

    def no_ssl_missing(missing, start, end):
        return {}

    calls: list[str] = []

    def fake_stooq_ticker(ticker, start, end):
        calls.append(ticker)
        return qqq if ticker == "QQQ" else pd.Series(name=ticker, dtype=float)

    with patch.object(_assets_mod, "_batch_yfinance", side_effect=fake_batch):
        with patch.object(_assets_mod, "_ssl_bypass_curl_session", return_value=None):
            with patch.object(_assets_mod, "_fetch_missing_with_ssl_bypass", side_effect=no_ssl_missing):
                with patch.object(_assets_mod, "_fetch_ticker_stooq", side_effect=fake_stooq_ticker):
                    out = fetch_all(cfg)

    assert "QQQ" in calls
    assert set(out.columns) == {"SPY", "QQQ"}
    assert out.index.name == "date"


def test_provider_flags_default_true() -> None:
    assert _assets_mod._provider_flags({"assets": {}}) == {
        "yfinance": True,
        "stooq": True,
        "openbb": True,
    }
