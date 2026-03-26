## Trading-Crab Roadmap

## Milestones

- ✅ **v1.0 — Core pipeline + planning evidence** — Phases 1–16 (shipped 2026-03-20) — [full roadmap](milestones/v1.0-ROADMAP.md) · [requirements](milestones/v1.0-REQUIREMENTS.md) · [audit](milestones/v1.0-MILESTONE-AUDIT.md)
- ✅ **v1.2 — Tactics, triggers & expanded signals** — Phases 17–27 (shipped 2026-03-24) — [full roadmap](milestones/v1.2-ROADMAP.md) · [requirements](milestones/v1.2-REQUIREMENTS.md) · [audit](milestones/v1.2-MILESTONE-AUDIT.md)
- 🔄 **v1.3 — Consolidation, submodule parity & PyPI** — Research **`.planning/research/`** (2026-03-25). **On this roadmap:** phases **28–34** (milestone backlog fully scoped below; **28–33** = shipped).

## Phases (v1.3 — current)

**Analysts:** Shipped **v1.0** / **v1.2** phase lists remain in **`milestones/v1.0-ROADMAP.md`** and **`milestones/v1.2-ROADMAP.md`**. Active v1.3 work is tracked below for **`gsd-tools roadmap get-phase`**.

- [x] **Phase 28: v1.3 — Hybrid PLAN/SUMMARY closure (I001)** — **GSD-10**
- [x] **Phase 29: v1.3 — Submodule comparison matrix (read-only mirrors)** — **SYNC-10**
- [x] **Phase 30: v1.3 — Submodule unification blueprint (owner gates)** — **SYNC-11**
- [x] **Phase 31: v1.3 — Library workspace & path API (PyPI-safe)** — **PKG-10**
- [x] **Phase 32: v1.3 — PyPI release engineering & publish story** — **PKG-11**
- [x] **Phase 33: v1.3 — Root prune (redundancy removal)** — **PRUNE-10**
- [ ] **Phase 34: v1.3 — Library documentation & rationale pass** — **DOCS-10**

### Phase 28: v1.3 — Hybrid PLAN/SUMMARY closure (I001)

**Goal:** Eliminate **`validate health` I001** gaps for v1.2 product phases by adding **hybrid** `*-SUMMARY.md` files beside each remaining `*-01-PLAN.md`: **as-built** (what shipped in repo), **plan fidelity** (what the plan promised), and a short **delta** section. No submodule edits and no `legacy/` changes.

**Requirements**: GSD-10

**Depends on:** v1.2 shipped (phases 17–27); milestone research in **`.planning/research/SUMMARY.md`**.

**Success criteria:**

1. Eight per-plan summary files exist with basenames matching the I001 list (see Phase 28 CONTEXT).
2. Each summary includes explicitly labeled sections **As-built**, **Plan fidelity**, and **Delta from plan** (or equivalent headings).
3. `node .codex/get-shit-done/bin/gsd-tools.cjs validate health` reports **no I001** for those eight plan paths (or `28-SUMMARY.md` documents an accepted tool false-positive with evidence).
4. **`.planning/REQUIREMENTS.md`** traceability marks **GSD-10** complete with pointer to **`28-SUMMARY.md`**.

### Phase 29: v1.3 — Submodule comparison matrix (read-only mirrors)

**Goal:** Produce a **structured comparison** of the **canonical root** repo vs the three **local read-only** mirrors (`trading-crab-lib-repo-copy`, `claude-scratch-work-repo-copy`, `trading-crab-repo-copy`): layout, public API / package names, features, tests, planning artifacts, and notable deltas — **without** editing files inside `legacy/`, `*_repo-copy/`, or submodule remotes (refresh via `git submodule update` only). Output lives under **`.planning/`** (e.g. research appendix or phase docs) for downstream **SYNC-11** unification ordering.

**Requirements**: SYNC-10

**Depends on:** Phase **28** (GSD-10); milestone research **`.planning/research/FEATURES.md`**, **`.planning/research/ARCHITECTURE.md`**.

**Success criteria:**

1. A single **markdown artifact** (path recorded in phase **29** `*-SUMMARY.md`) contains a **comparison table or equivalent** with one column/section per mirror + canonical root, covering at least: **tree layout** (`src/`, package name), **ingestion / features / prediction / reporting** module presence, **test inventory** (counts or file lists), **config entrypoints**, and **planning** (`.planning` or analog) where applicable.
2. **Merge order** is stated as: **trading-crab-lib mirror first**, then **claude-scratch-work**, then **trading-crab**, with a short **dependency/risk** note per step (may reference **FEATURES.md**).
3. **Explicit “do not edit submodules”** constraint is restated in the artifact (operational guard for executors).
4. **`REQUIREMENTS.md`** traceability row **SYNC-10** can move to **Complete** after execute (deferred until **`$gsd-execute-phase 29`**).

### Phase 30: v1.3 — Submodule unification blueprint (owner gates)

**Goal:** Turn the Phase **29** comparison artifact into an **executable, ordered unification blueprint**: discrete **batches** (e.g. tests, modules, config) to port or reconcile from mirrors into the **canonical root** so the root becomes the **superset**, with **explicit owner-confirmation checkpoints** before any implementation replaces “winning” code. **No** edits inside `legacy/`, `*_repo-copy/`, or submodule working trees except `git submodule update` / refresh.

**Requirements**: SYNC-11

