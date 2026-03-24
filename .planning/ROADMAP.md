## Trading-Crab Roadmap

## Milestones

- ✅ **v1.0 — Core pipeline + planning evidence** — Phases 1–16 (shipped 2026-03-20) — [full roadmap](milestones/v1.0-ROADMAP.md) · [requirements](milestones/v1.0-REQUIREMENTS.md) · [audit](milestones/v1.0-MILESTONE-AUDIT.md)
- 🚧 **v1.2 — Tactics, triggers & expanded signals** — Phases 17–27 (in planning / execution; **26–27** = gap closure from `v1.2-MILESTONE-AUDIT.md`)

---

## Phases (v1.2 — current)

**Gap closure (milestone audit — `.planning/v1.2-MILESTONE-AUDIT.md`):**

- [x] **Phase 26: v1.2 — Audit verification files & roadmap alignment** — **CLOSURE-01**, **CLOSURE-02**, **CLOSURE-03**, **DATA-10**, **DATA-11**
- [x] **Phase 27: v1.2 — Pipeline weekly E2E & dashboard model wiring** — **SIGNAL-10**, **SIGNAL-11**, **TACTICS-10**, **MODEL-10**, **MODEL-11**, **EMAIL-10**, **INSTALL-20**

**New product work (DATA/SIGNAL/MODEL/tactics/email):**

- [x] **Phase 17: v1.2 — Expanded macro & yield data** — **DATA-10**
- [x] **Phase 18: v1.2 — Signal & diagnostic layer** — **SIGNAL-10**, **SIGNAL-11**
- [x] **Phase 19: v1.2 — Boosted models & interpretability trees** — **MODEL-10**, **MODEL-11**
- [x] **Phase 20: v1.2 — Tactics classification** — **TACTICS-10**
- [x] **Phase 21: v1.2 — Email delivery & install hardening** — **EMAIL-10**, **INSTALL-20**
- [x] **Phase 22: v1.2 — Providers & ETF universe** — **DATA-11**

**v1.0 GSD / evidence closure (stats tool showed “missing plans/summaries” for shipped phases):**

- [x] **Phase 23: v1.2 — v1.0 plan ↔ summary parity** — **CLOSURE-01**
- [x] **Phase 24: v1.2 — v1.0 brownfield phase READMEs** — **CLOSURE-02**
- [x] **Phase 25: v1.2 — Phase 3 plan 04 reconciliation** — **CLOSURE-03**

---

## Phase Details

### Phase 17: v1.2 — Expanded macro & yield data
**Goal:** Extend FRED ingest and feature engineering with additional series and yield-curve / spread features, preserving publication-lag rules and causal variants.  
**Depends on:** v1.0 pipeline (checkpoints, `settings.yaml`).  
**Requirements:** DATA-10  
**Success criteria:**
  1. New series listed in `config/settings.yaml` ingest in step 1 when API available.
  2. Derived spreads/features documented and produced in causal + non-causal feature artifacts.
  3. Tests or smoke paths cover new columns without breaking clustering defaults.

### Phase 18: v1.2 — Signal & diagnostic layer
**Goal:** Prominent ratio/trigger diagnostics and RS/RRG-style tables vs benchmarks.  
**Depends on:** Phase 17 (data); existing diagnostics step patterns.  
**Requirements:** SIGNAL-10, SIGNAL-11  
**Success criteria:**
  1. Config-driven ratio definitions with stable parquet outputs.
  2. At least one benchmark-relative rotation/RS artifact for the ETF universe.
  3. Weekly report and/or plots reference new sections when configured.

### Phase 19: v1.2 — Boosted models & interpretability trees
**Goal:** Add LightGBM/XGBoost-style models and shallow decision trees on top feature sets for interpretability.  
**Depends on:** Phases 1–5 equivalent (supervised step); causal features.  
**Requirements:** MODEL-10, MODEL-11  
**Success criteria:**
  1. Train/eval hooks parallel to RF/DT with time-series CV.
  2. Metrics persisted alongside existing model artifacts.
  3. Human-readable tree/plot/text for one boosted model per task family.

### Phase 20: v1.2 — Tactics classification
**Goal:** Asset/tactics buckets (hold / swing / stand-aside) using vol, trend, correlation signals.  
**Depends on:** Phase 18–19; existing tactics artifact patterns.  
**Requirements:** TACTICS-10  
**Success criteria:**
  1. Stable parquet output keyed by ETF and date/quarter.
  2. Weekly report section when artifact present.
  3. Unit tests for label logic on synthetic fixtures.

### Phase 21: v1.2 — Email delivery & install hardening
**Goal:** Reliable optional SMTP send for weekly report; improved setup docs/scripts for secrets.  
**Depends on:** Report pipeline (v1.0).  
**Requirements:** EMAIL-10, INSTALL-20  
**Success criteria:**
  1. Documented `--send-email` or equivalent path with local config template.
  2. No secrets committed; `.gitignore` verified.
  3. One-command or two-command “happy path” documented in `scripts/README.md` or similar.

### Phase 22: v1.2 — Providers & ETF universe ✅
**Goal:** Optional data providers and broader ETF list behind config; preserve checkpoint contracts.  
**Depends on:** Phase 17; ingestion module patterns.  
**Requirements:** DATA-11 (done — see `phases/22-v1-2-providers-universe/22-SUMMARY.md`)  
**Success criteria:**
  1. Provider modules are optional and fail soft when keys missing.
  2. ETF universe expansion documented in `settings.yaml`.
  3. Regression tests for ingestion contracts.

