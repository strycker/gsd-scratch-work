"""Tests for macro_raw checkpoint column repair (run_pipeline step 1)."""

from __future__ import annotations

import sys
import types

import pandas as pd

if sys.modules.get("dotenv") is None:  # pragma: no cover - env without dev deps
    _m = types.ModuleType("dotenv")
    _m.load_dotenv = lambda *a, **k: None  # type: ignore[assignment]
    sys.modules["dotenv"] = _m


def test_repair_macro_raw_missing_columns_fills_from_checkpoint() -> None:
    from run_pipeline import _repair_macro_raw_missing_columns

    dates = pd.date_range("2000-03-31", periods=3, freq="QE")
    thin = pd.DataFrame({"fred_gdp": [10.0, 11.0, 12.0], "fred_cpi": [1.0, 1.1, 1.2]}, index=dates)
    full = thin.copy()
    for c in ("cpi", "dividend", "div_yield", "sp500", "sp500_adj", "gdp"):
        full[c] = float(len(c))

    class _FakeCM:
        def load(self, name: str) -> pd.DataFrame:
            if name == "macro_raw":
                return full
            raise FileNotFoundError(name)

    required = {"fred_gdp", "fred_cpi", "cpi", "dividend", "div_yield", "sp500", "sp500_adj", "gdp"}
    out, added = _repair_macro_raw_missing_columns(thin, required, _FakeCM())

    assert set(added) == {"cpi", "dividend", "div_yield", "sp500", "sp500_adj", "gdp"}
    assert required <= set(out.columns)
    assert len(out) == len(dates)


def test_repair_macro_raw_no_checkpoint_noop() -> None:
    from run_pipeline import _repair_macro_raw_missing_columns

    dates = pd.date_range("2000-03-31", periods=2, freq="QE")
    thin = pd.DataFrame({"a": [1.0, 2.0]}, index=dates)

    class _NoCkpt:
        def load(self, name: str) -> pd.DataFrame:
            raise FileNotFoundError(name)

    out, added = _repair_macro_raw_missing_columns(thin, {"a", "b"}, _NoCkpt())
    assert added == []
    assert list(out.columns) == ["a"]
