## Trading-Crab — Milestone **v1.2** requirements

**Defined:** 2026-03-21  
**Core value:** Transparent, regime-aware ETF guidance (unchanged — see `PROJECT.md`).

Prior milestone: **v1.0** archived at `.planning/milestones/v1.0-REQUIREMENTS.md`.

---

## v1.2 — Tactics, triggers & expanded signals

### 1. Data & APIs

- [ ] **DATA-10** — Additional FRED series & yield spreads  
  Ingest and align (with publication lags) high-value series (e.g. VIXCLS, UNRATE, M2, GS2, T10Y2Y, T10Y3M, HOUST, UMCSENT where configured). Derived spreads in `transforms.py` with causal / non-causal parity.

- [ ] **DATA-11** — Optional / configurable extra price & data providers  
  Strengthen stooq fallback; evaluate optional APIs (finviz Elite, etc.) behind config flags without breaking checkpoint contracts.

### 2. Signals & diagnostics

- [ ] **SIGNAL-10** — Ratio & trigger diagnostics  
  Config-driven cross-asset ratios (e.g. Oil:Gold, Oil:Bonds, Bonds:Gold, Lumber:Gold proxy, narrative “Saylor↔Schiff-style” views). Surface as parquet + plots/tables before promoting to model features.

- [ ] **SIGNAL-11** — Relative rotation / RS-style diagnostics  
  RS-ratio / RS-momentum vs benchmark(s); machine-readable artifacts and notebook/report hooks.

### 3. Models

- [ ] **MODEL-10** — Gradient-boosted classifiers/regressors  
  LightGBM or XGBoost (or similar) alongside RF/DT for current regime and forward horizons; same causal-feature and TimeSeriesSplit discipline.

- [ ] **MODEL-11** — Interpretability trees on boosted feature importances  
  Fit shallow `DecisionTreeClassifier` on top-ranked features from boosted models; text/plot output for review.

### 4. Tactics

- [ ] **TACTICS-10** — Strategy vs tactics classification  
  Classify assets/templates into buy-and-hold vs swing vs stand-aside using multi-horizon volatility, trend, correlations; weekly-entry bias; soft stops (e.g. anchored VWAP ideas) — no mandatory auto-execution.

### 5. Email & ops

- [ ] **EMAIL-10** — SMTP weekly report delivery  
  Optional send of `weekly_report.md` (or derived HTML/text) using local untracked config; no secrets in git.

- [ ] **INSTALL-20** — Setup helper for new secrets & env  
  Scripts/docs to scaffold `.env`, email config templates, smoke checks (extends v1 installer story without duplicating v1 **INSTALL-10** scope).

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
| DATA-10 | Phase 17 | Not started |
| SIGNAL-10, SIGNAL-11 | Phase 18 | Not started |
| MODEL-10, MODEL-11 | Phase 19 | Not started |
| TACTICS-10 | Phase 20 | Not started |
| EMAIL-10, INSTALL-20 | Phase 21 | Not started |
| DATA-11 | Phase 22 | Not started |
