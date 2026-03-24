## Trading-Crab — Milestone **v1.2** requirements

**Defined:** 2026-03-21  
**Core value:** Transparent, regime-aware ETF guidance (unchanged — see `PROJECT.md`).

Prior milestone: **v1.0** archived at `.planning/milestones/v1.0-REQUIREMENTS.md`.

**Gap closure:** **`$gsd-audit-milestone`** reported **`gaps_found`** (see **`.planning/v1.2-MILESTONE-AUDIT.md`**). **Phase 26** (GSD verification + roadmap + Nyquist 17–19) is **complete** (2026-03-24). **Phase 27** (weekly pipeline E2E + dashboard model wiring) remains **pending** for the listed SIGNAL/MODEL/TACTICS/EMAIL/INSTALL integration items.

---

## v1.2 — Tactics, triggers & expanded signals

### 1. Data & APIs

- [x] **DATA-10** — Additional FRED series & yield spreads  
  Ingest and align (with publication lags) high-value series (e.g. VIXCLS, UNRATE, M2, GS2, T10Y2Y, T10Y3M, HOUST, UMCSENT where configured). Derived spreads in `transforms.py` with causal / non-causal parity. *Prior delivery: Phase 17 — `config/settings.yaml` `features.*` + `17-CONTEXT.md`.* **Phase 26** — ROADMAP + `17-VERIFICATION.md` `passed` + `17-VALIDATION.md`.

- [x] **DATA-11** — Optional / configurable extra price & data providers  
  Strengthen stooq fallback; evaluate optional APIs (finviz Elite, etc.) behind config flags without breaking checkpoint contracts. *Prior delivery: Phase 22 — `assets.providers`, `tests/unit/test_assets_providers.py`.* **Phase 26** — `22-VERIFICATION.md`.

### 2. Signals & diagnostics

- [ ] **SIGNAL-10** — Ratio & trigger diagnostics  
  Config-driven cross-asset ratios (e.g. Oil:Gold, Oil:Bonds, Bonds:Gold, Lumber:Gold proxy, narrative “Saylor↔Schiff-style” views). Surface as parquet + plots/tables before promoting to model features. *Prior delivery: Phase 18.* **Pending gap closure Phase 27** (weekly E2E vs step 8).

- [ ] **SIGNAL-11** — Relative rotation / RS-style diagnostics  
  RS-ratio / RS-momentum vs benchmark(s); machine-readable artifacts and notebook/report hooks. *Prior delivery: Phase 18.* **Pending gap closure Phase 27**.

### 3. Models

- [ ] **MODEL-10** — Gradient-boosted classifiers/regressors  
  Sklearn `GradientBoostingClassifier` alongside RF/DT for current regime and forward horizons; same causal-feature and TimeSeriesSplit discipline; `boosted_*` hyperparameters from `settings.yaml`. *Prior delivery: Phase 19.* **Pending gap closure Phase 27** (dashboard vs training path).

- [ ] **MODEL-11** — Interpretability trees on boosted feature importances  
  Shallow `DecisionTreeClassifier` on top‑K features from the GB model; `current_regime_tree_gb.txt`. *Prior delivery: Phase 19.* **Pending gap closure Phase 27**.

### 4. Tactics

- [ ] **TACTICS-10** — Strategy vs tactics classification  
  Classify assets/templates into buy-and-hold vs swing vs stand-aside using multi-horizon volatility, trend, correlations; weekly-entry bias; soft stops (e.g. anchored VWAP ideas) — no mandatory auto-execution. *Prior delivery: Phase 20.* **Pending gap closure Phase 27** (weekly E2E vs step 9).

### 5. Email & ops

- [ ] **EMAIL-10** — SMTP weekly report delivery  
  Optional send of `weekly_report.md` (or derived HTML/text) using local untracked config; no secrets in git. *Prior delivery: Phase 21.* **Pending gap closure Phase 27** (`run_weekly_report.py` + same-run diagnostics/tactics).

- [ ] **INSTALL-20** — Setup helper for new secrets & env  
  Scripts/docs to scaffold `.env`, email config templates, smoke checks (extends v1 installer story without duplicating v1 **INSTALL-10** scope). *Prior delivery: Phase 21.* **Pending gap closure Phase 27**.

### 6. v1.0 planning evidence closure (GSD hygiene for phases 1–16)

These requirements make **`gsd-tools stats` / `validate health` / plan–summary parity** align with **shipped v1.0 product work**. They do not re-open the v1.0 **code** scope unless explicitly noted (**CLOSURE-03**).

- [x] **CLOSURE-01** — Per-plan `*-SUMMARY.md` for every remaining `*-PLAN.md`  
  Add a summary file whose basename matches each plan (same rule as `validate health` I001). *Prior delivery: Phase 23.* **Phase 26** — `23-VERIFICATION.md`.

- [x] **CLOSURE-02** — Brownfield phase directories **04–11** (no historical `*-PLAN.md`)  
  Add a short **`README.md`** in each target directory. *Prior delivery: Phase 24.* **Phase 26** — `24-VERIFICATION.md`.

- [x] **CLOSURE-03** — Phase **3** plan **04** (`03-supervised-regime-behavior-models-04-PLAN.md`)  
  Reconcile plan `must_haves` against the repo. *Prior delivery: Phase 25 + `03-supervised-regime-behavior-models-04-SUMMARY.md`.* **Phase 26** — `25-VERIFICATION.md`.

---

## Deferred (not v1.2 unless pulled in)

- HMM / temporal clustering (tier-2 roadmap).
- Full broker execution.

---

## Out of scope (unchanged)

- Single-name stocks; on-chain crypto; intraday strategies; auto-execution.

---

## Traceability

| Requirement | Gap closure phase | Status |
|-------------|-------------------|--------|
| DATA-10 | Phase 26 | Complete |
| DATA-11 | Phase 26 | Complete |
| CLOSURE-01 | Phase 26 | Complete |
| CLOSURE-02 | Phase 26 | Complete |
| CLOSURE-03 | Phase 26 | Complete |
| SIGNAL-10, SIGNAL-11 | Phase 27 | Pending |
| MODEL-10, MODEL-11 | Phase 27 | Pending |
| TACTICS-10 | Phase 27 | Pending |
| EMAIL-10, INSTALL-20 | Phase 27 | Pending |

*Phase 26 GSD evidence complete. **Phase 27** + **`$gsd-audit-milestone`** still track integration/E2E closure.*
