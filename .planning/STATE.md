---
gsd_state_version: 1.0
milestone: v1.5
milestone_last_shipped: v1.4
milestone_name: Template hardening & doc parity
status: executing
last_updated: "2026-03-27T12:00:00.000Z"
progress:
  total_phases: 3
  completed_phases: 1
  total_plans: 1
  completed_plans: 1
---

## Project state — Trading-Crab (GSD)

## Current position

- **Phase:** **37** shipped — **Phase 38** next (backlog doc reconciliation — **TMPL-02**); see **`.planning/ROADMAP.md`**
- **Plan:** —
- **Status:** Milestone **v1.5** in progress (1/3 phases complete)
- **Last activity:** 2026-03-27 — **Phase 37** executed (**TMPL-01** — **`docs/DEPENDENCIES.md`**, README / CURSOR links)

## Next actions

1. **`$gsd-plan-phase 38`** or **`$gsd:execute-phase 38`** — **TMPL-02** (reconcile **ROADMAP.md**, **FUTURE-TODO.md**, **CLAUDE.md** with **`src/trading_crab_lib`**)

## Milestone v1.3 — phase index (28–34) — archived

| Phase | Slug (dir prefix) | Requirement(s) |
|------:|-------------------|----------------|
| 28 | `28-v1-3-hybrid-i001-summaries` | GSD-10 ✅ |
| 29 | `29-v1-3-submodule-comparison-matrix` | SYNC-10 ✅ |
| 30 | `30-v1-3-submodule-unification-blueprint` | SYNC-11 ✅ |
| 31 | `31-v1-3-library-workspace-paths` | PKG-10 ✅ |
| 32 | `32-v1-3-pypi-release-engineering` | PKG-11 ✅ |
| 33 | `33-v1-3-root-prune` | PRUNE-10 ✅ |
| 34 | `34-v1-3-library-documentation-pass` | DOCS-10 ✅ |

**Archive:** **`.planning/milestones/v1.3-ROADMAP.md`**, **`v1.3-REQUIREMENTS.md`**, **`v1.3-MILESTONE-AUDIT.md`**.

## Milestone v1.4 — phase index (35–36) — archived

| Phase | Slug (dir prefix) | Requirement(s) |
|------:|-------------------|----------------|
| 35 | `35-v1-4-phase-28-verification-parity` | AUDIT-10 ✅ |
| 36 | `36-v1-4-root-docs-import-alignment` | DOC-ALIGN-10 ✅ |

**Archive:** **`.planning/milestones/v1.4-ROADMAP.md`**, **`v1.4-REQUIREMENTS.md`**, **`v1.4-MILESTONE-AUDIT.md`**.

## Milestone v1.5 — phase index (37–39) — active

| Phase | Slug | Requirement(s) |
|------:|------|----------------|
| 37 | `37-v1-5-fork-dependency-docs` | TMPL-01 ✅ |
| 38 | *(pending)* | TMPL-02 |
| 39 | *(pending)* | TMPL-03 |

See **`.planning/ROADMAP.md`** for goals and success criteria.

## Accumulated context

- **Phase 37** — **`docs/DEPENDENCIES.md`** + README **Dependency files (forks)** + **`docs/CURSOR.md`** link; evidence **`37-01-SUMMARY.md`**.
- **v1.3** / **v1.4** — **shipped** and **archived** (2026-03-26).
- **2026-03-26 housekeeping** — Import examples and notebooks aligned to **`trading_crab_lib`**; **`v1.5-CLEANUP-BACKLOG.md`** informed v1.5 scope.
- **Submodules (read-only):** `trading-crab-lib-repo-copy`, `claude-scratch-work-repo-copy`, `trading-crab-repo-copy`.
