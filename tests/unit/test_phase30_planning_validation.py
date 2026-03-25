"""
Nyquist hooks for Phase 30 (SYNC-11 submodule unification blueprint — docs only).

Encodes acceptance checks from `30-v1-3-submodule-unification-blueprint-01-PLAN.md` tasks 30-01-01 / 30-01-02.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

_BLUEPRINT = ROOT / ".planning" / "research" / "SUBMODULE_UNIFICATION_BLUEPRINT.md"
_SUMMARY = ROOT / ".planning" / "phases" / "30-v1-3-submodule-unification-blueprint" / "30-SUMMARY.md"
_REQUIREMENTS = ROOT / ".planning" / "REQUIREMENTS.md"
_ROADMAP = ROOT / ".planning" / "ROADMAP.md"


def test_phase30_blueprint_exists_with_acceptance_substrings() -> None:
    assert _BLUEPRINT.is_file(), "SUBMODULE_UNIFICATION_BLUEPRINT.md missing"
    text = _BLUEPRINT.read_text(encoding="utf-8")
    assert "Submodule unification blueprint (v1.3 — SYNC-11)" in text
    assert "more complete / better-tested" in text
    assert "## Winner-selection rule" in text
    assert "## Exclusions" in text
    assert "### Batch 1: LIB — Test and fixture parity" in text
    assert "### Batch 5: CRAB — Notebook and artifact reference" in text
    assert "Owner-confirm gate:" in text
    assert "no push" in text.lower()


def test_phase30_batches_have_five_field_labels_each() -> None:
    text = _BLUEPRINT.read_text(encoding="utf-8")
    for label in ("**Objective:**", "**Source:**", "**Risk:**", "**Depends on:**", "**Owner-confirm gate:**"):
        assert text.count(label) >= 5, f"Expected >= 5 occurrences of {label}"


def test_phase30_summary_cites_blueprint() -> None:
    assert _SUMMARY.is_file()
    body = _SUMMARY.read_text(encoding="utf-8")
    assert "SUBMODULE_UNIFICATION_BLUEPRINT.md" in body


def test_requirements_sync11_complete() -> None:
    md = _REQUIREMENTS.read_text(encoding="utf-8")
    assert "- [x] **SYNC-11**" in md
    assert "SYNC-11 | 30 | Complete" in md


def test_roadmap_phase30_checked() -> None:
    md = _ROADMAP.read_text(encoding="utf-8")
    assert "- [x] **Phase 30: v1.3 — Submodule unification blueprint (owner gates)**" in md
