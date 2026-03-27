---
phase: 37-v1-5-fork-dependency-docs
verified: 2026-03-27T12:00:00Z
status: passed
score: 3/3 must-have truths + ROADMAP success criterion + TMPL-01
nyquist_compliant: true
---

# Phase 37: Fork & dependency docs — Verification Report

**Phase goal:** Forks know how to install and which file is **canonical** for dependencies (**`pyproject.toml`** vs **`requirements*.txt`**), with pointers from onboarding docs.

**Requirement:** TMPL-01

**Verified:** 2026-03-27  
**Status:** **passed**

## Goal achievement (goal-backward)

### Observable truths (from `37-01-PLAN.md` `must_haves.truths`)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | `docs/DEPENDENCIES.md` exists and states `pyproject.toml` is canonical for package deps | ✓ VERIFIED | `test -f docs/DEPENDENCIES.md`; `grep -q 'pyproject.toml' docs/DEPENDENCIES.md` |
| 2 | `README.md` contains a pointer to `docs/DEPENDENCIES.md` under Installation (or immediately after) | ✓ VERIFIED | `grep -q 'docs/DEPENDENCIES.md' README.md` (subsection **Dependency files (forks)**) |
| 3 | `grep -q 'DEPENDENCIES.md' docs/CURSOR.md` exits 0 | ✓ VERIFIED | Command run: exit **0** |

**Score:** 3/3

### ROADMAP success criteria (`.planning/ROADMAP.md` — Phase overview row **37**)

| Criterion | Status | Evidence |
|-----------|--------|----------|
| README (or `docs/`) states pyproject vs requirements; `make`/CI story unchanged or documented | ✓ VERIFIED | **`docs/DEPENDENCIES.md`** covers canonical **`pyproject.toml`**, **`requirements.txt`** / **`requirements-dev.txt`**, **`scripts/setup.sh`**, optional lockfiles; README links to doc |

### Required artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `docs/DEPENDENCIES.md` | Single source of truth narrative for forks | ✓ EXISTS + SUBSTANTIVE | **445** words; sections: canonical `pyproject.toml`, `requirements*.txt`, dev file, scripts, lockfiles, fork checklist |
| `README.md` | Installation cross-link | ✓ MODIFIED | **Dependency files (forks)** → `docs/DEPENDENCIES.md` |
| `docs/CURSOR.md` | IDE setup cross-link | ✓ MODIFIED | Link to **`DEPENDENCIES.md`** after intro |

**`gsd-tools verify artifacts`:** N/A — structured `must_haves.artifacts` uses `path`/`provides` objects; verifier expects a flat artifact list. Manual checks used (same pattern as Phase **36**).

### Key links

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| README Installation | `docs/DEPENDENCIES.md` | Markdown link | ✓ WIRED | Resolves from repo root |
| `docs/CURSOR.md` | `docs/DEPENDENCIES.md` | Relative `DEPENDENCIES.md` | ✓ WIRED | Same directory |
| TMPL-01 (notebooks cross-link) | `notebooks/README.md` | Root README | ✓ WIRED | `grep -q 'notebooks/README.md' README.md` (existing notebook imports section) |

**`gsd-tools verify key-links`:** N/A — no `must_haves.key_links` in PLAN frontmatter. Manual table above.

## Requirements coverage

| Requirement | Status | Notes |
|-------------|--------|-------|
| TMPL-01 | ✓ SATISFIED | `[x]` in **`.planning/REQUIREMENTS.md`**; traceability `| TMPL-01 | 37 | Complete |`; truths 1–3 + notebooks cross-link per requirement text |

## Tooling notes

| Check | Result |
|-------|--------|
| `gsd-tools verify phase-completeness 37` | ✓ `complete: true` (1 plan, 1 summary **`37-01-SUMMARY.md`**) |
| `gsd-tools roadmap get-phase 37` | `found: false` — v1.5 roadmap uses table + `### Phase 37` headings, not the legacy parse format; manual roadmap row used |
| `gsd-tools validate health` | `degraded` — **W002** STATE references Phase **38** (not yet on disk); **W007** false positive (Phase **37** exists in **`.planning/ROADMAP.md`** v1.5 table). Neither blocks Phase **37** goal verification |

## Anti-patterns scan (`docs/DEPENDENCIES.md`, edited README / CURSOR sections)

| Pattern | Result |
|---------|--------|
| TODO / FIXME / placeholder onboarding | None in scanned files |

## Human verification required

None — documentation-only phase; grep and file presence are sufficient.

## Gaps summary

**No gaps found.** Phase goal achieved.

## Verification commands (this run)

```bash
test -f docs/DEPENDENCIES.md
grep -q 'pyproject.toml' docs/DEPENDENCIES.md
grep -q 'docs/DEPENDENCIES.md' README.md
grep -q 'DEPENDENCIES.md' docs/CURSOR.md
grep -q 'notebooks/README.md' README.md

grep -E '\[x\] \*\*TMPL-01' .planning/REQUIREMENTS.md
grep 'TMPL-01 | 37 | Complete' .planning/REQUIREMENTS.md

wc -w docs/DEPENDENCIES.md

node .codex/get-shit-done/bin/gsd-tools.cjs verify phase-completeness 37
```

## Verification metadata

- **Plans verified:** `37-01-PLAN.md`
- **Summary:** `37-01-SUMMARY.md`
- **Verifier:** GSD `verify-phase` workflow (automated checks + manual goal-backward review)
