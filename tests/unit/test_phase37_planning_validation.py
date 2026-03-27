"""
Nyquist hooks for Phase 37 (TMPL-01 — fork & dependency docs).

Encodes acceptance checks from `37-01-PLAN.md` must_haves and **TMPL-01**.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

_DEPS_DOC = ROOT / "docs" / "DEPENDENCIES.md"
_README = ROOT / "README.md"
_CURSOR = ROOT / "docs" / "CURSOR.md"
_REQUIREMENTS = ROOT / ".planning" / "REQUIREMENTS.md"
_ROADMAP = ROOT / ".planning" / "ROADMAP.md"


def test_phase37_dependencies_doc_exists_and_canonical_story() -> None:
    assert _DEPS_DOC.is_file(), "docs/DEPENDENCIES.md missing"
    text = _DEPS_DOC.read_text(encoding="utf-8")
    assert "pyproject.toml" in text
    assert "requirements.txt" in text
    assert "pip install -e" in text


def test_phase37_readme_links_dependencies_doc() -> None:
    body = _README.read_text(encoding="utf-8")
    assert "docs/DEPENDENCIES.md" in body


def test_phase37_cursor_links_dependencies_doc() -> None:
    body = _CURSOR.read_text(encoding="utf-8")
    assert "DEPENDENCIES.md" in body


def test_phase37_notebooks_readme_crosslink_tmplt01() -> None:
    """TMPL-01 asks for notebooks/README cross-link when not already prominent."""
    body = _README.read_text(encoding="utf-8")
    assert "notebooks/README.md" in body


def test_requirements_tmpl01_complete() -> None:
    md = _REQUIREMENTS.read_text(encoding="utf-8")
    assert "- [x] **TMPL-01**" in md
    assert "TMPL-01 | 37 | Complete" in md


def test_roadmap_v15_phase37_complete_row() -> None:
    md = _ROADMAP.read_text(encoding="utf-8")
    assert "| **37** |" in md
    assert "DEPENDENCIES.md" in md
