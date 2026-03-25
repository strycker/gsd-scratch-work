# Pitfalls Research — v1.3

**Researched:** 2026-03-25

## 1. Submodule editing drift

**Risk:** Accidentally patching files under `*_repo-copy/` “to make tests pass”.  
**Mitigation:** CI or pre-commit *optional* rule: reject changes under mirror paths. Only `git submodule update` / `pull` in v1.3.

## 2. Nested / stale submodule layouts

**Risk:** Comparing wrong directory (e.g. nested `gsd-scratch-work-repo-copy` inside another mirror) yields false “missing features”.  
**Mitigation:** Document **canonical path per mirror** in RUNBOOK or research appendix; refresh submodules before diff.

## 3. `ROOT` / `CONFIG_DIR` after `pip install`

**Risk:** Library appears broken off-repo; silent reads of wrong config.  
**Mitigation:** Explicit path API + docs (ARCHITECTURE.md); tests for both editable and installed layouts.

## 4. “Superset” = unbounded scope

**Risk:** Trying to merge every experiment from scratch repos blows v1.3.  
**Mitigation:** Stakeholder confirmation per chunk; **defer** to future milestones with explicit REQ; use feature flags / extras.

## 5. PyPI name / trademark

**Risk:** **`trading-crab-lib`** collision or policy rejection.  
**Mitigation:** Early TestPyPI upload; reserve name; clear description (“macro regime research library”, not investment advice).

## 6. Comment verbosity vs maintenance

**Risk:** “Explain every block” rots when code changes; comments contradict code.  
**Mitigation:** Prefer **why / invariants / failure modes** over restating *what* the code does; tie long rationale to design docs where stable.

## 7. Docstring standard

**Recommendation:** **Google-style** for modules and public functions (readable in IDEs); **short lead paragraph** per file for human + LLM context. For numerical-heavy public API, optional **NumPy-style** `Parameters` / `Returns` blocks where precision matters.

## 8. Merge conflict policy ambiguity

**Risk:** “More complete/tested” without metrics devolves into opinion.  
**Mitigation:** Require **test count + benchmark + OWNER decision** logged before replacement.

## 9. Pruning notebooks

**Risk:** Losing pedagogical value.  
**Mitigation:** Export irreplaceable narratives to `docs/` or single canonical notebook before delete; git history retains files.

## 10. PROJECT.md staleness

**Risk:** Still references `market_regime` while package is `trading_crab_lib`.  
**Mitigation:** v1.3 doc pass aligns terminology (no legacy package rename required — docs only unless stakeholder wants alias).
