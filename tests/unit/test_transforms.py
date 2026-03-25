"""Unit tests for src/trading_crab_lib/transforms.py"""

import copy
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from trading_crab_lib.config import load
from trading_crab_lib.transforms import (
    add_cross_ratios,
    add_yield_curve_features,
    apply_log_transforms,
    apply_gap_fill,
    apply_derivatives,
    engineer_all,
    select_features,
)


# ── add_cross_ratios ───────────────────────────────────────────────────────

class TestAddCrossRatios:
    def test_all_ten_columns_added(self, raw_macro_df):
        result = add_cross_ratios(raw_macro_df)
        expected = [
            "div_yield2", "price_div", "price_gdp", "price_gdp2", "price_gnp2",
            "div_minus_baa", "credit_spread", "real_price2", "real_price3",
            "real_price_gdp2",
        ]
        for col in expected:
            assert col in result.columns, f"Missing column: {col}"

    def test_input_columns_preserved(self, raw_macro_df):
        result = add_cross_ratios(raw_macro_df)
        for col in raw_macro_df.columns:
            assert col in result.columns

    def test_div_yield2_formula(self, raw_macro_df):
        result = add_cross_ratios(raw_macro_df)
        expected = raw_macro_df["dividend"] / raw_macro_df["sp500"]
        pd.testing.assert_series_equal(result["div_yield2"], expected, check_names=False)

    def test_credit_spread_formula(self, raw_macro_df):
        result = add_cross_ratios(raw_macro_df)
        expected = (raw_macro_df["fred_baa"] - raw_macro_df["fred_aaa"]) / 100.0
        pd.testing.assert_series_equal(result["credit_spread"], expected, check_names=False)

    def test_does_not_mutate_input(self, raw_macro_df):
        original_cols = list(raw_macro_df.columns)
        add_cross_ratios(raw_macro_df)
        assert list(raw_macro_df.columns) == original_cols


# ── apply_log_transforms ───────────────────────────────────────────────────

class TestApplyLogTransforms:
    def test_adds_log_columns(self, raw_macro_df):
        cols = ["sp500", "gdp"]
        result = apply_log_transforms(raw_macro_df, cols)
        assert "log_sp500" in result.columns
        assert "log_gdp" in result.columns

    def test_log_values_correct(self, raw_macro_df):
        result = apply_log_transforms(raw_macro_df, ["sp500"])
        expected = np.log(raw_macro_df["sp500"].clip(lower=1e-9))
        pd.testing.assert_series_equal(result["log_sp500"], expected, check_names=False)

    def test_clips_at_1e9(self, quarterly_index):
        df = pd.DataFrame({"x": [-5.0, 0.0, 1.0, 100.0]},
                          index=quarterly_index[:4])
        result = apply_log_transforms(df, ["x"])
        assert np.all(np.isfinite(result["log_x"].values))

    def test_skips_missing_column(self, raw_macro_df):
        # Should not raise; just skip
        result = apply_log_transforms(raw_macro_df, ["nonexistent_col"])
        assert "log_nonexistent_col" not in result.columns

    def test_does_not_mutate_input(self, raw_macro_df):
        original_cols = list(raw_macro_df.columns)
        apply_log_transforms(raw_macro_df, ["sp500"])
        assert list(raw_macro_df.columns) == original_cols


# ── select_features ────────────────────────────────────────────────────────

class TestSelectFeatures:
    def test_keeps_requested_columns(self, raw_macro_df):
        result = select_features(raw_macro_df, ["sp500", "gdp"])
        assert list(result.columns) == ["sp500", "gdp"]

    def test_keeps_market_code_if_present(self, raw_macro_df):
        df = raw_macro_df.copy()
        df["market_code"] = 0
        result = select_features(df, ["sp500"])
        assert "market_code" in result.columns

    def test_no_market_code_if_absent(self, raw_macro_df):
        result = select_features(raw_macro_df, ["sp500"])
        assert "market_code" not in result.columns

    def test_missing_cols_silently_skipped(self, raw_macro_df):
        result = select_features(raw_macro_df, ["sp500", "does_not_exist"])
        assert "sp500" in result.columns
        assert "does_not_exist" not in result.columns


# ── apply_gap_fill ─────────────────────────────────────────────────────────

