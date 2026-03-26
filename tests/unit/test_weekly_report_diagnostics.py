from __future__ import annotations

import pandas as pd

from trading_crab_lib.reporting import write_weekly_report_md


def test_weekly_report_diagnostics_section(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("trading_crab_lib.OUTPUT_DIR", tmp_path)
    diag = tmp_path / "reports" / "diagnostics"
    diag.mkdir(parents=True)
    pd.DataFrame(
        {
            "name": ["Oil:Gold"],
            "latest_zscore": [2.1],
            "trigger": ["stretched"],
        }
    ).to_parquet(diag / "ratios_current.parquet")
    pd.DataFrame(
        {
            "benchmark": ["SPY"],
            "asset": ["GLD"],
            "quadrant": ["LEADING"],
            "rs_ratio": [102.0],
            "rs_momentum": [101.0],
        }
    ).to_parquet(diag / "rrg_current.parquet")

    rec = pd.DataFrame(
        {
            "current_pct": [100.0],
            "target_pct": [100.0],
            "delta_pct": [0.0],
            "signal": ["HOLD"],
        },
        index=["SPY"],
    )
    out = write_weekly_report_md(
        0,
        "R",
        {0: 1.0},
        rec,
        None,
        tmp_path / "weekly_report.md",
        cfg={"diagnostics": {"weekly_report_include": True}},
    )
    text = out.read_text(encoding="utf-8")
    assert "## Diagnostics" in text
    assert "Oil:Gold" in text
    assert "RRG quadrant" in text


def test_weekly_report_skips_diagnostics_when_disabled(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("trading_crab_lib.OUTPUT_DIR", tmp_path)
    diag = tmp_path / "reports" / "diagnostics"
    diag.mkdir(parents=True)
    pd.DataFrame({"name": ["A"], "latest_zscore": [1.0]}).to_parquet(
        diag / "ratios_current.parquet"
    )

    rec = pd.DataFrame(
        {
            "current_pct": [100.0],
            "target_pct": [100.0],
            "delta_pct": [0.0],
            "signal": ["HOLD"],
        },
        index=["SPY"],
    )
    out = write_weekly_report_md(
        0,
        "R",
        {0: 1.0},
        rec,
        None,
        tmp_path / "weekly_report.md",
        cfg={"diagnostics": {"weekly_report_include": False}},
    )
    text = out.read_text(encoding="utf-8")
    assert "## Diagnostics" not in text


def test_plot_diagnostics_ratios_saves_png(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("trading_crab_lib.plotting.PLOT_DIR", tmp_path)
    from trading_crab_lib import plotting
    from trading_crab_lib.runtime import RunConfig

    df = pd.DataFrame({"name": ["Oil:Gold"], "latest_zscore": [1.5]})
    rc = RunConfig(generate_plots=True, save_plots=True)
    plotting.plot_diagnostics_ratios_summary(df, rc)
    assert (tmp_path / "08_diagnostics_ratios.png").exists()


def test_plot_diagnostics_rrg_saves_png(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("trading_crab_lib.plotting.PLOT_DIR", tmp_path)
    from trading_crab_lib import plotting
    from trading_crab_lib.runtime import RunConfig

    df = pd.DataFrame(
        {
            "benchmark": ["SPY", "SPY"],
            "asset": ["GLD", "TLT"],
            "quadrant": ["LEADING", "LAGGING"],
            "rs_ratio": [102.0, 98.0],
            "rs_momentum": [101.0, 99.0],
        }
    )
    rc = RunConfig(generate_plots=True, save_plots=True)
    plotting.plot_diagnostics_rrg(df, rc)
    assert (tmp_path / "08_diagnostics_rrg.png").exists()
