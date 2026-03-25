# Trading-Crab — Requirements (v1.3)

**Milestone:** v1.3 — Consolidation, submodule parity & PyPI  
**Research:** `.planning/research/SUMMARY.md` (2026-03-25)

**Archived:** v1.0 / v1.2 — `.planning/milestones/v1.*-REQUIREMENTS.md`

---

## 1. GSD & planning hygiene

- [x] **GSD-10** — Hybrid **`*-SUMMARY.md`** for all **I001** plan paths (v1.2 phases **17–22**, **26–27**)  
  Each file: **As-built**, **Plan fidelity**, **Delta from plan**; satisfy **`gsd-tools validate health`**. **Evidence:** `.planning/phases/28-v1-3-hybrid-i001-summaries/28-SUMMARY.md`.

## 2. Submodule analysis & merge blueprint

- [x] **SYNC-10** — Matrix comparing root vs `trading-crab-lib-repo-copy`, `claude-scratch-work-repo-copy`, `trading-crab-repo-copy` (read-only mirrors). **Roadmap:** **Phase 29**. **Evidence:** `.planning/research/SUBMODULE_COMPARISON_MATRIX.md`, **`.planning/phases/29-v1-3-submodule-comparison-matrix/29-SUMMARY.md`**.
- [x] **SYNC-11** — Ordered unification blueprint (lib → claude-scratch → trading-crab) with owner-confirm gates. **Roadmap:** **Phase 30**. **Evidence:** `.planning/research/SUBMODULE_UNIFICATION_BLUEPRINT.md`, **`.planning/phases/30-v1-3-submodule-unification-blueprint/30-SUMMARY.md`**.

## 3. Library packaging & PyPI

- [ ] **PKG-10** — Consumer-safe workspace/path API for `pip install` (no implicit repo `ROOT`). **Roadmap:** **Phase 31**.
- [ ] **PKG-11** — Release engineering: build, TestPyPI, PyPI, trusted publishing, README install story. **Roadmap:** **Phase 32**.

## 4. Root prune & narrative docs

- [ ] **PRUNE-10** — Remove redundant root notebooks/scratch/duplicate docs (excluding `legacy/`, `*_repo-copy/`). **Roadmap:** **Phase 33**.
- [ ] **DOCS-10** — Extensive Google-style docstrings + file “why” + major-block rationale under `src/trading_crab_lib/`. **Roadmap:** **Phase 34**.

---

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| GSD-10 | 28 | Complete |
| SYNC-10 | 29 | Complete |
| SYNC-11 | 30 | Complete |
| PKG-10 | 31 | Not started |
| PKG-11 | 32 | Not started |
| PRUNE-10 | 33 | Not started |
| DOCS-10 | 34 | Not started |

**Milestone v1.3 roadmap scope:** phases **28–34** on **`.planning/ROADMAP.md`** (all REQ rows above are mapped).