class TestApplyGapFill:
    def test_interior_nans_filled(self, quarterly_index):
        vals = np.array([1.0, np.nan, np.nan, 4.0, 5.0,
                         6.0, 7.0, 8.0, 9.0, 10.0,
                         11.0, 12.0, 13.0, 14.0, 15.0,
                         16.0, 17.0, 18.0, 19.0, 20.0])
        df = pd.DataFrame({"x": vals}, index=quarterly_index)
        result = apply_gap_fill(df)
        assert result["x"].isna().sum() == 0

    def test_no_nans_unchanged(self, quarterly_index):
        vals = np.arange(20, dtype=float)
        df = pd.DataFrame({"x": vals}, index=quarterly_index)
        result = apply_gap_fill(df)
        pd.testing.assert_series_equal(result["x"], df["x"])

    def test_market_code_not_filled(self, quarterly_index):
        vals = np.array([1.0, np.nan, 3.0] + [4.0] * 17)
        df = pd.DataFrame(
            {"x": vals, "market_code": [0, np.nan, 1] + [0] * 17},
            index=quarterly_index,
        )
        result = apply_gap_fill(df)
        # market_code NaN at index 1 should NOT be touched by gap fill
        assert np.isnan(result["market_code"].iloc[1])
        # x should still fill using row 0 and 2 even though market_code was NaN on row 1
        assert not np.isnan(result["x"].iloc[1])

    def test_does_not_mutate_input(self, quarterly_index):
        vals = np.array([1.0, np.nan, 3.0] + [4.0] * 17)
        df = pd.DataFrame({"x": vals}, index=quarterly_index)
        original_vals = df["x"].copy()
        apply_gap_fill(df)
        pd.testing.assert_series_equal(df["x"], original_vals)

    def test_single_non_nan_value_does_not_crash(self, quarterly_index):
        """np.gradient needs ≥2 points; sparse columns must not raise."""
        vals = np.array([np.nan] * 19 + [1.0])
        df = pd.DataFrame({"x": vals}, index=quarterly_index)
        result = apply_gap_fill(df)
        assert len(result) == 20


# ── apply_derivatives ──────────────────────────────────────────────────────

class TestApplyDerivatives:
    def test_three_derivative_columns_added(self, quarterly_index):
        df = pd.DataFrame(
            {"x": np.linspace(1, 20, 20)},
            index=quarterly_index,
        )
        result = apply_derivatives(df)
        assert "x_d1" in result.columns
        assert "x_d2" in result.columns
        assert "x_d3" in result.columns

    def test_market_code_has_no_derivatives(self, quarterly_index):
        df = pd.DataFrame(
            {"x": np.linspace(1, 20, 20), "market_code": np.zeros(20)},
            index=quarterly_index,
        )
        result = apply_derivatives(df)
        assert "market_code_d1" not in result.columns
        assert "market_code_d2" not in result.columns

    def test_sparse_market_code_does_not_skip_derivatives(self, quarterly_index):
        """Overlay labels must not define derivative support (regression: PCA n_samples≈4 bug)."""
        mc = np.full(20, np.nan)
        mc[[5, 6, 7]] = [0.0, 1.0, 2.0]  # only 3 labeled quarters
        df = pd.DataFrame(
            {"x": np.linspace(1, 20, 20), "market_code": mc},
            index=quarterly_index,
        )
        result = apply_derivatives(df, window=1)
        assert result["x_d1"].notna().sum() >= 15

    def test_linear_series_has_constant_d1(self, quarterly_index):
        """Derivative of a linear series should be roughly constant."""
        df = pd.DataFrame(
            {"x": np.linspace(0, 1, 20)},
            index=quarterly_index,
        )
        result = apply_derivatives(df, window=1)
        d1 = result["x_d1"].dropna()
        # All values should be nearly the same (constant slope)
        assert d1.std() < d1.mean() * 0.1


# ── add_yield_curve_features ───────────────────────────────────────────────

class TestAddYieldCurveFeatures:
    def test_builds_three_spreads_when_rates_present(self, quarterly_index):
        rng = np.random.default_rng(7)
        n = len(quarterly_index)
        df = pd.DataFrame(
            {
                "fred_gs10": rng.uniform(3.0, 8.0, n),
                "fred_gs2": rng.uniform(1.0, 6.0, n),
                "fred_tb3ms": rng.uniform(0.5, 5.0, n),
            },
            index=quarterly_index,
        )
        out = add_yield_curve_features(df)
        assert np.allclose(out["yc_10y_2y"], df["fred_gs10"] - df["fred_gs2"])
        assert np.allclose(out["yc_10y_3m"], df["fred_gs10"] - df["fred_tb3ms"])
        assert np.allclose(out["yc_2y_3m"], df["fred_gs2"] - df["fred_tb3ms"])

    def test_no_columns_when_rates_missing(self, quarterly_index):
        df = pd.DataFrame({"fred_gs10": [4.0] * 20}, index=quarterly_index)
        out = add_yield_curve_features(df)
        assert "yc_10y_2y" not in out.columns


