"""
Nyquist hooks for Phase 38 (TMPL-02 — backlog doc reconciliation).

Encodes acceptance checks from `38-01-PLAN.md` must_haves and **TMPL-02**.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

_PRODUCT_ROADMAP = ROOT / "ROADMAP.md"
_CLAUDE = ROOT / "CLAUDE.md"
_FUTURE_TODO = ROOT / ".planning" / "FUTURE-TODO.md"
_REQUIREMENTS = ROOT / ".planning" / "REQUIREMENTS.md"
_CLEANUP = ROOT / ".planning" / "v1.5-CLEANUP-BACKLOG.md"


def test_product_roadmap_tier13_yield_shipped_story() -> None:
    md = _PRODUCT_ROADMAP.read_text(encoding="utf-8")
    assert "add_yield_curve_features" in md
    assert "yc_10y_2y" in md


def test_product_roadmap_tier14_forward_window_shipped() -> None:
    md = _PRODUCT_ROADMAP.read_text(encoding="utf-8")
    assert "build_forward_window_probabilities" in md
    assert "forward_window_probabilities.parquet" in md


def test_claude_gap6_and_no_missing_empirical_forward_bullet() -> None:
    md = _CLAUDE.read_text(encoding="utf-8")
    assert "Gap 6" in md
    assert "build_forward_window_probabilities" in md
    assert "✗ Empirical forward probabilities" not in md


def test_future_todo_forward_window_paths() -> None:
    md = _FUTURE_TODO.read_text(encoding="utf-8")
    assert "build_forward_window_probabilities" in md
    assert "forward_window_probabilities.parquet" in md


def test_requirements_tmpl02_complete() -> None:
    md = _REQUIREMENTS.read_text(encoding="utf-8")
    assert "- [x] **TMPL-02**" in md
    assert "TMPL-02 | 38 | Complete" in md


def test_cleanup_backlog_phase38_note() -> None:
    md = _CLEANUP.read_text(encoding="utf-8")
    assert "TMPL-02" in md and "Phase 38" in md
