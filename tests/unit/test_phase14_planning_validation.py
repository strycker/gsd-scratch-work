"""
Nyquist hooks for Phase 14 (planning source reconciliation — docs only).

Encoding the acceptance checks from `14-v1-audit-planning-reconciliation-01-PLAN.md`
so CI can catch ROADMAP / STATE / VERIFICATION drift regressions.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _roadmap_phase1_block(text: str) -> str:
    start = text.index("### Phase 1:")
    end = text.index("### Phase 2:")
    return text[start:end]


def _roadmap_phase1_block_resolved() -> str:
    """Phase 1 detail lives in root ROADMAP or in `milestones/v1.0-ROADMAP.md` after v1.0 archive."""
    main = ROOT / ".planning" / "ROADMAP.md"
    text = main.read_text(encoding="utf-8")
    if "### Phase 1:" in text:
        return _roadmap_phase1_block(text)
    archived = ROOT / ".planning" / "milestones" / "v1.0-ROADMAP.md"
    assert archived.is_file(), "Collapsed ROADMAP must keep .planning/milestones/v1.0-ROADMAP.md"
    return _roadmap_phase1_block(archived.read_text(encoding="utf-8"))


def _traceability_table_chunk(text: str) -> str:
    i = text.find("## Traceability")
    assert i >= 0, "REQUIREMENTS.md missing ## Traceability"
    chunk = text[i : i + 6000]
    j = chunk.find("\n---\n", 1)
    return chunk if j < 0 else chunk[:j]


def test_roadmap_phase1_lists_01_null_plans_not_phase3() -> None:
    block = _roadmap_phase1_block_resolved()
    assert "03-supervised-regime-behavior-models" not in block
    assert "01-null-01-PLAN.md" in block


def test_state_points_at_phase14_not_stale_phase3() -> None:
    md = (ROOT / ".planning" / "STATE.md").read_text(encoding="utf-8")
    assert "Current Phase: 03" not in md
    # Mid–v1.0 audit: 14–16; after v1.0: v1.2 + current_phase null. v1.3+ uses gsd_state_version + narrative **Phase:** (no YAML current_phase).
    acceptable = (
        "current_phase: 14" in md
        or 'current_phase: "14"' in md
        or "current_phase: 15" in md
        or "current_phase: 16" in md
        or "current_phase: null" in md
        or "current_phase: 17" in md
        or "current_phase: 18" in md
        or "current_phase: 19" in md
        or "current_phase: 20" in md
        or "current_phase: 21" in md
        or "current_phase: 22" in md
        or "milestone: v1.3" in md
    )
    assert acceptable, "STATE.md should not be stuck on early phases; expected 14–22, null (v1.2–), or v1.3+ milestone"


def test_early_verification_bodies_use_trading_crab_lib_paths() -> None:
    paths = [
        ROOT / ".planning/phases/01-null/01-null-VERIFICATION.md",
        ROOT / ".planning/phases/02-regime-clustering-interpretation/02-regime-clustering-interpretation-VERIFICATION.md",
        ROOT / ".planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-VERIFICATION.md",
    ]
    for p in paths:
        body = p.read_text(encoding="utf-8")
        assert "src/market_regime" not in body, f"{p} still references src/market_regime"


def test_phase2_verification_explains_validation_vs_verification() -> None:
    p = (
        ROOT
        / ".planning/phases/02-regime-clustering-interpretation/02-regime-clustering-interpretation-VERIFICATION.md"
    )
    text = p.read_text(encoding="utf-8")
    assert "## Notes: VERIFICATION vs VALIDATION" in text
    assert "gaps_found" in text
    assert "nyquist" in text.lower()


def test_requirements_traceability_has_no_pending_rows() -> None:
    md = (ROOT / ".planning" / "REQUIREMENTS.md").read_text(encoding="utf-8")
    chunk = _traceability_table_chunk(md)
    pending_lines = [ln for ln in chunk.splitlines() if "| Pending |" in ln]
    assert not pending_lines, f"Unexpected Pending rows: {pending_lines}"


def test_phase14_summary_exists() -> None:
    p = ROOT / ".planning/phases/14-v1-audit-planning-reconciliation/14-SUMMARY.md"
    assert p.is_file()
    text = p.read_text(encoding="utf-8")
    assert "# Phase 14 Summary" in text
    assert "## Changes" in text
