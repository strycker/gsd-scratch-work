## Trading-Crab Roadmap

## Milestones

- ✅ **v1.0 — Core pipeline + planning evidence** — Phases 1–16 (shipped 2026-03-20) — [full roadmap](milestones/v1.0-ROADMAP.md) · [requirements](milestones/v1.0-REQUIREMENTS.md) · [audit](milestones/v1.0-MILESTONE-AUDIT.md)
- 🚧 **v1.2 — Tactics, triggers & expanded signals** — Phases 17–22 (in planning / execution)

---

## Phases (v1.2 — current)

- [ ] **Phase 17: v1.2 — Expanded macro & yield data** — Ingest/config **DATA-10**; derived spreads and causal parity in features.
- [ ] **Phase 18: v1.2 — Signal & diagnostic layer** — **SIGNAL-10**, **SIGNAL-11** artifacts, plots, report hooks.
- [ ] **Phase 19: v1.2 — Boosted models & interpretability trees** — **MODEL-10**, **MODEL-11** alongside existing stack.
- [ ] **Phase 20: v1.2 — Tactics classification** — **TACTICS-10** labels and reporting.
- [ ] **Phase 21: v1.2 — Email delivery & install hardening** — **EMAIL-10**, **INSTALL-20**; weekly report path.
- [ ] **Phase 22: v1.2 — Providers & ETF universe** — **DATA-11** optional providers; broaden universe safely.

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

### Phase 22: v1.2 — Providers & ETF universe
**Goal:** Optional data providers and broader ETF list behind config; preserve checkpoint contracts.  
**Depends on:** Phase 17; ingestion module patterns.  
**Requirements:** DATA-11  
**Success criteria:**
  1. Provider modules are optional and fail soft when keys missing.
  2. ETF universe expansion documented in `settings.yaml`.
  3. Regression tests for ingestion contracts.

---

## Progress

| Phase | Name | Plans Complete | Status | Notes |
|-------|------|----------------|--------|-------|
| 17 | Expanded macro & yield data | 0/? | Not started | |
| 18 | Signal & diagnostic layer | 0/? | Not started | |
| 19 | Boosted models & trees | 0/? | Not started | |
| 20 | Tactics classification | 0/? | Not started | |
| 21 | Email & install | 0/? | Not started | |
| 22 | Providers & universe | 0/? | Not started | |
