## Trading-Crab — Milestone **v1.2** requirements

**Defined:** 2026-03-21  
**Core value:** Transparent, regime-aware ETF guidance (unchanged — see `PROJECT.md`).

Prior milestone: **v1.0** archived at `.planning/milestones/v1.0-REQUIREMENTS.md`.

---

## v1.2 — Tactics, triggers & expanded signals

### 1. Data & APIs

- [x] **DATA-10** — Additional FRED series & yield spreads  
  Ingest and align (with publication lags) high-value series (e.g. VIXCLS, UNRATE, M2, GS2, T10Y2Y, T10Y3M, HOUST, UMCSENT where configured). Derived spreads in `transforms.py` with causal / non-causal parity. **Completed in Phase 17** — see `config/settings.yaml` `features.*` + `17-CONTEXT.md`.

- [ ] **DATA-11** — Optional / configurable extra price & data providers  
  Strengthen stooq fallback; evaluate optional APIs (finviz Elite, etc.) behind config flags without breaking checkpoint contracts.

### 2. Signals & diagnostics

- [x] **SIGNAL-10** — Ratio & trigger diagnostics  
  Config-driven cross-asset ratios (e.g. Oil:Gold, Oil:Bonds, Bonds:Gold, Lumber:Gold proxy, narrative “Saylor↔Schiff-style” views). Surface as parquet + plots/tables before promoting to model features. **Completed in Phase 18** — `diagnostics.trigger_defaults`, `compute_ratios_diagnostics`, plots `08_diagnostics_*.png`.

- [x] **SIGNAL-11** — Relative rotation / RS-style diagnostics  
  RS-ratio / RS-momentum vs benchmark(s); machine-readable artifacts and notebook/report hooks. **Completed in Phase 18** — `rrg_current.parquet`, `notebooks/08_diagnostics.ipynb`, weekly report **Diagnostics** section.

### 3. Models

- [x] **MODEL-10** — Gradient-boosted classifiers/regressors  
  Sklearn `GradientBoostingClassifier` alongside RF/DT for current regime and forward horizons; same causal-feature and TimeSeriesSplit discipline; `boosted_*` hyperparameters from `settings.yaml`. **Completed in Phase 19** — see `make_gradient_boosting_classifier`, `current_regime_gb.pkl`.

- [x] **MODEL-11** — Interpretability trees on boosted feature importances  
  Shallow `DecisionTreeClassifier` on top‑K features from the GB model; `current_regime_tree_gb.txt`. **Completed in Phase 19**.

### 4. Tactics

- [x] **TACTICS-10** — Strategy vs tactics classification  
  Classify assets/templates into buy-and-hold vs swing vs stand-aside using multi-horizon volatility, trend, correlations; weekly-entry bias; soft stops (e.g. anchored VWAP ideas) — no mandatory auto-execution. **Completed in Phase 20** — `src/trading_crab_lib/tactics.py` (`classification_version` v1 vs v1_2, `vol_aggregate`, `entry_bias_score`, `soft_stop_z`, `as_of` / `quarter_end`); artifact **`outputs/reports/tactics_signals.parquet`** (extra columns); optional weekly enrich via `tactics.weekly_report_enrich`.

### 5. Email & ops

- [ ] **EMAIL-10** — SMTP weekly report delivery  
  Optional send of `weekly_report.md` (or derived HTML/text) using local untracked config; no secrets in git.

- [ ] **INSTALL-20** — Setup helper for new secrets & env  
  Scripts/docs to scaffold `.env`, email config templates, smoke checks (extends v1 installer story without duplicating v1 **INSTALL-10** scope).

### 6. v1.0 planning evidence closure (GSD hygiene for phases 1–16)

These requirements make **`gsd-tools stats` / `validate health` / plan–summary parity** align with **shipped v1.0 product work**. They do not re-open the v1.0 **code** scope unless explicitly noted (**CLOSURE-03**).

- [ ] **CLOSURE-01** — Per-plan `*-SUMMARY.md` for every remaining `*-PLAN.md`  
  Add a summary file whose basename matches each plan (same rule as `validate health` I001). **Known gaps (2026-03-21):**  
  `06-weekly-report-pipeline-01-PLAN.md`, `08-data-signals-diagnostics-01-PLAN.md`, `12-v1-audit-verify-phases-4-6-01-PLAN.md`, `13-v1-audit-verify-phases-7-11-01-PLAN.md`, `15-v1-gap-regime-profiles-names-01-PLAN.md`, `16-v1-gap-e2e-integration-runbook-01-PLAN.md`.  
  Summaries may point to existing phase-level `NN-SUMMARY.md` where that file is the canonical narrative.

- [ ] **CLOSURE-02** — Brownfield phase directories **04–11** (no historical `*-PLAN.md`)  
  Add a short **`README.md`** in each of: `04-regime-conditional-etf-portfolio-behavior`, `05-recommendations-machine-readable-outputs`, `07-portfolio-and-email-integration`, `09-tactics-and-diagnostics`, `10-tactics-install`, `11-core-cleanup` (and **`06`**, **`08`** if not fully covered by **CLOSURE-01**) stating: work was delivered under v1.0; primary evidence is `*-VERIFICATION.md` / `*-VALIDATION.md` + `RUNBOOK.md` / pipeline entrypoints.

- [ ] **CLOSURE-03** — Phase **3** plan **04** (`03-supervised-regime-behavior-models-04-PLAN.md`)  
  Reconcile plan `must_haves` against the repo (`trading_crab_lib`, `pipelines/05_predict.py`, `outputs/reports/model_metrics/*`, tests). **Either:** implement/polish remaining gaps and update **VERIFICATION**/**VALIDATION**, **or** document a **signed waiver** (deferred items, rationale, optional follow-up REQ) in a new **`03-supervised-regime-behavior-models-04-SUMMARY.md`** plus a short note in **VERIFICATION**.

---

## Deferred (not v1.2 unless pulled in)

- HMM / temporal clustering (tier-2 roadmap).
- Full broker execution.

---

## Out of scope (unchanged)

- Single-name stocks; on-chain crypto; intraday strategies; auto-execution.

---

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| DATA-10 | Phase 17 | Complete |
| SIGNAL-10, SIGNAL-11 | Phase 18 | Complete |
| MODEL-10, MODEL-11 | Phase 19 | Complete |
| TACTICS-10 | Phase 20 | Complete |
| EMAIL-10, INSTALL-20 | Phase 21 | Not started |
| DATA-11 | Phase 22 | Not started |
| CLOSURE-01 | Phase 23 | Not started |
| CLOSURE-02 | Phase 24 | Not started |
| CLOSURE-03 | Phase 25 | Not started |
