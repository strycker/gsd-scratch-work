# Incremental migration to the master `trading-crab` repo — human-driven playbook

**Goal:** Move **validated, working** pieces from this workspace (**`gsd-scratch-work`**, with **`trading_crab_lib`** + `run_pipeline.py` + notebooks) into the **master public-facing repository** tracked as submodule **`trading-crab-repo-copy`** (`https://github.com/strycker/trading-crab`), **slowly**, with **human verification at every wave**.

**Non-goals:** Automated bulk sync without review; editing submodules **inside** this scratch repo as the source of truth for the migration (you work in **clones of the real remotes** for commits that land upstream).

**Assumed preconditions (you said you will reach these first):**

- Codebases are **synchronized** where you intend them to be (see `.planning/SUBMODULE-CLAUDE-SCRATCH-SYNC-GUIDE.md` for `claude-scratch-work-repo-copy` alignment).
- **`trading_crab_lib`** is **PyPI-robust**: `pip install trading-crab-lib` (or editable install) works; `import trading_crab_lib as crab` resolves; `paths.py` / `TRADING_CRAB_*` env vars documented (`README`, `CLAUDE.md`, phase 31 work).
- **`python run_pipeline.py --steps …`** runs end-to-end on a **known machine** with cached data.
- **Notebooks** in this repo exercise steps thoroughly (ingestion → dashboard).

This document is the **human-operating procedure** for migrating that reality into **`trading-crab`** without breaking the story users see on GitHub.

---

## 1. Understand the three-repository roles

| Repository | Typical role | Today’s reality (observed) |
|----------|--------------|----------------------------|
| **`gsd-scratch-work`** (this workspace) | Integration, GSD planning, experiments, submodules as mirrors | **Canonical dev tree**: `src/trading_crab_lib`, `pipelines/`, `run_pipeline.py`, `config/`, `tests/`, `notebooks/`. |
| **`trading-crab-lib`** (submodule `trading-crab-lib-repo-copy`) | **Publishable library** — importable package, versioned, PyPI | Smaller checkout; should track **the same package** as `gsd-scratch-work` after you promote releases. |
| **`trading-crab`** (submodule `trading-crab-repo-copy`) | **Master “product” repo** — README, demos, notebooks, maybe thin app wrapper | README still describes an **older** `src/python` / `trading_crab.pipeline` layout; **no** modern `pyproject` package tree at root in the sparse tree we see — treat as **documentation + assets + placeholder** until migration waves land. |

**Implication:** Migration is not “copy `gsd-scratch-work` into `trading-crab` wholesale.” It is **layering**: (1) depend on **`trading_crab_lib`** as a package, (2) add **runner + config + docs** that match the current pipeline, (3) **replace** obsolete README structure with truth, (4) optionally slim **`trading-crab`** to “consumer + notebooks only” if you want a clean separation.

---

## 2. Principles (carry over from project docs)

From **`CLAUDE.md`**, **`ARCHITECTURE.md`**, **`RUNBOOK.md`**, **`.planning/REBUILD-FROM-SCRATCH-GUIDE.md`**:

1. **Never silently change** `clustering_features` / PCA / labels — migration steps that touch **config** require a **re-run plan** and explicit **`regime_labels.yaml`** review.
2. **Causal vs centered features** — any notebook or script in **`trading-crab`** must use the **same** checkpoints as the library docs (`features_supervised` for supervised, etc.).
3. **Submodules are read-only** **here**; **commits** for `trading-crab` and `trading-crab-lib` happen in **dedicated clones** (see §4).
4. **One version story** — PyPI version of `trading-crab-lib` should match what **`trading-crab`** pins in `requirements.txt` / `pyproject.toml`.

---

## 3. Suggested migration waves (ordered, prioritized)

Each **wave** is a **mergeable unit** (PR-sized). **Stop** after any wave if validation fails.

| Wave | Name | Outcome | Human “done” signal |
|------|------|---------|----------------------|
| **W0** | Target repo hygiene | Branch, issue, checklist | You can build a clean branch on `trading-crab` remote |
| **W1** | Declare dependency on `trading_crab_lib` | Install instructions + pinned version | `pip install` / venv imports `trading_crab_lib as crab` on a fresh machine |
| **W2** | Add **runner surface** | `run_pipeline.py` + `pipelines/` **or** thin wrapper calling installed package | Same CLI semantics as scratch (documented delta list) |
| **W3** | Config & data contract | `config/`, `.env.example`, `data/` / `outputs/` gitignore | `TRADING_CRAB_ROOT` (or equivalent) documented; paths resolve |
| **W4** | Notebooks & narrative | Port / link notebooks; update README “Usage” | Each notebook runs against **pinned** lib version |
| **W5** | CI & release wiring | GitHub Actions: lint + pytest (lib) or smoke | Green CI on default branch |
| **W6** | Deprecate legacy README claims | Remove `python -m trading_crab.pipeline` if obsolete | README matches actual entrypoints only |
| **W7** | Optional: repo split clarity | `trading-crab` = docs + demos only; code only in `trading-crab-lib` | Single source of truth documented |