**Depends on:** Phase **29** (**SYNC-10** artifact complete); **`.planning/research/FEATURES.md`** (merge policy, order: lib mirror → claude-scratch → trading-crab).

**Success criteria:**

1. One **markdown blueprint** (path cited in phase **30** `*-SUMMARY.md`) lists **ordered batches** with: objective, **source** (root vs which mirror), **risk**, **deps on prior batch**, and **owner-confirm** gate description per batch.
2. **Winner-selection rule** is documented: prefer **more complete / better-tested** implementation **wherever it lives**, with **human confirmation** before merge-type work in later phases.
3. **Explicit exclusions:** submodules remain read-only for v1.3; downstream **push to mirror remotes** is out of scope for this phase (document as post-milestone).
4. **`REQUIREMENTS.md`** traceability **SYNC-11** → **Complete** only after execute + SUMMARY.

### Phase 31: v1.3 — Library workspace & path API (PyPI-safe)

**Goal:** Remove implicit **checkout-only** assumptions for **`ROOT` / `CONFIG_DIR` / `DATA_DIR` / `OUTPUT_DIR`** in **`trading_crab_lib`** so **`pip install`** consumers can supply **explicit paths** (or env vars) while **editable install** / repo workflows keep a sane default. Align **`pyproject.toml`** / package metadata as needed; add **tests** for at least one “simulated installed” vs repo-root scenario (see **`.planning/research/ARCHITECTURE.md`**).

**Requirements**: PKG-10

**Depends on:** Phase **30** (unification blueprint complete — path and packaging work follow planning freeze for merge batches).

**Success criteria:**

1. Public API (or documented module entrypoints) allow resolving **config** and **data** directories **without** assuming `Path(__file__).parent.parent.parent` is the user project root after install.
2. **`README.md`** or **`docs/`** snippet: **“library-only install”** vs **“full repo checkout”** with copy-pastable examples.
3. **Automated tests** pass in CI for the new resolution logic (`pytest`).
4. **`REQUIREMENTS.md`** **PKG-10** → **Complete** after execute.

### Phase 32: v1.3 — PyPI release engineering & publish story

**Goal:** Make **`trading-crab-lib`** **publishable** as the **single** PyPI distribution from **`src/`**: **`python -m build`**, **TestPyPI** dry run, **README**/`[project.urls]`, **LICENSE** visibility, **classifiers** for **Python 3.10–3.14**, optional **Trusted Publishing** docs (GitHub OIDC) or manual Twine steps — **without** requiring the full app (pipelines/notebooks) in the wheel.

**Requirements**: PKG-11

**Depends on:** Phase **31** (**PKG-10**) — consumer path story stable enough to document “`pip install trading-crab-lib`”.

**Success criteria:**

1. Documented **release checklist** in-repo (e.g. **`docs/`** or **`CONTRIBUTING.md`** / **`RELEASING.md`**) with exact commands: build, upload TestPyPI, upload PyPI.
2. **`pyproject.toml`** reflects **OSS** intent: **urls**, **readme**, **license** file reference; **`requires-python`** policy aligned to **3.10–3.14** (as documented in research).
3. CI or manual steps scripted such that a maintainer can produce **`dist/*.whl`** reproducibly.
4. **`REQUIREMENTS.md`** **PKG-11** → **Complete** after execute (actual PyPI publish may be **manual** first upload — document either way in SUMMARY).

### Phase 33: v1.3 — Root prune (redundancy removal)

**Goal:** **Remove or consolidate** redundant **root-only** assets: duplicate markdown, scratch notebooks/paths, obsolete docs — **never** `legacy/` or `*_repo-copy/` contents. Produce a short **inventory → action** list (delete, merge into canonical doc, or keep with rationale).

**Requirements**: PRUNE-10

**Depends on:** Phase **32** (PyPI story and `pyproject` / `README` stable before deleting or merging root docs).

**Success criteria:**

1. **PR list / table** in phase artifact: each pruned or merged path with **rationale**; **git** history preserves prior content for anything deleted.
2. **`CLAUDE.md` / `RUNBOOK.md` / `ARCHITECTURE.md`** links remain valid or updated in same phase.
3. No deletions under **`legacy/`** or submodule dirs (verify via path allowlist in SUMMARY).
4. **`REQUIREMENTS.md`** **PRUNE-10** → **Complete**.

### Phase 34: v1.3 — Library documentation & rationale pass

**Goal:** Add **Google-style** (or equivalent) **module + public API docstrings** and **file-level “why”** paragraphs across **`src/trading_crab_lib/`**, plus **short rationale** before **major** blocks where it aids humans and AI agents — **without** redundant “what” comments that mirror the code line-by-line.

**Requirements**: DOCS-10

**Depends on:** Phase **33** (prune complete — reduces doc churn). If Phase **33** is waived in CONTEXT (nothing to prune), **Depends on:** Phase **32** instead (document waiver in SUMMARY).

**Success criteria:**

1. **Coverage checklist** in `*-SUMMARY.md`: every **`.py`** under **`src/trading_crab_lib/`** touched or explicitly **waived** (with reason: thin re-export, etc.).
2. **`ruff check`** / **`pytest`** still green (no broken imports from doc-only edits).
3. **Spot-check:** at least **four** modules (`config`, `checkpoints`, `transforms`, `prediction/classifier`) have expanded **module docstrings** per SUMMARY.
4. **`REQUIREMENTS.md`** **DOCS-10** → **Complete**.

---
</think>


<｜tool▁calls▁begin｜><｜tool▁call▁begin｜>
Read
