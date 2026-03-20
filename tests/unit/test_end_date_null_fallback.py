"""
CORE-02: When cfg['data']['end_date'] is null/None (YAML `end_date: null`),
ingestion must use today's calendar date as the fetch window end — same as
`fred.py` and `assets.py` `... or str(date.today())` logic.

These modules are loaded via importlib so importing does not execute
`trading_crab_lib/__init__.py` (which requires python-dotenv at collection time).
"""

from __future__ import annotations

import importlib.util
import sys
import types
from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd

_INGEST = Path(__file__).resolve().parents[2] / "src" / "trading_crab_lib" / "ingestion"

# Minimal envs may lack fredapi; fred.py only needs a placeholder at import time
# (tests patch Fred before any network use). If fredapi is installed, use it.
try:
    import fredapi  # noqa: F401
except ImportError:
    _fredapi_stub = types.ModuleType("fredapi")

    class _FredStub:
        pass

    _fredapi_stub.Fred = _FredStub
    sys.modules["fredapi"] = _fredapi_stub


def _load_ingestion_module(stem: str, qualname: str):
    path = _INGEST / f"{stem}.py"
    spec = importlib.util.spec_from_file_location(qualname, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[qualname] = mod
    spec.loader.exec_module(mod)
    return mod


_fred_mod = _load_ingestion_module("fred", "_tc_fred_ingestion_under_test")
_assets_mod = _load_ingestion_module("assets", "_tc_assets_ingestion_under_test")
fetch_fred_all = _fred_mod.fetch_all
fetch_assets_all = _assets_mod.fetch_all


def test_fred_fetch_all_uses_today_when_end_date_is_null() -> None:
    fixed_today = date(2031, 7, 15)
    cfg = {
        "fred": {
            "api_key": "test-api-key",
            "series": {
                "GS10": {"name": "fred_gs10", "shift": False},
            },
        },
        "data": {
            "start_date": "2000-01-01",
            "end_date": None,
        },
    }

    idx = pd.date_range("2020-01-31", periods=2, freq="ME")
    mock_series = pd.Series([1.0, 2.0], index=idx)

    with patch.object(_fred_mod, "Fred") as mock_fred_cls:
        mock_instance = MagicMock()
        mock_fred_cls.return_value = mock_instance
        mock_instance.get_series.return_value = mock_series

        with patch.object(_fred_mod, "date") as mock_date:
            mock_date.today.return_value = fixed_today
            out = fetch_fred_all(cfg)

    mock_instance.get_series.assert_called()
    for call in mock_instance.get_series.call_args_list:
        observation_end = call.kwargs.get("observation_end")
        assert observation_end == str(fixed_today), (
            f"expected observation_end={fixed_today!s}, got {observation_end!r}"
        )
    assert not out.empty
    assert "fred_gs10" in out.columns


def test_fred_fetch_all_respects_explicit_end_date() -> None:
    cfg = {
        "fred": {
            "api_key": "test-api-key",
            "series": {"GS10": {"name": "fred_gs10", "shift": False}},
        },
        "data": {"start_date": "2000-01-01", "end_date": "2019-06-30"},
    }
    idx = pd.date_range("2019-01-31", periods=2, freq="ME")
    mock_series = pd.Series([3.0, 3.1], index=idx)

    with patch.object(_fred_mod, "Fred") as mock_fred_cls:
        mock_instance = MagicMock()
        mock_fred_cls.return_value = mock_instance
        mock_instance.get_series.return_value = mock_series

        with patch.object(_fred_mod, "date") as mock_date:
            mock_date.today.return_value = date(2099, 12, 31)
            fetch_fred_all(cfg)

    mock_instance.get_series.assert_called()
    end_kw = mock_instance.get_series.call_args.kwargs.get("observation_end")
    assert end_kw == "2019-06-30"
    mock_date.today.assert_not_called()


def test_assets_fetch_all_uses_today_when_end_date_is_null() -> None:
    fixed_today = date(2031, 8, 20)
    cfg = {
        "assets": {"etfs": ["SPY"]},
        "data": {
            "start_date": "2018-01-01",
            "end_date": None,
        },
    }

    qe = pd.Timestamp("2020-03-31")
    stub_series = pd.Series([100.0], index=pd.DatetimeIndex([qe]), name="SPY")

    with patch.object(_assets_mod, "_batch_yfinance") as mock_batch:
        mock_batch.return_value = ({"SPY": stub_series}, False)

        with patch.object(
            _assets_mod,
            "_ssl_bypass_curl_session",
            return_value=None,
        ):
            with patch.object(_assets_mod, "date") as mock_date:
                mock_date.today.return_value = fixed_today
                out = fetch_assets_all(cfg)

    mock_batch.assert_called_once()
    args, _kwargs = mock_batch.call_args
    assert args[0] == ["SPY"]
    assert args[1] == "2018-01-01"
    assert args[2] == str(fixed_today), f"end should be today as str, got {args[2]!r}"
    assert "SPY" in out.columns


def test_assets_fetch_all_respects_explicit_end_date() -> None:
    cfg = {
        "assets": {"etfs": ["SPY"]},
        "data": {"start_date": "2018-01-01", "end_date": "2020-12-31"},
    }
    stub_series = pd.Series(
        [101.0],
        index=pd.DatetimeIndex([pd.Timestamp("2020-03-31")]),
        name="SPY",
    )

    with patch.object(_assets_mod, "_batch_yfinance") as mock_batch:
        mock_batch.return_value = ({"SPY": stub_series}, False)

        with patch.object(
            _assets_mod,
            "_ssl_bypass_curl_session",
            return_value=None,
        ):
            with patch.object(_assets_mod, "date") as mock_date:
                mock_date.today.return_value = date(2099, 1, 1)
                fetch_assets_all(cfg)

    assert mock_batch.call_args[0][2] == "2020-12-31"
    mock_date.today.assert_not_called()
