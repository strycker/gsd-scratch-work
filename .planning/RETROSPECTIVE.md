# GSD retrospective — Trading-Crab

## Cross-Milestone Trends

*(Update after each milestone ships.)*

---

## Milestone: v1.0 — Core pipeline + planning evidence

**Shipped:** 2026-03-20  
**Phases:** 16 | **Plans:** 17 (per `MILESTONES.md` / `gsd-tools milestone complete`)

### What was built

- Executable macro → regime → supervised models → ETF returns → dashboard/weekly report pipeline (`trading_crab_lib`, `run_pipeline.py`, checkpoints).
- GSD-style evidence: per-phase `VERIFICATION.md` and `VALIDATION.md`, requirements traceability, milestone audit, gap-closure phases **15–16** (REGIME-02/03, **`RUNBOOK.md`**).

### What worked

- Checkpointed pipeline + formal verification made audits tractable.
- Dedicated gap-closure phases (audit → plan-milestone-gaps → execute) cleared blockers without polluting earlier phase narratives.

### What was inefficient

- Duplicate / stale **MILESTONES** entries from earlier tooling runs (ledger preserved; newest v1.0 entry is canonical).
- `summary` frontmatter `one-liner` sparse → empty accomplishments from `gsd-tools`; filled manually in **MILESTONES.md**.

### Patterns established

- Single operational source for E2E:**`RUNBOOK.md`** + **`ARCHITECTURE.md`** pointer.
- Regime macro vs ETF artifacts split: `profiles.parquet` vs `etf_behavior_by_regime.parquet`.

### Residual tech debt (from audit)

- Checkpoint invalidation vs config edits (operator discipline; documented in RUNBOOK).
- SMTP/secrets paths environment-dependent (**REPORT-03** / **INSTALL-10**).

---
