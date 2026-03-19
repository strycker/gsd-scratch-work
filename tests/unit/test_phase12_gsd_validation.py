"""
Nyquist hooks for Phase 12 (PORT/UX/REPORT gap-closure verification).

Keeps automated coverage lightweight: reporting helpers + weekly script contract.
Full pipeline E2E remains manual (see phase VERIFICATION.md human_verification blocks).
"""

from __future__ import annotations

import pandas as pd
import pytest

from trading_crab_lib.reporting import generate_recommendation, write_weekly_report_md


def test_generate_recommendation_uses_current_portfolio_weights() -> None:
    """UX-01: deltas reflect moving from current holdings toward blended target."""
    target = pd.Series({"SPY": 0.5, "TLT": 0.3, "GLD": 0.2})
    current = pd.Series({"SPY": 0.4, "TLT": 0.35, "GLD": 0.25})
    rec = generate_recommendation(target, current_weights=current, threshold=0.02)
    assert not rec.empty
    spy = rec.loc["SPY"]
    assert spy["signal"] == "BUY"  # +10% vs target
    assert spy["delta_pct"] == pytest.approx(10.0, rel=0.01)


def test_write_weekly_report_md_contains_regime_and_buy_section(tmp_path) -> None:
    """REPORT-02: markdown has regime line and recommendations section."""
    rec = pd.DataFrame(
        {
            "current_pct": [0.0, 50.0],
            "target_pct": [25.0, 25.0],
            "delta_pct": [25.0, -25.0],
            "signal": ["BUY", "SELL"],
        },
        index=["GLD", "SPY"],
    )
    probs = {0: 0.35, 1: 0.4, 2: 0.25}
    out = write_weekly_report_md(
        current_regime=1,
        regime_name="Test Regime",
        regime_probabilities=probs,
        rec_df=rec,
        transition_row=None,
        output_path=tmp_path / "weekly_report.md",
    )
    text = out.read_text(encoding="utf-8")
    assert "Current regime:" in text or "**Current regime:**" in text
    assert "Recommendations" in text
    assert "GLD" in text or "BUY" in text
