# Features Research — v1.3 (superset + submodule parity)

**Researched:** 2026-03-25  
**Confidence:** MEDIUM until submodule trees are refreshed and line-level diff is executed

## Milestone intent (from stakeholder)

1. Close **GSD planning hygiene**: hybrid **PLAN + SUMMARY** for all **I001** gaps (as-built + plan fidelity + delta).
2. **Compare** canonical root (`src/trading_crab_lib/`, pipelines, tests) vs **three read-only mirrors**:
   - `trading-crab-lib-repo-copy`
   - `claude-scratch-work-repo-copy`
   - `trading-crab-repo-copy`
3. **Unify one submodule at a time** into root (root becomes **superset**); submodule repos updated **later**, not in v1.3.
4. **PyPI:** publish **`trading-crab-lib`** from `src/` only (see STACK.md).
5. **Prune** redundancy (notebooks, scratch, duplicate docs) — **exclude** `legacy/` and `*_repo-copy/`.
6. **Documentation density:** extensive module + internal comments (see PITFALLS.md for style).

**Shipped scope confirmation:** No additional “not shipped” phases beyond health **I001** list; other gaps → future milestones.

## Peer codebase inventory (local only)

| Mirror | Role | v1.3 edits |
|--------|------|------------|
| `trading-crab-lib-repo-copy` | Standalone library sibling | Read-only; refresh via git |
| `claude-scratch-work-repo-copy` | Scratch / broader experiments | Read-only |
| `trading-crab-repo-copy` | App-style / pipeline sibling | Read-only |

**Note:** At least one mirror path shows **nested** `gsd-scratch-work-repo-copy/` inside another submodule — treat as **layout noise** from history; normalization is out of scope for v1.3 inside mirrors.

## Unification order (locked + refinement)

1. **Primary order (stakeholder):** `trading-crab-lib` → `claude-scratch-work` → `trading-crab`.
2. **Then:** Research/proposals refine **dependency and risk** within each step (e.g. merge low-risk pure functions before IO-heavy ingest).

## Comparison dimensions (use as matrix per repo)

For each mirror, tabulate:

| Dimension | Questions |
|-----------|-----------|
| **Package layout** | `src/` package name, `__init__` exports, lazy imports |
| **Public API** | Functions/classes documented vs actually exported |
| **Data + config** | Paths to `config/`, `DATA_DIR`, env vars — portability |
| **Tests** | Coverage overlap; tests only in mirror → candidate to port |
| **Features** | Diagnostics, tactics, email, providers, clustering extras |
| **Docs / notebooks** | Duplicate HOWTO — consolidate into root or delete |
| **Planning** | `.planning/` or equivalent — informational only for merge |

## Merge policy (stakeholder)

- When implementations diverge, prefer **more complete / better-tested** implementation **regardless of repo**.
- **Human confirmation** required before choosing winner — record decision in phase **CONTEXT.md** or REQ trace.

## “Superset” definition

Root should implement **union** of valuable capabilities across peers, with:

- Single authoritative implementation per concern (no forked logic).
- Tests proving parity or superiority vs dropped variant.
- Clear **deprecation** comments if API is transitional (v1.3 allows breakage but public OSS benefits from **CHANGELOG** entries).

## Planning artifact repair (I001)

**Hybrid SUMMARY** for each missing file must:

1. **As-built:** What exists in repo today tied to that plan’s intent.
2. **Plan fidelity:** What the PLAN promised.
3. **Delta:** Short explicit gap list (done / partial / superseded).

No code ship requirement beyond documentation closure for these plans unless delta exposes a product bug (then new phase).

## Table stakes vs defer

| Table stakes (v1.3) | Defer |
|---------------------|-------|
| Comparative matrix + ordered merge plan | Pushing commits to submodule remotes |
| PyPI-ready library layout | Full narrative docs site (optional later) |
| Prune redundant root docs/notebooks | Editing nested submodule files |