# ── engineer_all (Phase 17 macro smoke) ───────────────────────────────────

class TestEngineerAllExpandedMacro:
    """Synthetic frame + narrowed feature lists — exercises yc_* + log_fred_* path."""

    @pytest.fixture
    def macro_df_v12(self, quarterly_index):
        rng = np.random.default_rng(42)
        n = len(quarterly_index)
        return pd.DataFrame(
            {
                "dividend": rng.uniform(10, 60, n),
                "sp500": rng.uniform(800, 4000, n),
                "gdp": rng.uniform(8000, 22000, n),
                "fred_gdp": rng.uniform(8000, 22000, n),
                "fred_gnp": rng.uniform(7500, 21000, n),
                "div_yield": rng.uniform(0.01, 0.05, n),
                "fred_baa": rng.uniform(3.0, 9.0, n),
                "fred_aaa": rng.uniform(2.5, 8.0, n),
                "cpi": rng.uniform(150, 280, n),
                "fred_cpi": rng.uniform(150, 280, n),
                "sp500_adj": rng.uniform(800, 4000, n),
                "10yr_ustreas": rng.uniform(2.0, 6.0, n),
                "fred_gs10": rng.uniform(3.0, 9.0, n),
                "fred_gs2": rng.uniform(2.0, 6.0, n),
                "fred_tb3ms": rng.uniform(0.5, 6.0, n),
                "fred_vix": rng.uniform(12, 45, n),
                "fred_unrate": rng.uniform(3.5, 9.0, n),
                "fred_m2sl": rng.uniform(5000, 25000, n),
                "fred_m2ns": rng.uniform(3000, 20000, n),
                "fred_houst": rng.uniform(400, 1800, n),
                "fred_umcsent": rng.uniform(55, 105, n),
            },
            index=quarterly_index,
        )

    def test_engineer_all_no_exception_and_clustering_columns(self, macro_df_v12):
        cfg = copy.deepcopy(load())
        cfg["features"]["initial_features"] = [
            "credit_spread",
            "div_minus_baa",
            "10yr_ustreas",
            "fred_gs10",
            "fred_tb3ms",
            "fred_gs2",
            "log_fred_vix",
            "log_fred_unrate",
            "log_fred_m2sl",
            "log_fred_m2ns",
            "log_fred_houst",
            "log_fred_umcsent",
            "yc_10y_2y",
            "yc_10y_3m",
            "yc_2y_3m",
        ]
        cfg["features"]["clustering_features"] = [
            "yc_10y_2y_d1",
            "yc_10y_2y_d2",
            "yc_10y_3m_d1",
            "yc_10y_3m_d2",
            "yc_2y_3m_d1",
            "yc_2y_3m_d2",
            "log_fred_vix_d1",
            "log_fred_vix_d2",
            "fred_gs2_d1",
            "fred_gs2_d2",
        ]
        out = engineer_all(macro_df_v12, cfg, causal=False)
        assert "yc_10y_2y_d1" in out.columns
        assert "log_fred_vix_d1" in out.columns
        assert "fred_gs2_d1" in out.columns
        assert out.drop(columns=["market_code"], errors="ignore").notna().all().all()

    def test_engineer_all_causal_mode_same_columns(self, macro_df_v12):
        cfg = copy.deepcopy(load())
        cfg["features"]["initial_features"] = [
            "credit_spread",
            "fred_gs10",
            "fred_tb3ms",
            "fred_gs2",
            "log_fred_vix",
            "yc_10y_2y",
        ]
        cfg["features"]["clustering_features"] = [
            "yc_10y_2y_d1",
            "log_fred_vix_d1",
        ]
        out_nc = engineer_all(macro_df_v12, cfg, causal=False)
        out_c = engineer_all(macro_df_v12, cfg, causal=True)
        assert list(out_nc.columns) == list(out_c.columns)