**Do not skip W1–W3** to “just copy notebooks” — you will get path drift and import hell.

---

## 4. Where you physically work (important)

| Action | Where |
|--------|--------|
| **Draft migration steps, checklists** | This repo’s `.planning/` (you’re reading it) |
| **Commits to `strycker/trading-crab`** | **Clone** `trading-crab` **outside** scratch submodules; `git push` from there |
| **Commits to `strycker/trading-crab-lib`** | **Clone** `trading-crab-lib` separately; release tags for PyPI |
| **Update submodule pointers in scratch** | After upstream merges, `git submodule update --remote` in `gsd-scratch-work` |

**Why:** Submodule directories inside scratch are easy to commit to by mistake; the playbook assumes **upstream PRs** are the system of record.

---

## 5. Wave-by-wave manual procedure

### W0 — Target repo hygiene (no library code yet)

**You do:**

1. Clone **`trading-crab`** to a clean directory (not inside submodule copy if you can avoid it).
2. Create branch `migration/w0-baseline`.
3. Open an issue: “Migrate to `trading_crab_lib` + modern pipeline.”
4. In README, add a **banner**: “Repository structure is being migrated; see issue #N.”
5. Commit if you only add the banner + issue link.

**Validate:**

- [ ] Default branch policy known (who approves PRs).
- [ ] `LICENSE` / `README` license section matches `trading-crab-lib` (MIT).

**Stop if:** You cannot create branches (permissions).

---

### W1 — Depend on `trading_crab_lib` (published or Git URL)

**You do:**

1. Choose **version pin**: e.g. `trading-crab-lib==0.1.0` from PyPI **or**  
   `trading-crab-lib @ git+https://github.com/strycker/trading-crab-lib@v0.1.0` until PyPI is stable.
2. Add **`pyproject.toml`** or update **`requirements.txt`** in **`trading-crab`** to install **only** the library + its deps (not duplicate numpy/pandas pins blindly — follow lib’s `pyproject`).
3. Document in README:

   ```text
   pip install "trading-crab-lib[dev]"   # or minimal install
   python -c "import trading_crab_lib as crab; print(crab.ROOT)"
   ```

4. Set **`TRADING_CRAB_ROOT`** (or full granular vars per `paths.py`) to point **this repo root** when running from a checkout.

**Validate (human):**

- [ ] Fresh venv: install succeeds.
- [ ] `import trading_crab_lib as crab` works.
- [ ] `resolve_library_paths()` or `ROOT` points to **`trading-crab` repo root** when env set — **print and eyeball** paths.

**Stop if:** Import fails — fix **lib** release first, not the consumer repo.

---

### W2 — Runner surface (`run_pipeline` + `pipelines`)

**You do:**

1. **Copy** from **`gsd-scratch-work`** (or released **trading-crab-lib** sdist if you bundle pipelines there — today pipelines often live **next to** the lib in scratch):  
   - `run_pipeline.py`  
   - `pipelines/*.py`
2. **Prefer** copying from **the same commit** you pinned in W1.
3. Adjust **only**:
   - shebang / `sys.path` hacks — remove `sys.path.insert` if package is properly installed;
   - relative imports should resolve to **`trading_crab_lib`**.
4. Add **`[project.scripts]`** optional entry point later — not required for W2.

**Validate:**

- [ ] `python run_pipeline.py --steps 1` (or your minimal step) with **test data** or **cached** `data/checkpoints` copied under `trading-crab` tree.
- [ ] Compare stdout **line-by-line** with scratch run on **same config hash** (rough parity).

**Critique gate:** If **`run_pipeline.py`** in scratch is **much longer** than in lib-only repo, maintain **one** canonical copy — usually **scratch** until you cut a release that includes pipelines **inside** `trading-crab-lib` package data (optional future).

**Stop if:** Steps fail on paths — revisit W1 env vars; read **`paths.py`** docstring.

---

### W3 — Config, `.env`, directories

**You do:**

1. Copy **`config/settings.yaml`**, **`config/regime_labels.yaml`** (template), **`.env.example`** from scratch.
2. Ensure **`.gitignore`** includes `data/`, `outputs/`, `.env`, `__pycache__/`.
3. Document **FRED_API_KEY** and any optional keys.
4. Run **`scripts/setup.sh`** equivalent if you use one — or write a **minimal** `Makefile` target `make data-dirs`.

**Validate:**

- [ ] `python -c "from trading_crab_lib.config import load; print(load()['data']['start_date'])"` works from **`trading-crab` root**.
- [ ] No secrets in git (`git grep FRED_API_KEY` empty).

---

### W4 — Notebooks & human “step verification”

**You do:**

