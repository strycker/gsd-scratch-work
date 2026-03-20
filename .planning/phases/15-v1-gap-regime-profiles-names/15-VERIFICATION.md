---
phase: 15-v1-gap-regime-profiles-names
verified: 2026-03-20T00:00:00Z
status: passed
score: 4/4 must-have truths verified
---

# Phase 15: v1.0 Gap Closure — Regime ETF profiles & pinned names — Verification Report

**Phase goal:** Satisfy **REGIME-02** and **REGIME-03** at the evidence level from `.planning/v1.0-MILESTONE-AUDIT.md` (Phase 2 requirement-level VERIFICATION aligns with `passed` for automated truths).

**Verified:** 2026-03-20  
**Status:** passed  
**Invocation:** `$gsd:verify-phase 15` (goal-backward)

## Goal achievement

### Observable truths (`15-v1-gap-regime-profiles-names-01-PLAN.md` `must_haves.truths`)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | REGIME-02: macro in `profiles.parquet`; ETF/proxy behavior in `etf_behavior_by_regime.parquet` (step 6); split documented in code + Phase 2 VERIFICATION. | ✓ VERIFIED | `src/trading_crab_lib/regime.py` includes *Regime artifacts (macro vs ETF)* with both paths; `pipelines/06_asset_returns.py` L125–127 calls `behavior_tables` and writes `etf_behavior_by_regime.parquet`; `pipelines/04_regime_label.py` docstring cross-links step 6; `.planning/phases/02-regime-clustering-interpretation/02-regime-clustering-interpretation-VERIFICATION.md` truth row 4 ✓. |
| 2 | REGIME-03: `config/regime_labels.yaml` pins IDs **0–4** for `balanced_k=5`; no stray IDs. | ✓ VERIFIED | `python -c "… assert set(r.keys())=={0,1,2,3,4}"` exits 0; `grep '^5:' config/regime_labels.yaml` → no matches. |
| 3 | Automated test guards ETF path (`behavior_tables`) for REGIME-02. | ✓ VERIFIED | `tests/unit/test_regime_etf_profile_artifact.py` present; `pytest tests/unit/test_regime_etf_profile_artifact.py tests/unit/test_regime.py -q` → **6 passed** (verify run). |
| 4 | Phase 2 `*-VERIFICATION.md` frontmatter **`status: passed`** without `gaps_found` for these items. | ✓ VERIFIED | Line 4: `status: passed`; `gaps: []` in frontmatter. |

**Score:** 4/4 truths verified

### Roadmap success criteria (cross-check)

| # | Criterion (`.planning/ROADMAP.md` Phase 15) | Status | Evidence |
|---|---------------------------------------------|--------|----------|
| 1 | ETF return summaries reproducible; agreed artifact + VERIFICATION cite. | ✓ | Same as truth 1 + Phase 2 VERIFICATION artifacts table. |
| 2 | `regime_labels.yaml` pinned mappings. | ✓ | Same as truth 2. |
| 3 | Phase 2 VERIFICATION updated toward `passed`. | ✓ | Same as truth 4. |

## Required artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/trading_crab_lib/regime.py` | Docstring lists canonical paths | ✓ | `etf_behavior_by_regime.parquet`, `profiles.parquet`, `asset_return_profile.parquet`. |
| `tests/unit/test_regime_etf_profile_artifact.py` | REGIME-02 column contract test | ✓ | Non-empty `behavior_tables` output; required columns present. |
| `config/regime_labels.yaml` | Keys **0–4** only | ✓ | YAML load assert; no `5:` key. |
| `15-SUMMARY.md` | Execution record | ✓ | Present; ≥15 lines. |

**Tooling note:** `gsd-tools verify artifacts` on this plan returns *No must_haves.artifacts* (nested YAML shape); evidence above is primary.

## Key link verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| Step 6 pipeline | `data/regimes/etf_behavior_by_regime.parquet` | `behavior_tables` → `to_parquet` | ✓ WIRED | `pipelines/06_asset_returns.py` |
| Step 4 pipeline | `data/regimes/profiles.parquet` | `build_profiles` | ✓ WIRED | `pipelines/04_regime_label.py` (pre-existing) |
| Phase 4 naming | `config/regime_labels.yaml` | `load_name_overrides` | ✓ WIRED | `trading_crab_lib.regime.load_name_overrides` |

## Requirements coverage

| Requirement | Status | Notes |
|-------------|--------|-------|
| REGIME-02 | ✓ SATISFIED | `.planning/REQUIREMENTS.md` Phase **15** \| **Complete**. |
| REGIME-03 | ✓ SATISFIED | Same. |

## Anti-patterns

No blockers found in sampled deliverables (`regime.py`, new test, yaml, Phase 2 VERIFICATION). Optional spot-check: no `TODO` required for phase closure.

## Human verification

**Inherited (Phase 2 scope):** `02-regime-clustering-interpretation-VERIFICATION.md` frontmatter **`human_verification`** — subjective notebook/plot review of regime interpretability. **Does not fail Phase 15** automated goal; note for milestone UAT only.

## Gaps summary

**None** — Phase 15 goal-backward verification **passed**.

---

_Re-verification: run `pytest tests/unit/test_regime_etf_profile_artifact.py tests/unit/test_regime.py -q` after future regime/returns changes._
