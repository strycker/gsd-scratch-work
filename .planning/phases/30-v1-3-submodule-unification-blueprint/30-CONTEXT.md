# Phase 30: Submodule unification blueprint — Context

**Gathered:** 2026-03-25  
**Status:** Ready for planning  
**Source:** ROADMAP Phase 30, **REQUIREMENTS.md** (**SYNC-11**), **`.planning/research/FEATURES.md`**, **`.planning/research/SUBMODULE_COMPARISON_MATRIX.md`** (Phase 29)

---

## Phase boundary

**In scope:** One **markdown blueprint** under **`.planning/research/`** that turns the **Phase 29** comparison into **ordered, executable batches** (tests, modules, config/pipelines, experimental code, notebook/reference artifacts). Each batch must name **objective**, **source** (canonical root vs named mirror), **risk**, **dependency on prior batches**, and an **owner-confirmation** gate before later phases treat the batch as approved for implementation.

**Explicitly out of scope for Phase 30 execute:** Any code edits inside **`legacy/`**, **`trading-crab-lib-repo-copy/`**, **`claude-scratch-work-repo-copy/`**, **`trading-crab-repo-copy/`**, or **pushing commits to submodule remotes**. Unification **implementation** is **later phases** (31+), not this blueprint-only phase.

---

## Locked decisions

1. **Merge sequence (batches follow this order):** **`trading-crab-lib-repo-copy`** first → **`claude-scratch-work-repo-copy`** second → **`trading-crab-repo-copy`** last — matches **FEATURES.md** § *Unification order* and **SUBMODULE_COMPARISON_MATRIX.md** § *Merge order*.
2. **Winner policy:** When implementations diverge, prefer **more complete / better-tested** code **wherever it lives**; **human (owner) confirmation** is required before recording a “winner” for merge work in a future execute (see **FEATURES.md** § *Merge policy*).
3. **Superset target:** Canonical root becomes the **union** of valuable capabilities with **one** implementation per concern after future merges; this phase only **plans** batches and gates — it does not deduplicate code.
4. **Nested mirror noise:** Diffs should use **path-normalized** views (canonical paths only); do **not** treat nested `gsd-scratch-work-repo-copy/` trees inside LIB mirror as primary sources without an explicit path — **FEATURES.md** + Phase 29 matrix *Layout caveats*.
5. **Post-milestone:** Document that **updating submodule remotes / pushing to mirrors** is **out of scope for v1.3** in the blueprint *Exclusions* section.

---

## Canonical references (read before execute)

| Path | Role |
|------|------|
| `.planning/research/SUBMODULE_COMPARISON_MATRIX.md` | Phase 29 inventory and deltas |
| `.planning/research/FEATURES.md` | Merge policy, unification order, superset definition |
| `.planning/research/ARCHITECTURE.md` | Packaging / layout expectations for later PKG phases |
| `.planning/ROADMAP.md` | Phase 30 success criteria |
| `.planning/REQUIREMENTS.md` | **SYNC-11** |

---

*Phase: 30-v1-3-submodule-unification-blueprint*
