---
phase: 38-v1-5-backlog-reconciliation
verified: 2026-03-27T12:00:00Z
status: passed
score: 4/4 must-have truths + TMPL-02 + ROADMAP success row
nyquist_compliant: true
---

# Phase 38: Backlog reconciliation — Verification Report

**Phase goal:** Product markdown (**root `ROADMAP.md`**, **`FUTURE-TODO.md`**, **`CLAUDE.md`**) matches **`src/trading_crab_lib`** for yield-curve **`yc_*`** features and **`build_forward_window_probabilities`** / **`forward_window_probabilities.parquet`**, without phantom “not implemented” claims for shipped code.

**Requirement:** TMPL-02

**Verified:** 2026-03-27  
**Status:** **passed**

## Goal achievement (goal-backward)

### Observable truths (from `38-01-PLAN.md` `must_haves.truths`)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Root **`ROADMAP.md`** Tier 1.3 names **`yc_*`** / **`add_yield_curve_features`** | ✓ VERIFIED | §1.3: **`add_yield_curve_features()`**, **`yc_10y_2y`**, **`yc_10y_3m`**, **`yc_2y_3m`**, **`config/settings.yaml`** |
| 2 | Root **`ROADMAP.md`** Tier 1.4 names **`build_forward_window_probabilities`** / **`forward_window_probabilities.parquet`** (not only legacy name) | ✓ VERIFIED | §1.4: implementation path + parquet + legacy one-liner |
| 3 | **`CLAUDE.md`** does not list empirical forward probs as missing in **`src/`** while **`regime.py`** ships the API | ✓ VERIFIED | **Features in legacy NOT yet in src** has no ✗ empirical line; **Gap 6** closed with **`build_forward_window_probabilities`** |
| 4 | **`FUTURE-TODO.md`** empirical-forward bullet matches API + output path | ✓ VERIFIED | **`build_forward_window_probabilities()`**, **`regime.py`**, **`forward_window_probabilities.parquet`** |

**Score:** 4/4

### ROADMAP success criteria (`.planning/ROADMAP.md` — Phase **38** overview)

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Root **`ROADMAP`** / **`FUTURE-TODO`** / **`CLAUDE`** gaps aligned with **`trading_crab_lib`** | ✓ VERIFIED | Edits in **`ROADMAP.md`**, **`CLAUDE.md`**, **`FUTURE-TODO.md`**; **`v1.5-CLEANUP-BACKLOG.md`** TMPL-02 note |

### Required artifacts

| Artifact | Status | Details |
|----------|--------|---------|
| `ROADMAP.md` (repo root) | ✓ EXISTS + SUBSTANTIVE | Tier 1.3–1.4 + suggested starting points updated |
| `CLAUDE.md` | ✓ MODIFIED | Gap 6, Next Priority, note block |
| `.planning/FUTURE-TODO.md` | ✓ MODIFIED | Forward-window bullet |
| `.planning/v1.5-CLEANUP-BACKLOG.md` | ✓ MODIFIED | **TMPL-02 (Phase 38)** section |

**`gsd-tools verify artifacts`:** N/A — same structured-artifact frontmatter pattern as Phase **37**; manual checks used.

### Key links

| From | To | Status | Details |
|------|----|--------|---------|
| Docs | **`src/trading_crab_lib/transforms.py`** / **`regime.py`** | ✓ CONSISTENT | Column and function names match onboarding text |
| TMPL-02 | **`.planning/REQUIREMENTS.md`** | ✓ WIRED | `[x] **TMPL-02**`; traceability **Complete** |

## Requirements coverage

| Requirement | Status | Notes |
|-------------|--------|-------|
| TMPL-02 | ✓ SATISFIED | Checkbox + **`38-01-SUMMARY.md`** |

## Tooling notes

| Check | Result |
|-------|--------|
| `gsd-tools verify phase-completeness 38` | ✓ `complete: true` |
| `gsd-tools roadmap get-phase 38` | `found: false` — v1.5 table format; phase content verified in **`.planning/ROADMAP.md`** row **38** |

## Anti-patterns scan (edited files)

| Pattern | Result |
|---------|--------|
| TODO / placeholder-only backlog for shipped §1.3–1.4 | None — Tier markers use *(shipped)* |

## Human verification required

None — documentation parity only.

## Gaps summary

**No gaps found.** Phase goal achieved.

## Verification commands (this run)

```bash
grep -E 'yc_10y_2y|add_yield_curve_features|build_forward_window|forward_window_probabilities' ROADMAP.md
grep -E 'build_forward_window|Gap 6' CLAUDE.md
grep -E 'build_forward_window|forward_window_probabilities' .planning/FUTURE-TODO.md
grep -E '\[x\] \*\*TMPL-02|TMPL-02 \| 38 \| Complete' .planning/REQUIREMENTS.md

node .codex/get-shit-done/bin/gsd-tools.cjs verify phase-completeness 38
```

## Verification metadata

- **Plans verified:** `38-01-PLAN.md`
- **Summary:** `38-01-SUMMARY.md`
- **Verifier:** GSD `verify-phase` workflow
