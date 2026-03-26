# GSD planning inventory — v1.3 (2026-03-26)

**Purpose:** One place to see **phase artifacts** vs **conversational UAT** (`*-UAT.md`) for milestone hygiene.

## v1.3 phases (28–34)

| Phase | Folder (short) | Phase SUMMARY | VERIFICATION / VALIDATION | Per-plan `01-SUMMARY` | UAT |
|------:|------------------|---------------|---------------------------|----------------------|-----|
| 28 | `28-v1-3-hybrid-i001-summaries` | 28-SUMMARY.md | 28-VALIDATION.md | ✅ `28-*-01-SUMMARY.md` | — |
| 29 | `29-v1-3-submodule-comparison-matrix` | 29-SUMMARY.md | 29-VERIFICATION.md, 29-VALIDATION.md | ✅ `29-*-01-SUMMARY.md` | — |
| 30 | `30-v1-3-submodule-unification-blueprint` | 30-SUMMARY.md | 30-VERIFICATION.md, 30-VALIDATION.md | ✅ `30-*-01-SUMMARY.md` | — |
| 31 | `31-v1-3-library-workspace-paths` | 31-SUMMARY.md | 31-VERIFICATION.md, 31-VALIDATION.md | ✅ `31-*-01-SUMMARY.md` | — |
| 32 | `32-v1-3-pypi-release-engineering` | 32-SUMMARY.md | 32-VERIFICATION.md, 32-VALIDATION.md | ✅ `32-*-01-SUMMARY.md` | **32-UAT.md** (complete) |
| 33 | `33-v1-3-root-prune` | 33-SUMMARY.md | 33-VERIFICATION.md, 33-VALIDATION.md | ✅ `33-*-01-SUMMARY.md` | — |
| 34 | `34-v1-3-library-documentation-pass` | 34-SUMMARY.md | 34-VERIFICATION.md | ✅ `34-*-01-SUMMARY.md` | **34-UAT.md** (complete) |

**Note:** Phases **23–25** are v1.0 closure tracks with **23/24/25-UAT.md** (separate from the v1.3 backlog above).

**Conversational UAT** (`*-UAT.md`) is **optional** for phases that already have **VERIFICATION.md** / **VALIDATION.md** and green **`validate health`**. Add UAT when you want explicit user sign-off beyond automated verification.

## `gsd-tools validate health`

Run from repo root:

```bash
node .codex/get-shit-done/bin/gsd-tools.cjs validate health
```

Expect **`status: healthy`** with **no I001** for any `*-01-PLAN.md` that lacks a matching `*-01-SUMMARY.md` basename (Phase 34 hybrid summary added 2026-03-26).

**Last check:** `healthy`, `info: []` (2026-03-26).
