# Trading-Crab — Requirements (v1.3 + v1.4)

**Milestone (shipped):** v1.3 — Consolidation, submodule parity & PyPI  
**Milestone (shipped):** v1.4 — Audit gap closure (phases **35–36**; see **`.planning/v1.3-MILESTONE-AUDIT.md`**)  
**Research:** `.planning/research/SUMMARY.md` (2026-03-25)

**Archived:** v1.0 / v1.2 — `.planning/milestones/v1.*-REQUIREMENTS.md`

---

## Milestone v1.4 — Audit gap closure

- [x] **AUDIT-10** — Formal **`28-VERIFICATION.md`** aligned with **28-SUMMARY** / **28-VALIDATION** and **`validate health`**. **Roadmap:** **Phase 35**. **Evidence:** **`.planning/phases/28-v1-3-hybrid-i001-summaries/28-VERIFICATION.md`**, **`35-SUMMARY.md`**.

- [x] **DOC-ALIGN-10** — Root **README** / **CLAUDE** (and related) use **`trading_crab_lib`** imports and correct paths; **34-VALIDATION** / **34-VERIFICATION** refreshed. **Roadmap:** **Phase 36**. **Evidence:** **`.planning/phases/36-v1-4-root-docs-import-alignment/36-SUMMARY.md`**, **`CLAUDE.md`**, **`README.md`**.

---

## 1. GSD & planning hygiene

- [x] **GSD-10** — Hybrid **`*-SUMMARY.md`** for all **I001** plan paths (v1.2 phases **17–22**, **26–27**)  
  Each file: **As-built**, **Plan fidelity**, **Delta from plan**; satisfy **`gsd-tools validate health`**. **Evidence:** `.planning/phases/28-v1-3-hybrid-i001-summaries/28-SUMMARY.md`.

## 2. Submodule analysis & merge blueprint

- [x] **SYNC-10** — Matrix comparing root vs `trading-crab-lib-repo-copy`, `claude-scratch-work-repo-copy`, `trading-crab-repo-copy` (read-only mirrors). **Roadmap:** **Phase 29**. **Evidence:** `.planning/research/SUBMODULE_COMPARISON_MATRIX.md`, **`.planning/phases/29-v1-3-submodule-comparison-matrix/29-SUMMARY.md`**.
- [x] **SYNC-11** — Ordered unification blueprint (lib → claude-scratch → trading-crab) with owner-confirm gates. **Roadmap:** **Phase 30**. **Evidence:** `.planning/research/SUBMODULE_UNIFICATION_BLUEPRINT.md`, **`.planning/phases/30-v1-3-submodule-unification-blueprint/30-SUMMARY.md`**.

## 3. Library packaging & PyPI

- [x] **PKG-10** — Consumer-safe workspace/path API for `pip install` (no implicit repo `ROOT`). **Roadmap:** **Phase 31**. **Evidence:** `src/trading_crab_lib/paths.py`, **`.planning/phases/31-v1-3-library-workspace-paths/31-SUMMARY.md`**, **`tests/unit/test_library_paths.py`**, **`README.md`** (Library-only install).
- [x] **PKG-11** — Release engineering: build, TestPyPI, PyPI, trusted publishing, README install story. **Roadmap:** **Phase 32**. **Evidence:** **`LICENSE`**, **`pyproject.toml`**, **`docs/RELEASING.md`**, **`scripts/build_dist.sh`**, **`README.md`** (Install from PyPI), **`.planning/phases/32-v1-3-pypi-release-engineering/32-SUMMARY.md`**.

## 4. Root prune & narrative docs

- [x] **PRUNE-10** — Remove redundant root notebooks/scratch/duplicate docs (excluding `legacy/`, `*_repo-copy/`). **Roadmap:** **Phase 33**. **Evidence:** **`.planning/phases/33-v1-3-root-prune/33-ROOT-INVENTORY.md`**, **`.planning/phases/33-v1-3-root-prune/33-SUMMARY.md`**.
- [x] **DOCS-10** — Extensive Google-style docstrings + file “why” + major-block rationale under `src/trading_crab_lib/`. **Roadmap:** **Phase 34**. **Evidence:** **`.planning/phases/34-v1-3-library-documentation-pass/34-SUMMARY.md`**, **`34-VERIFICATION.md`**.

---

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| GSD-10 | 28 | Complete |
| SYNC-10 | 29 | Complete |
| SYNC-11 | 30 | Complete |
| PKG-10 | 31 | Complete |
| PKG-11 | 32 | Complete |
| PRUNE-10 | 33 | Complete |
| DOCS-10 | 34 | Complete |
| AUDIT-10 | 35 | Complete |
| DOC-ALIGN-10 | 36 | Complete |

**Milestone v1.3 roadmap scope:** phases **28–34** on **`.planning/ROADMAP.md`** (all v1.3 REQ rows **Complete**).

**Milestone v1.4 gap closure:** phases **35–36** on **`.planning/ROADMAP.md`**.
