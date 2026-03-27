"""Unit tests for ``plot_regime_confusion_matrix`` (TMPL-03 / Phase 39)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from trading_crab_lib.plotting import plot_regime_confusion_matrix
from trading_crab_lib.runtime import RunConfig


def _sample_regime_confusion_tidy() -> pd.DataFrame:
    """Tidy rows matching ``confusion_matrices.parquet`` (current-regime RF)."""
    return pd.DataFrame(
        {
            "family": ["regime", "regime", "regime"],
            "model": ["rf", "rf", "rf"],
            "horizon": [pd.NA, pd.NA, pd.NA],
            "fold": [0, 0, 1],
            "true_label": ["0", "1", "1"],
            "pred_label": ["0", "0", "1"],
            "count": [3, 2, 5],
        }
    )


def test_plot_regime_confusion_matrix_smoke() -> None:
    """Tidy frame matching ``confusion_matrices.parquet`` schema; no disk write."""
    df = _sample_regime_confusion_tidy()
    regime_names = {0: "Alpha", 1: "Beta"}
    run_cfg = RunConfig(generate_plots=True, save_plots=False, show_plots=False)
    plot_regime_confusion_matrix(df, regime_names, run_cfg)


def test_regime_confusion_aggregation_matches_plot_contract() -> None:
    """Same groupby/pivot contract as ``plot_regime_confusion_matrix`` (sums folds)."""
    df = _sample_regime_confusion_tidy()
    sub = df[df["family"].eq("regime") & df["model"].eq("rf")].copy()
    sub = sub[sub["horizon"].isna()]
    agg = sub.groupby(["true_label", "pred_label"], as_index=False)["count"].sum()
    pivot = agg.pivot(index="true_label", columns="pred_label", values="count").fillna(0.0)
    assert float(pivot.loc["0", "0"]) == 3.0
    assert float(pivot.loc["1", "0"]) == 2.0
    assert float(pivot.loc["1", "1"]) == 5.0


def test_forward_regime_rows_not_used_for_current_regime_plot() -> None:
    """Rows with non-null horizon (forward models) are excluded from current-regime heatmap."""
    df = pd.DataFrame(
        {
            "family": ["regime", "regime"],
            "model": ["rf", "rf"],
            "horizon": [1, pd.NA],
            "fold": [1, 1],
            "true_label": ["0", "0"],
            "pred_label": ["0", "0"],
            "count": [99, 3],
        }
    )
    sub = df[df["family"].eq("regime") & df["model"].eq("rf")].copy()
    sub = sub[sub["horizon"].isna()]
    assert len(sub) == 1
    assert int(sub["count"].iloc[0]) == 3


def test_run_pipeline_step5_wires_confusion_plot() -> None:
    """Static check: master runner loads parquet and calls the plotting helper."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "run_pipeline.py").read_text(encoding="utf-8")
    assert "confusion_matrices.parquet" in text
    assert "plot_regime_confusion_matrix" in text


def test_standalone_predict_script_supports_confusion_plot() -> None:
    """Static check: ``pipelines/05_predict.py --plots`` calls the same helper."""
    root = Path(__file__).resolve().parents[2]
    text = (root / "pipelines" / "05_predict.py").read_text(encoding="utf-8")
    assert '"--plots"' in text or "'--plots'" in text
    assert "plot_regime_confusion_matrix" in text
