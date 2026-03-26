"""Tests for Phase 27: pipeline step order and dashboard model path resolution."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from run_pipeline import resolve_pipeline_step_order  # noqa: E402
from trading_crab_lib.prediction.dashboard_model import (  # noqa: E402
    resolve_current_regime_model_path,
)


class TestResolvePipelineStepOrder:
    def test_seven_eight_nine(self) -> None:
        assert resolve_pipeline_step_order({7, 8, 9}) == [8, 9, 7]

    def test_full_stack(self) -> None:
        order = resolve_pipeline_step_order({1, 2, 3, 4, 5, 6, 7, 8, 9})
        i7 = order.index(7)
        i8 = order.index(8)
        i9 = order.index(9)
        assert i8 < i7 and i9 < i7

    def test_five_seven_no_swap(self) -> None:
        assert resolve_pipeline_step_order({5, 7}) == [5, 7]

    def test_eight_nine_only(self) -> None:
        assert resolve_pipeline_step_order({8, 9}) == [8, 9]

    def test_seven_only(self) -> None:
        assert resolve_pipeline_step_order({7}) == [7]


class TestResolveCurrentRegimeModelPath:
    def test_defaults_rf(self, tmp_path: Path) -> None:
        rf = tmp_path / "current_regime.pkl"
        rf.write_bytes(b"x")
        p = resolve_current_regime_model_path({}, tmp_path, None)
        assert p == rf

    def test_gb_when_present(self, tmp_path: Path) -> None:
        rf = tmp_path / "current_regime.pkl"
        gb = tmp_path / "current_regime_gb.pkl"
        rf.write_bytes(b"a")
        gb.write_bytes(b"b")
        cfg = {"dashboard": {"regime_model": "gb"}}
        assert resolve_current_regime_model_path(cfg, tmp_path, None) == gb

    def test_gb_fallback_when_missing(
        self, tmp_path: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        import logging

        rf = tmp_path / "current_regime.pkl"
        rf.write_bytes(b"a")
        cfg = {"dashboard": {"regime_model": "gb"}}
        caplog.set_level(logging.WARNING)
        p = resolve_current_regime_model_path(cfg, tmp_path, logging.getLogger("t"))
        assert p == rf
        assert "falling back" in caplog.text