1. Copy **`notebooks/*.ipynb`** incrementally — **one notebook per PR** if possible.
2. At top of each notebook, add a **metadata cell**: `trading-crab-lib` version, git SHA of `trading-crab`, date.
3. For each notebook:
   - Run **Kernel → Restart & Run All** on a machine with data.
   - Record **expected runtime** and **required checkpoints** in a `notebooks/README.md`.

**Validate (explicit checklist per notebook):**

| Notebook | Validates | Sign-off |
|----------|-----------|----------|
| 01 ingestion | Raw + completeness | [ ] |
| 02 features | Dual features / NaNs | [ ] |
| 03 clustering | PCA + clusters | [ ] |
| … | … | [ ] |

**Stop if:** A notebook **only** works with **scratch-only** paths — fix to use **`ROOT`** from env.

---

### W5 — CI

**You do:**

1. Add **`.github/workflows/ci.yml`**: Python matrix, `pip install -e ".[dev]"` or install lib + dev deps, `pytest` **for tests you ship** in `trading-crab` (may be empty initially — then smoke `import trading_crab_lib`).
2. Optionally **reuse** workflows from **`trading-crab-lib`** via reusable workflow — only if you’re comfortable coupling repos.

**Validate:**

- [ ] CI green on PR.
- [ ] CI does **not** hit FRED (no network) — mock or skip integration.

---

### W6 — README truth pass

**You do:**

1. Delete or strike through old **`python -m trading_crab.pipeline`** instructions if that package **does not exist** in **`trading-crab`** anymore.
2. Replace “Repository Structure” section with **actual** tree (or link to **`trading-crab-lib`** for code structure).
3. Move long “Concepts” narrative to **`docs/`** if README exceeds ~200 lines.

**Validate:**

- [ ] New user can follow README **only** and get a successful **`run_pipeline.py`** dry run or documented cache path.

---

### W7 — Optional split clarity

**You do:**

1. Decide: **`trading-crab`** contains **no** `src/trading_crab_lib` source — only depends on PyPI.
2. Add **Contributing** section: “Library code → `trading-crab-lib` repo.”

**Validate:**

- [ ] No duplicated `transforms.py` in two repos.

---

## 6. Human validation rituals (every wave)

Use a **paper or Markdown log** in **`trading-crab`** (e.g. `docs/MIGRATION-LOG.md`):

1. **Date / author**
2. **Wave ID**
3. **Git SHA** (scratch reference + `trading-crab` + `trading-crab-lib`)
4. **Commands run** (copy-paste)
5. **Pass/fail** + screenshots or log snippets for plots if relevant
6. **Follow-ups** (open issues)

**Minimum bar:** Two people **or** two sessions on different machines for W1–W2 (import + pipeline) to catch path issues.

---

## 7. Rollback strategy

| Failure | Action |
|---------|--------|
| Bad release on PyPI | Pin previous version in `trading-crab`; yank if needed |
| Broken `run_pipeline` merge | Revert PR; keep W1 import-only README |
| Notebook red herring | Isolate: run same step via CLI only |
| Config drift | Restore `settings.yaml` from tagged commit |

Tag **`trading-crab`** releases **`vYYYY.MM.0`** that **pin** **`trading-crab-lib`** max version.

---

## 8. Alignment with existing planning artifacts

| Document | Use during migration |
|----------|----------------------|
| **`RUNBOOK.md`** (scratch) | Golden-path commands to reproduce before/after |
| **`ARCHITECTURE.md`** | Invariants to not break when copying configs |
| **`.planning/SUBMODULE-CLAUDE-SCRATCH-SYNC-GUIDE.md`** | If scratch still pulls from `claude-scratch-work`, finish alignment **before** declaring “frozen” migration source |
| **`.planning/REBUILD-FROM-SCRATCH-GUIDE.md`** | Order of pipeline concerns — use as review checklist |
| **Phase 31 / PKG-10** | Path resolution — must match what you document in **`trading-crab` README** |

---

## 9. Open decisions (fill before W2)

Record answers in **`trading-crab`** issue or `docs/DECISIONS.md`:

1. Will **`pipelines/`** live **only** in **`trading-crab`** or be **packaged inside** `trading-crab-lib` for `python -m` style?
2. Will **`trading-crab`** ship **tests** or only consume **lib** tests?
3. Will **`data/`** in **`trading-crab`** be empty + download script, or **document-only**?

---

## 10. One-page cheat sheet

1. **Freeze** a **lib** version on PyPI (or git tag).  
2. **Clone** `trading-crab` separately — **branch**.  
3. **W1:** Add dependency — **verify import**.  
4. **W2:** Add `run_pipeline` + `pipelines` — **verify step 1–2**.  
5. **W3:** Config + env — **verify `load()`**.  
6. **W4:** Notebooks one-by-one — **restart & run all**.  
7. **W5:** CI.  
8. **W6:** README truth.  
9. **Submodule in scratch:** update pointer when happy.

---

*This playbook is procedural. When `trading-crab` repo gains a real `pyproject.toml` and package layout, update §2 and §6 to match reality.*
