---
phase: 16-v1-gap-e2e-integration-runbook
gathered: 2026-03-20
status: ready_for_planning
source: "$gsd:discuss-phase 16 (non-interactive — recommended defaults applied)"
tags: [v1.0, gap-closure, integration, runbook, e2e]
---

# Phase 16: v1.0 Gap Closure — E2E runbook & integration contract — Context

**Gathered:** 2026-03-20  
**Status:** Ready for planning

<domain>
## Phase boundary

Deliver **documentation only** (no new pipeline features unless a one-line cross-link is needed): one **canonical operational runbook** that closes **`$gsd-audit-milestone` `gaps.integration`** — `market_code` / checkpoint discipline, a **repeatable golden-path** recipe (including post–re-cluster `regime_labels.yaml` hygiene), and explicit clarity on **core steps 1–7** vs **extended 8–9** for DIAG/TACTICS/report excerpts.

Discussion clarifies **where** and **how deep** the doc goes, not whether to add new capabilities. Out of scope: automatic checkpoint invalidation engineering, new FRED series, SMTP automation — **v1.2 / backlog** (`<deferred>`).

</domain>

<discuss_phase_note>
## Gray areas (presented) → resolutions

*Interactive multi-select was not available; below are the **recommended defaults** applied so planning can proceed without re-asking.*

| Area | Resolution |
|------|--------------|
| **Doc home** | Add **`RUNBOOK.md`** at **repository root** (next to `README.md` / `CLAUDE.md` for discoverability). Optionally add a **single** pointer sentence in `ARCHITECTURE.md` (“Operational sequences → `RUNBOOK.md`”) — avoid duplicating the full flag table if `CLAUDE.md` / `run_pipeline.py` docstring already list flags; **link** instead. |
| **Depth** | **Golden path** (fresh machine / CI-style sanity) + **partial rerun** recipe + **checkpoint / `market_code` consistency** + **post–cluster YAML checklist** + **§ Extended: steps 8–9**. Keep under ~300 lines unless planner expands with tables. |
| **Audience** | Maintainers and contributors who already use `pip install -e ".[dev]"` and read `CLAUDE.md`. Not an end-user trading guide. |
| **Audit traceability** | Include a **mapping table**: each bullet from `.planning/v1.0-MILESTONE-AUDIT.md` `gaps.integration` and relevant `tech_debt.operational` rows → **anchor heading** in `RUNBOOK.md` (for re-audit evidence). |
| **Naming default for `market_code`** | Document **recommended default:** train/score/report using a **single** label source end-to-end — e.g. **`predicted`** after a full 1–5 run, or **`clustered`** with `--save-market-code` after step 3; never mix without re-running downstream steps. |

</discuss_phase_note>

<decisions>
## Implementation decisions

### Runbook location and shape
- Primary artifact: **`RUNBOOK.md`** (repo root).
- Structure (locked headings for audit mapping):
  1. Prerequisites (venv, `.env`, optional `k-means-constrained`)
  2. Golden path — full refresh (`--refresh --recompute` …) vs incremental (from checkpoints)
  3. **`--market-code` / `--save-market-code`** — semantic contract + worked examples mirroring `run_pipeline.py` header comments
  4. **Checkpoint hygiene** — when to `--recompute` / `--refresh`; staleness risk when `clustering_features`, `regime_labels.yaml`, or label column choice changes; pointer to `CheckpointManager` / manifest (`data/checkpoints/`)
  5. **Post–re-cluster checklist** — re-run steps 3+; refresh `config/regime_labels.yaml` if cluster IDs shift; confirm `balanced_k` alignment
  6. **Extended pipeline — steps 8–9** — which artifacts/report sections need them; command to run `run_pipeline.py --steps …`
  7. **Audit integration index** — table: audit finding → RUNBOOK §

### Cross-links (minimal churn)
- Do **not** duplicate the entire `CLAUDE.md` flag table in `RUNBOOK.md` — summarize **decision-relevant** flags and link **`CLAUDE.md`** / **`run_pipeline.py`** for exhaustive CLI reference.
- **`ARCHITECTURE.md`**: add at most **one** short subsection or bullet under introduction pointing to `RUNBOOK.md` for operational flows (planner chooses exact placement).

### Claude's discretion
- Subsection ordering inside `RUNBOOK.md` if the outline above fits better merged (e.g. combine golden path + partial rerun).
- Tone (bullets vs numbered steps); optional `mermaid` diagram for step flow only if it fits without scope creep.
- Whether to add a **second** link from `README.md` “Development” — nice-to-have; not required if `ARCHITECTURE.md` points to `RUNBOOK.md`.

</decisions>

<canonical_refs>
## Canonical references

**Downstream agents MUST read these before planning or implementing.**

### Planning + audit source
- `.planning/ROADMAP.md` — **Phase 16** goal, success criteria, requirement evidence targets.
- `.planning/v1.0-MILESTONE-AUDIT.md` — YAML `gaps.integration`, `tech_debt.operational` (lines to cite in RUNBOOK index).
- `.planning/STATE.md` — current milestone / phase cursor after Phase 15.

### Product contracts
- `CLAUDE.md` — pipeline steps, flags, checkpoints, non-negotiables (publication lag, feature order).
- `run_pipeline.py` — authoritative `--market-code` / `--save-market-code` documentation in module docstring and argparse help.
- `ARCHITECTURE.md` — causal vs centered features, PCA=5, two feature checkpoints (invariants runbook must not contradict).

### Config / artifacts
- `config/settings.yaml` — `clustering.balanced_k`, feature lists, `assets.etfs`.
- `config/regime_labels.yaml` — pinned IDs (post–Phase 15: 0–4).

### Implementation touchpoints (for accurate prose)
- `src/trading_crab_lib/io/checkpoints.py` — `CheckpointManager` behavior (names only in runbook unless planner tasks code change).

</canonical_refs>

<code_context>
## Existing code insights

### Reusable assets
- **`run_pipeline.py`** — Already documents `market_code` modes (`grok`, `clustered`, `predicted`, named checkpoints); runbook should **align** wording with this file, not invent new semantics.
- **`ARCHITECTURE.md`** — Explains `features` vs `features_supervised`; runbook should warn: supervised steps must use **causal** feature checkpoint consistent with training.

### Established patterns
- **Step numbering 1–7** “core” vs **8–9** diagnostics/tactics in `CLAUDE.md` / `pipelines/` layout.
- Checkpoints under `data/checkpoints/`; regime outputs under `data/regimes/`; reports under `outputs/reports/`.

### Integration points
- Phase 16 deliverable is **markdown + light cross-links**; wiring is reader mental model, not new imports.

</code_context>

<specifics>
## Specific ideas

- Mirror the **three worked examples** already in `run_pipeline.py` top docstring (`--market-code grok`, `clustered`, `predicted`) in the runbook for copy-paste fidelity.
- Call out **REPORT-03 / INSTALL-10** as environment-dependent (SMTP) per audit `tech_debt` — file-based report is the no-secrets path.

</specifics>

<deferred>
## Deferred ideas

- **Automatic checkpoint invalidation** when `settings.yaml` hashes or `regime_labels.yaml` change — engineering task, not Phase 16 doc-only scope.
- **CI job** that runs a mocked golden path — separate phase or v1.2 hygiene.
- **Expanded FRED / v1.2 tactics** — roadmap `PROJECT.md` v1.2 milestone.

</deferred>

---

*Phase: 16-v1-gap-e2e-integration-runbook*  
*Context gathered: 2026-03-20 — `$gsd:discuss-phase 16` (defaults applied)*
