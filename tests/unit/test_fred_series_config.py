from __future__ import annotations

from pathlib import Path

import yaml

CFG_PATH = Path(__file__).resolve().parents[2] / "config" / "settings.yaml"


def _load_cfg() -> dict:
    with CFG_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_fred_t10y_spreads_not_in_clustering_features() -> None:
    """Phase 17: clustering uses yc_* spreads; FRED T10Y2Y/T10Y3M stay ingest-only."""
    cfg = _load_cfg()
    cf = cfg["features"]["clustering_features"]
    assert "fred_t10y2y" not in cf
    assert "fred_t10y2y_d1" not in cf
    assert "fred_t10y3m" not in cf
    assert "fred_t10y3m_d1" not in cf
    assert "yc_10y_2y_d1" in cf
    assert "yc_10y_3m_d1" in cf


def test_fred_series_includes_phase8_additions() -> None:
    cfg = _load_cfg()
    series = cfg["fred"]["series"]
    for key, name in [
        ("VIXCLS", "fred_vix"),
        ("UNRATE", "fred_unrate"),
        ("M2SL", "fred_m2sl"),
        ("M2NS", "fred_m2ns"),
        ("GS2", "fred_gs2"),
        ("T10Y2Y", "fred_t10y2y"),
        ("T10Y3M", "fred_t10y3m"),
        ("HOUST", "fred_houst"),
        ("UMCSENT", "fred_umcsent"),
    ]:
        assert key in series
        assert series[key]["name"] == name
        assert series[key].get("shift", False) is False
