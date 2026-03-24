# GSD retrospective — Trading-Crab

## Cross-Milestone Trends

*(Update after each milestone ships.)*

---

## Milestone: v1.2 — Tactics, triggers & expanded signals

**Shipped:** 2026-03-24  
**Phases:** 11 | **Plans:** 11

### What was built

- Macro + yield expansion, optional providers, signal/diagnostics, sklearn boosted models + interpret trees, tactics layer, email/install docs, GSD verification closure (**21–25**, **17–19** VALIDATION), pipeline integration (**8 → 9 → 7**, `dashboard.regime_model`, `run_weekly_report.py`).

### What worked

- Dedicated gap-closure phases (**26–27**) after **`$gsd-audit-milestone`** turned audit findings into small, testable integration work.
- Unit tests for step-order and model-path resolution caught wiring regressions without full E2E scrapes.

### What was inefficient

- **`gsd-tools milestone complete`** left **accomplishments** empty (sparse SUMMARY frontmatter); **MILESTONES.md** filled manually.
- Multiple **`human_needed`** VERIFICATIONs (optional real-data runs) remain as documented tech debt, not blockers.

### Patterns established

- **`resolve_pipeline_step_order`** as the single place to enforce cross-step ordering when CLI step lists are partial.
- Requirements + roadmap archived per milestone; living **REQUIREMENTS.md** collapsed to a stub until **`$gsd-new-milestone`**.

### Residual tech debt

- Optional full-pipeline human runs for phases **18–20**; HMM / macrotrends / empirical forward probabilities still deferred per **`milestones/v1.2-REQUIREMENTS.md`**.

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