### Phase 23: v1.2 — v1.0 plan ↔ summary parity ✅
**Goal:** Satisfy **`validate health` I001** / `gsd-tools stats` plan–summary expectations for every **non–plan-04** plan file under `.planning/phases/` from milestone v1.0.  
**Depends on:** Nothing blocking (documentation).  
**Requirements:** CLOSURE-01 (done — see `phases/23-v1-0-plan-summary-parity/23-SUMMARY.md`)  
**Success criteria:**
  1. For each plan in **CLOSURE-01** list, a matching `*-SUMMARY.md` exists (basename alignment), or the plan is explicitly superseded in git with a one-line pointer SUMMARY.
  2. `gsd-tools validate health` shows **no I001** for those paths (or accepted project convention documented in this phase’s SUMMARY).
  3. Phase-level `NN-SUMMARY.md` referenced where it remains canonical.

### Phase 24: v1.2 — v1.0 brownfield phase READMEs
**Goal:** Phases **04–11** that shipped **without** a historical `*-PLAN.md` still have a **discoverable** anchor for auditors.  
**Depends on:** CLOSURE-01 optional ordering (can parallelize).  
**Requirements:** CLOSURE-02  
**Success criteria:**
  1. Each directory listed in **CLOSURE-02** has a **`README.md`** with: pointer to `*-VERIFICATION.md`, `*-VALIDATION.md`, and primary code/pipeline entrypoints.
  2. No claim of “not started” left standing for product scope—only GSD artifact debt.

### Phase 25: v1.2 — Phase 3 plan 04 reconciliation
**Goal:** Close or explicitly defer **`03-supervised-regime-behavior-models-04-PLAN.md`** (supervised metrics, behavior models wiring, leakage guardrails).  
**Depends on:** Understanding current `trading_crab_lib` / `05_predict` vs plan `must_haves`.  
**Requirements:** CLOSURE-03  
**Success criteria:**
  1. Matrix: each **must_have** truth → evidence path in repo **or** **documented waiver** with owner/date.
  2. **`03-supervised-regime-behavior-models-04-SUMMARY.md`** exists (executed, waived, or split follow-up).
  3. **`03-*-VERIFICATION.md`** / **`03-VALIDATION.md`** updated if product state changed.

### Phase 26: v1.2 — Audit verification files & roadmap alignment
**Goal:** Close GSD **verification** gaps from **`v1.2-MILESTONE-AUDIT.md`**: add `*-VERIFICATION.md` for phases **21–25**; reconcile **ROADMAP** Phase **17** checkbox / Progress row with shipped **DATA-10** work; set **`17-VERIFICATION.md`** frontmatter to **`passed`** when evidence is complete; optionally add **`*-VALIDATION.md`** skeletons for phases **17–19** (Nyquist parity) or document waivers.  
**Depends on:** Existing SUMMARY/VALIDATION artifacts in phases 21–25.  
**Requirements:** CLOSURE-01, CLOSURE-02, CLOSURE-03, DATA-10, DATA-11  
**Gap closure:** Audit — missing phase VERIFICATION files; roadmap drift; Nyquist files for 17–19.

### Phase 27: v1.2 — Pipeline weekly E2E & dashboard model wiring
**Goal:** Close **integration / flow** gaps: ensure a single run can produce **Diagnostics** + **Tactics** in **`weekly_report.md`** (step order, optional second pass of step **7**, or documented contract); extend **`scripts/run_weekly_report.py`** to include steps **8–9** and a final report pass when appropriate; resolve **RF vs GB** for dashboard/step-7 scoring via **config + docs** (or explicit waiver).  
**Depends on:** Phase 26 optional (docs can land in parallel).  
**Requirements:** SIGNAL-10, SIGNAL-11, TACTICS-10, MODEL-10, MODEL-11, EMAIL-10, INSTALL-20  
**Gap closure:** Audit — step 7 vs 8/9 ordering; weekly script scope; boosted model not on live dashboard path.

---

## Progress

| Phase | Name | Plans Complete | Status | Notes |
|-------|------|----------------|--------|-------|
| 17 | Expanded macro & yield data | 1/1 | Complete | DATA-10 — see `17-VERIFICATION.md` |
| 18 | Signal & diagnostic layer | 1/? | Complete | |
| 19 | Boosted models & trees | 1/? | Complete | |
| 20 | Tactics classification | 1/1 | Complete | TACTICS-10 |
| 21 | Email & install | 1/1 | Complete | EMAIL-10, INSTALL-20 |
| 22 | Providers & universe | 1/1 | Complete | DATA-11 |
| 23 | v1.0 plan ↔ summary parity | 1/1 | Complete | CLOSURE-01 |
| 24 | v1.0 brownfield READMEs | 1/1 | Complete | CLOSURE-02 |
| 25 | Phase 3 plan 04 reconciliation | 1/1 | Complete | CLOSURE-03 |
| 26 | Audit verification & roadmap | 1/1 | Complete | Gap closure — VERIFICATION + VALIDATION 17–19 |
| 27 | Pipeline weekly E2E & dashboard model | 1/1 | Complete | Gap closure — step order, regime_model, tests |
