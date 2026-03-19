---
phase: 03-supervised-regime-behavior-models
created: 2026-03-19
status: locked
tags: [supervised, timeseries, leakage-guard, behavior, metrics, horizons]
---

# Phase 03 — Context (Locked Decisions)

This file captures the Phase 3 implementation decisions that should not be re-litigated during planning/execution.

## Scope Reminder (from ROADMAP)

- Phase 3 builds **supervised regime + behavior models** (MODEL-01..04).
- Inputs are **Phase 2 regimes** and **Phase 1 causal features**.
- Must remain ETF-only, no intraday, no auto-trading.

## Locked Decisions

### 1) Leakage guardrails (causal feature requirement)

**Decision:** Step 5 (and any Phase-3 training entrypoint) may only train on non-causal features when the user explicitly opts in.

- **Default behavior:** require `data/processed/features_supervised.parquet`.
- **If missing:** error out **unless** an explicit flag is provided.
- **Opt-in flag:** add a CLI flag (name TBD during planning; e.g. `--allow-noncausal-features`) that permits fallback to `data/processed/features.parquet` with a loud warning.

Rationale: avoid silent leakage regressions while preserving an escape hatch for exploratory work.

### 2) Behavior models wiring

**Decision:** Phase 3 should **wire behavior models into pipeline step 5** (not library-only).

- Persist behavior model bundles alongside regime models.
- Emit metrics artifacts for behavior models in the same reporting surface as regime models (MODEL-04).

Rationale: keep Phase 3 “complete” as a modeling layer that downstream phases can consume without bespoke notebooks.

### 3) Metrics + reporting artifacts (beyond pickled models)

**Decision:** Persist structured metrics artifacts, not just log strings.

Produce (format can be refined during planning):
- **CV summary table** (per model × horizon) — parquet/CSV
- **Per-fold reports** (for auditability) — JSON (or JSONL)
- **Confusion matrices** — parquet + optional plot
- **Calibration diagnostics** — reliability metrics + optional plot

Rationale: MODEL-04 requires time-series aware metrics that are inspectable before trusting recommendations.

### 4) Horizon configuration source of truth

**Decision:** Use **separate config keys** for regime horizons vs behavior horizons.

- Regime horizons: keep using `prediction.forward_horizons_quarters` (or migrate to a dedicated key during planning).
- Behavior horizons: add a separate key (e.g. `prediction.behavior_horizons_quarters`).

Rationale: regime-transition forecasting horizons and behavior horizons may diverge over time; keep explicit.

## Code Context / Integration Points (informational)

- Step 2 produces both:
  - `data/processed/features.parquet` (centered; for clustering/regimes)
  - `data/processed/features_supervised.parquet` (causal; for supervised models)
- Step 5 currently prefers supervised features but historically allowed fallback; Phase 3 will gate this behind an explicit opt-in flag.
- Regime labels: `data/regimes/cluster_labels.parquet` (column `balanced_cluster`).

## Deferred / Out-of-Scope (for this phase)

- New model families (e.g. LightGBM) unless already planned elsewhere.
- Anything beyond ETFs, intraday cadence, or automated execution.

