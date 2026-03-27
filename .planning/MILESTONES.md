# Milestones

## v1.5 Template hardening & doc parity (Shipped: 2026-03-27)

**Phases completed:** 3 phases (37–39), 3 plans

**Archives:** `.planning/milestones/v1.5-ROADMAP.md`, `v1.5-REQUIREMENTS.md`, `v1.5-MILESTONE-AUDIT.md`

**Key accomplishments:**
- **TMPL-01 (Phase 37):** Added `docs/DEPENDENCIES.md` and linked it from `README.md` and `docs/CURSOR.md` for fork install clarity.
- **TMPL-02 (Phase 38):** Reconciled backlog docs (`ROADMAP.md`, `.planning/FUTURE-TODO.md`, `CLAUDE.md`) with shipped code (`yc_*`, `build_forward_window_probabilities`).
- **TMPL-03 (Phase 39):** Shipped confusion-matrix visualization (`plot_regime_confusion_matrix`), wired step-5 plot paths, and added validation tests.

---

## v1.4 Audit gap closure (Shipped: 2026-03-26)

**Phases completed:** 2 phases (35–36), 2 plans

**Archives:** `.planning/milestones/v1.4-ROADMAP.md`, `v1.4-REQUIREMENTS.md`, `v1.4-MILESTONE-AUDIT.md`

**Key accomplishments:**

- **AUDIT-10:** Formal **`28-VERIFICATION.md`** (validate health + hybrid I001 evidence) — **Phase 35**.
- **DOC-ALIGN-10:** Root **`trading_crab_lib`** onboarding; **`34-VALIDATION`** Nyquist complete; **`34-VERIFICATION`** refreshed — **Phase 36**.

---

## v1.3 Consolidation, submodule parity & PyPI (Shipped: 2026-03-26)

**Phases completed:** 7 phases (28–34), 7 plans

**Archives:** `.planning/milestones/v1.3-ROADMAP.md`, `v1.3-REQUIREMENTS.md`, `v1.3-MILESTONE-AUDIT.md`

**Key accomplishments:**

- **GSD-10 / I001:** Hybrid `*-SUMMARY.md` beside remaining v1.2 plans; **`validate health`** clean for listed paths (**Phase 28**).
- **SYNC-10 / SYNC-11:** Submodule comparison matrix + ordered unification blueprint (read-only mirrors) ( **29–30** ).
- **PKG-10 / PKG-11:** `paths.py` consumer-safe workspace API; PyPI release story (**LICENSE**, **`docs/RELEASING.md`**, **`scripts/build_dist.sh`**) (**31–32**).
- **PRUNE-10:** Root inventory and redundancy removal outside `legacy/` / mirrors (**33**).
- **DOCS-10:** Google-style docstrings + file-level “why” across `src/trading_crab_lib/` (**34**).

---

## v1.2 Tactics, triggers & expanded signals (Shipped: 2026-03-24)

**Phases completed:** 11 phases, 11 plans

**Archives:** `.planning/milestones/v1.2-ROADMAP.md`, `v1.2-REQUIREMENTS.md`, `v1.2-MILESTONE-AUDIT.md`

**Key accomplishments:**

- Expanded macro ingest and yield-curve / spread features (FRED + `transforms.py`); optional price providers and broader ETF universe behind config (**DATA-10**, **DATA-11**).
- Signal & diagnostic layer: ratio triggers, RS/RRG-style tables, parquet + report hooks (**SIGNAL-10**, **SIGNAL-11**).
- Boosted classifiers (sklearn `GradientBoostingClassifier`) with TS-CV, metrics, interpretability trees; live dashboard picks **RF vs GB** via **`dashboard.regime_model`** (**MODEL-10**, **MODEL-11**).
- Tactics classification (hold / swing / stand-aside) with tests and weekly report integration (**TACTICS-10**).
- Email/install hardening; GSD evidence closure (**CLOSURE-01..03**); milestone verification + Nyquist **VALIDATION** for phases **17–19**.
- Pipeline integration: **`resolve_pipeline_step_order`** runs **8 → 9 → 7** when combined; **`scripts/run_weekly_report.py`** defaults include **8–9** before **7**; unit tests in **`test_run_pipeline_step_order.py`**.

---

## v1.0 Core pipeline + planning evidence (Shipped: 2026-03-20)

**Phases completed:** 16 phases, 17 plans, 0 tasks

**Archives:** `.planning/milestones/v1.0-ROADMAP.md`, `v1.0-REQUIREMENTS.md`, `v1.0-MILESTONE-AUDIT.md`

**Key accomplishments:**

- End-to-end regime pipeline: checkpointed ingest/features, PCA+KMeans regimes, supervised models, ETF returns, dashboard + weekly report (steps 1–7; 8–9 diagnostics/tactics).
- GSD evidence closure: phase `VERIFICATION.md` / `VALIDATION.md` for all 16 phases; `REQUIREMENTS.md` traceability 30/30 Complete; milestone audit **tech_debt** (ops notes only).
- REGIME-02/03 closure: pinned `regime_labels.yaml`; ETF-by-regime artifact `etf_behavior_by_regime.parquet` + tests; Phase 2 verification **passed**.
- Integration contract: root **`RUNBOOK.md`** (golden path, `market_code`, checkpoints, steps 8–9); **`ARCHITECTURE.md`** link.

---

## v1.1 ETF Behavior & Portfolios (Shipped: 2026-03-17)

**Phases completed:** 4 phases, 9 plans, 0 tasks

**Key accomplishments:**

- (none recorded)

---

## v1.0 v1.0 Trading-Crab (Shipped: 2026-03-16)

**Phases completed:** 3 phases, 8 plans, 0 tasks

**Key accomplishments:**

- (none recorded)

---
