## Trading-Crab Roadmap

## Current focus: v1.5 — Template hardening & doc parity *(active)*

**Milestone:** v1.5 — phases **37–39**  
**Requirements:** **`.planning/REQUIREMENTS.md`** (TMPL-01 … TMPL-03)

### Phase overview

| # | Name | Goal | Requirements | Success criteria (observable) |
|---|------|------|--------------|------------------------------|
| **37** | Fork & dependency docs | Forks know how to install and which file is canonical for deps | TMPL-01 | Complete — `docs/DEPENDENCIES.md` + README/CURSOR links (2026-03-27) |
| **38** | Backlog reconciliation | Product markdown matches code | TMPL-02 | Complete — `yc_*` / `build_forward_window_probabilities` docs; **TMPL-02** (2026-03-27) |
| **39** | Confusion matrix | Close CLAUDE visualization gap for classifiers | TMPL-03 | Plot saved under `outputs/plots/` when plots enabled; tests or smoke path documented |

### Phase 37 — Fork & dependency docs

- **Goal:** Remove ambiguity for new repos cloning this template.
- **Deliverables:** README section (or small `docs/DEPENDENCIES.md`) describing `pip install -e ".[dev]"` vs `requirements.txt`; optional `CONTRIBUTING.md` pointer.
- **Maps to:** TMPL-01

### Phase 38 — Backlog reconciliation

- **Goal:** No “phantom” gaps in top-level docs.
- **Deliverables:** Edits to `ROADMAP.md`, `FUTURE-TODO.md`, `CLAUDE.md` as needed; optional note in `v1.5-CLEANUP-BACKLOG.md` that items moved to shipped/deferred.
- **Maps to:** TMPL-02

### Phase 39 — Confusion matrix

- **Goal:** Per-class confusion matrix for current-regime (or CV) predictions — parity with legacy `supervised` reporting style.
- **Deliverables:** `plotting.plot_confusion_matrix` (or similar), call site from step 5 pipeline or metrics writer; PNG in `outputs/plots/`.
- **Maps to:** TMPL-03

---

## Milestones

- 🔄 **v1.5 — Template hardening & doc parity** — Phases **37–39** *(active)* — requirements: **`.planning/REQUIREMENTS.md`**
- ✅ **v1.0 — Core pipeline + planning evidence** — Phases 1–16 (shipped 2026-03-20) — [full roadmap](milestones/v1.0-ROADMAP.md) · [requirements](milestones/v1.0-REQUIREMENTS.md) · [audit](milestones/v1.0-MILESTONE-AUDIT.md)
- ✅ **v1.2 — Tactics, triggers & expanded signals** — Phases 17–27 (shipped 2026-03-24) — [full roadmap](milestones/v1.2-ROADMAP.md) · [requirements](milestones/v1.2-REQUIREMENTS.md) · [audit](milestones/v1.2-MILESTONE-AUDIT.md)
- ✅ **v1.3 — Consolidation, submodule parity & PyPI** — Phases 28–34 (shipped 2026-03-26) — [full roadmap](milestones/v1.3-ROADMAP.md) · [requirements](milestones/v1.3-REQUIREMENTS.md) · [audit](milestones/v1.3-MILESTONE-AUDIT.md)
- ✅ **v1.4 — Audit gap closure** — Phases 35–36 (shipped 2026-03-26) — [full roadmap](milestones/v1.4-ROADMAP.md) · [requirements](milestones/v1.4-REQUIREMENTS.md) · [audit](milestones/v1.4-MILESTONE-AUDIT.md)

## Phases (archived by milestone)

| Milestone | Phases | Roadmap archive |
|-----------|--------|-----------------|
| **v1.4** | 35–36 (AUDIT-10, DOC-ALIGN-10) | [milestones/v1.4-ROADMAP.md](milestones/v1.4-ROADMAP.md) |
| **v1.3** | 28–34 (GSD-10 … DOCS-10) | [milestones/v1.3-ROADMAP.md](milestones/v1.3-ROADMAP.md) |
| **v1.2** | 17–27 | [milestones/v1.2-ROADMAP.md](milestones/v1.2-ROADMAP.md) |
| **v1.0** | 1–16 | [milestones/v1.0-ROADMAP.md](milestones/v1.0-ROADMAP.md) |

Phase directories remain under **`.planning/phases/`** as execution history.

## Phase directory — 01 (Data & Constraints Foundations)

GSD folder **`01-data-and-constraints-foundations/`** — plans **`01-data-and-constraints-foundations-01-PLAN.md`**, **`01-data-and-constraints-foundations-02-PLAN.md`**, **`01-data-and-constraints-foundations-03-PLAN.md`**. Full narrative and success criteria: [v1.0 roadmap — Phase 1](milestones/v1.0-ROADMAP.md).

## Shipped phase checklist *(compact — details in milestone archives)*

- [x] **Phase 28: v1.3 — Hybrid PLAN/SUMMARY closure (I001)** — **GSD-10**
- [x] **Phase 29: v1.3 — Submodule comparison matrix (read-only mirrors)** — **SYNC-10**
- [x] **Phase 30: v1.3 — Submodule unification blueprint (owner gates)** — **SYNC-11**
- [x] **Phase 31: v1.3 — Library workspace & path API (PyPI-safe)** — **PKG-10**
- [x] **Phase 32: v1.3 — PyPI release engineering & publish story** — **PKG-11**
- [x] **Phase 33: v1.3 — Root prune (redundancy removal)** — **PRUNE-10**
- [x] **Phase 34: v1.3 — Library documentation & rationale pass** — **DOCS-10**
- [x] **Phase 35: v1.4 — Phase 28 verification parity (audit)** — **AUDIT-10**
- [x] **Phase 36: v1.4 — Root docs & import alignment** — **DOC-ALIGN-10**

## v1.5 execution checklist

- [x] **Phase 37** — TMPL-01 (fork & dependency docs) (completed 2026-03-27)
- [x] **Phase 38** — TMPL-02 (ROADMAP / FUTURE-TODO / CLAUDE reconciliation) (completed 2026-03-27)
- [ ] **Phase 39** — TMPL-03 (confusion matrix plot + wiring)
