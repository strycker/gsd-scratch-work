# Phase 29: Submodule comparison matrix — Context

**Gathered:** 2026-03-25  
**Status:** Ready for planning  
**Source:** **`.planning/ROADMAP.md`** Phase 29; **`.planning/research/FEATURES.md`**; **`.planning/research/ARCHITECTURE.md`**

## Phase boundary

Deliver **one authoritative markdown comparison artifact** under **`.planning/`** covering **canonical root** vs three **read-only** submodule mirrors:

- `trading-crab-lib-repo-copy`
- `claude-scratch-work-repo-copy`
- `trading-crab-repo-copy`

**No** edits inside mirror trees or `legacy/`; **no** submodule commits. `git submodule update --init --recursive` / refresh is allowed for **freshness only**.

## Implementation decisions

- **Merge order (locked):** `trading-crab-lib` mirror **→** `claude-scratch-work` **→** `trading-crab`; each step gets **dependency/risk** notes in the artifact.
- **Winner policy:** Prefer **more complete / better-tested** code **regardless of repo**; actual merges are **Phase 30+** with **owner confirmation** — this phase only **observes** and **tables** deltas.
- **Nested layout:** If a mirror contains another nested `*_repo-copy` / scratch tree, **document it** as a row (“nested clone noise”) — do **not** normalize inside submodule.
- **Primary artifact path:** **`.planning/research/SUBMODULE_COMPARISON_MATRIX.md`** (single file; path repeated in **29-SUMMARY.md** after execute).

## Canonical references

- **`.planning/research/FEATURES.md`** — comparison dimensions, superset definition  
- **`.planning/research/ARCHITECTURE.md`** — `ROOT` / packaging context  
- **`.gitmodules`** — authoritative submodule URLs/paths  
- **`.planning/ROADMAP.md`** — Phase 29 success criteria

## Deferred

- Executable unification batches → **Phase 30** (**SYNC-11**).
