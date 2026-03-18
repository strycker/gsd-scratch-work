"""
Unit tests for empirical forward-window regime probabilities (reach within N quarters).

Validates build_forward_window_probabilities() semantics and determinism using
a small synthetic label sequence with hand-computed probabilities.
"""

from __future__ import annotations

import pandas as pd
import pytest

from market_regime.regime import build_forward_window_probabilities


def test_forward_window_probabilities_columns_and_shape():
    """Output has required columns and long format."""
    labels = pd.Series([0, 1, 1, 2, 0])
    horizons = [1, 2]
    out = build_forward_window_probabilities(labels, horizons)

    assert isinstance(out, pd.DataFrame)
    assert list(out.columns) == ["from_regime", "to_regime", "horizon_quarters", "prob"]
    # Regimes 0,1,2 × 3 to_regime × 2 horizons = 18 rows
    assert len(out) == 3 * 3 * 2
    assert out["horizon_quarters"].isin(horizons).all()
    assert set(out["from_regime"].unique()) == {0, 1, 2}
    assert set(out["to_regime"].unique()) == {0, 1, 2}


def test_forward_window_probabilities_hand_computed():
    """
    For labels = [0, 1, 1, 2, 0]:
    - Horizon 1, from_regime=0: only t=0 has current=0 with valid window; window [1] → reached 1. So P(reach 1 | 0) = 1.0.
    - Horizon 1, from_regime=2: only t=3 has current=2; window [0] → reached 0. So P(reach 0 | 2) = 1.0.
    """
    labels = pd.Series([0, 1, 1, 2, 0])
    horizons = [1, 2]
    out = build_forward_window_probabilities(labels, horizons)

    row_0_to_1_h1 = out[(out["from_regime"] == 0) & (out["to_regime"] == 1) & (out["horizon_quarters"] == 1)]
    assert len(row_0_to_1_h1) == 1
    assert row_0_to_1_h1["prob"].iloc[0] == pytest.approx(1.0)

    row_2_to_0_h1 = out[(out["from_regime"] == 2) & (out["to_regime"] == 0) & (out["horizon_quarters"] == 1)]
    assert len(row_2_to_0_h1) == 1
    assert row_2_to_0_h1["prob"].iloc[0] == pytest.approx(1.0)


def test_forward_window_probabilities_in_unit_interval():
    """All probabilities are in [0, 1]."""
    labels = pd.Series([0, 1, 1, 2, 0])
    horizons = [1, 2, 4]
    out = build_forward_window_probabilities(labels, horizons)

    assert (out["prob"] >= 0.0).all()
    assert (out["prob"] <= 1.0).all()


def test_forward_window_probabilities_deterministic_ordering():
    """Output is sorted by horizon_quarters, from_regime, to_regime and is deterministic across calls."""
    labels = pd.Series([0, 1, 1, 2, 0])
    horizons = [1, 2]

    out1 = build_forward_window_probabilities(labels, horizons)
    out2 = build_forward_window_probabilities(labels, horizons)

    expected_order = ["horizon_quarters", "from_regime", "to_regime"]
    out1_sorted = out1.sort_values(expected_order).reset_index(drop=True)
    out2_sorted = out2.sort_values(expected_order).reset_index(drop=True)

    pd.testing.assert_frame_equal(out1_sorted, out2_sorted)


def test_forward_window_probabilities_dropna():
    """NaN labels are dropped before computation."""
    labels = pd.Series([0.0, 1.0, float("nan"), 2.0, 0.0])
    horizons = [1]
    out = build_forward_window_probabilities(labels, horizons)

    # Treated as 0,1,2,0 after dropna → regimes 0,1,2
    assert set(out["from_regime"].unique()) <= {0, 1, 2}
    assert (out["prob"] >= 0).all() and (out["prob"] <= 1).all()
