---
wave: 1
depends_on: []
requirements:
  - SIGNAL-10
  - SIGNAL-11
  - TACTICS-10
  - MODEL-10
  - MODEL-11
  - EMAIL-10
  - INSTALL-20
files_modified:
  - run_pipeline.py
  - pipelines/07_dashboard.py
  - config/settings.yaml
  - src/trading_crab_lib/prediction/dashboard_model.py
  - scripts/run_weekly_report.py
  - RUNBOOK.md
  - scripts/README.md
  - tests/unit/test_run_pipeline_step_order.py
autonomous: true
gap_closure: true
source_audit: .planning/v1.2-MILESTONE-AUDIT.md
---

# Phase 27 — Pipeline weekly E2E & dashboard model wiring

**Mode:** Gap closure — closes **`gaps.integration`** and **`gaps.flows`** in **`.planning/v1.2-MILESTONE-AUDIT.md`**: (1) step **7** runs before **8/9** in sorted order so `weekly_report.md` misses same-run diagnostics/tactics; (2) **`scripts/run_weekly_report.py`** only runs steps **1–7** / **2–7**; (3) step **7** loads **`current_regime.pkl`** (RF) only while **`current_regime_gb.pkl`** exists when **`prediction.use_boosted: true`**.

---

## Wave 1 — Step execution order + dashboard model selection

<task id="27-01-01">
<title>Reorder pipeline steps so 8 and 9 run before 7 when all are requested</title>
<read_first>
- `run_pipeline.py` — `main()` loop (`for step_num in sorted(requested)`), `STEPS` dict (lines ~1349–1351)
- `.planning/v1.2-MILESTONE-AUDIT.md` — integration `step_7_weekly_report` → `steps_8_9_diagnostics_tactics`
</read_first>
<action>
1. Add a pure function **`resolve_pipeline_step_order(requested: set[int]) -> list[int]`** in **`run_pipeline.py`** (module level, above `main` or below `STEPS`), documented in a 4-line docstring:
   - If **`7 not in requested`** OR **`requested` ∩ `{8, 9}` is empty**: return **`sorted(requested)`** (preserve current behavior).
   - Else: return: sorted steps in `requested` that are less than 7, then 8 (if in set), then 9 (if in set), then 7 (if in set), then sorted steps greater than 9 (future-proof; currently empty).
2. Replace **`for step_num in sorted(requested):`** in **`main()`** with **`for step_num in resolve_pipeline_step_order(requested):`**.
3. Add **`log.info("Step execution order: %s", ...)`** once per run (list or tuple) so operators see reordering in logs.
</action>
<acceptance_criteria>
- `grep -n resolve_pipeline_step_order run_pipeline.py` exits 0.
- With **`requested = {7,8,9}`**, order is **`[8, 9, 7]`** — verify via a unit test (see Wave 2) or `python -c` importing the function.
- With **`requested = {1,2,3,4,5,6,7,8,9}`**, **`7` appears after **`8`** and **`9`** in the resolved list.
- With **`requested = {5,7}`**, order remains **`[5, 7]`** (no 8/9).
</acceptance_criteria>
</task>

<task id="27-01-02">
<title>Shared helper + config: choose RF vs GB for live dashboard regime scoring</title>
<read_first>
- `run_pipeline.py` — `step7_dashboard` (`current_regime.pkl` load ~1111–1118)
- `pipelines/07_dashboard.py` — model load ~90–93
- `config/settings.yaml` — `dashboard:` block (~466+)
</read_first>
<action>
1. Add **`src/trading_crab_lib/prediction/dashboard_model.py`** with:
   - **`def resolve_current_regime_model_path(cfg: dict, model_dir: Path, log: logging.Logger | None = None) -> Path`**
   - Read **`regime_model = cfg.get("dashboard", {}).get("regime_model", "rf")`** — allowed values **`"rf"`** | **`"gb"`** (case-sensitive, lowercase in YAML).
   - If **`regime_model == "gb"`** and **`(model_dir / "current_regime_gb.pkl").exists()`**: return that path.
   - If **`regime_model == "gb"`** but file missing: log **warning** (if log) and fall back to **`current_regime.pkl`**.
   - Otherwise return **`model_dir / "current_regime.pkl"`**.
2. In **`config/settings.yaml`** under **`dashboard:`**, add (with comment):
   ```yaml
   # Live regime for dashboard / weekly report: "rf" (default) or "gb" when current_regime_gb.pkl exists
   regime_model: rf
   ```
3. In **`step7_dashboard`**, replace the hardcoded **`current_regime.pkl`** open with **`path = resolve_current_regime_model_path(cfg, model_dir, log)`** and **`open(path, "rb")`**; log which path was chosen at INFO.
4. In **`pipelines/07_dashboard.py`**, use the same helper + **`load()`** cfg (import **`resolve_current_regime_model_path`** from **`trading_crab_lib.prediction.dashboard_model`**).
</action>
<acceptance_criteria>
- `test -f src/trading_crab_lib/prediction/dashboard_model.py` exits 0.
- `grep -q 'regime_model' config/settings.yaml` exits 0.
- `step7_dashboard` and **`07_dashboard.py`** both import and use **`resolve_current_regime_model_path`** (`grep -n resolve_current_regime_model_path run_pipeline.py pipelines/07_dashboard.py`).
- **`python3 -c "from trading_crab_lib.prediction.dashboard_model import resolve_current_regime_model_path; ..."`** runs without ImportError when **`PYTHONPATH=src`**.
</acceptance_criteria>
</task>

<task id="27-01-03">
<title>Export helper from prediction package (if needed)</title>
<read_first>
- `src/trading_crab_lib/prediction/__init__.py`
</read_first>
<action>
If **`__init__.py`** re-exports public APIs, add **`resolve_current_regime_model_path`** optionally; otherwise rely on **`from trading_crab_lib.prediction.dashboard_model import ...`**. Do not create circular imports.
</action>
<acceptance_criteria>
- `python3 -c "import trading_crab_lib.prediction"` with **`PYTHONPATH=src`** exits 0 after changes.
</acceptance_criteria>
</task>

---

## Wave 2 — Weekly script, docs, tests

<task id="27-02-01">
<title>Extend `scripts/run_weekly_report.py` to run 8–9 before 7</title>
<read_first>
- `scripts/run_weekly_report.py` — `steps =` lines ~77–78
- `run_pipeline.py` — **`resolve_pipeline_step_order`** behavior
</read_first>
<action>
1. Change default step strings:
   - Cached: **`"2,3,4,5,6,8,9,7"`** (not **`2,3,4,5,6,7`**).
   - Full: **`"1,2,3,4,5,6,8,9,7"`** (not **`1,2,3,4,5,6,7`**).
2. Update module docstring top-of-file **Usage** lines to state that **8–9** run before **7** so **`weekly_report.md`** includes Diagnostics + Tactics when configured.
3. **`--help`** description: mention steps **2–9** ending with **7** (wording: “pipeline through tactics/diagnostics, then weekly report”).
</action>
<acceptance_criteria>
- `grep "8,9,7" scripts/run_weekly_report.py` exits 0 (both cached and full variants appear in file).
- `grep "2,3,4,5,6,7" scripts/run_weekly_report.py` exits 1 (old default removed).
</acceptance_criteria>
</task>

<task id="27-02-02">
<title>Document behavior in RUNBOOK + scripts README</title>
<read_first>
- `RUNBOOK.md` — weekly / email / step table sections (search **weekly**, **step 7**, **Diagnostics**)
- `scripts/README.md` — happy path / `run_weekly_report`
</read_first>
<action>
1. **`RUNBOOK.md`:** Add a short subsection (or bullets) stating: (a) full weekly artifact with diagnostics+tactics uses **`--steps`** including **8, 9** before **7**, or relies on **`run_pipeline.py`** auto-ordering when **7+8+9** are together; (b) **`dashboard.regime_model`** chooses RF vs GB for live scoring; (c) **`run_weekly_report.py`** now invokes **8,9** before **7** by default.
2. **`scripts/README.md`:** Mirror the step order and link to **`RUNBOOK.md`**.
</action>
<acceptance_criteria>
- `grep -q '8,9,7\|8.*9.*7' RUNBOOK.md` OR `grep -qi 'diagnostics' RUNBOOK.md` and `grep -qi 'tactics' RUNBOOK.md` after edit (at least one sentence tying weekly report to steps 8/9).
- `grep -q run_weekly_report scripts/README.md` exits 0 (file still documents script).
</acceptance_criteria>
</task>

<task id="27-02-03">
<title>Unit tests: step order + model path resolution</title>
<read_first>
- `tests/unit/test_checkpoints.py` or similar — pytest style
- `pyproject.toml` — pytest `pythonpath`
</read_first>
<action>
Add **`tests/unit/test_run_pipeline_step_order.py`**:
1. Import **`resolve_pipeline_step_order`** from **`run_pipeline`** (or factor it into **`trading_crab_lib.runtime`** only if needed to avoid importing heavy **`run_pipeline`** side effects — prefer importing from **`run_pipeline`** if import is clean).
2. Tests:
   - **`{7,8,9} -> [8,9,7]`**
   - **`{1,2,3,4,5,6,7,8,9}`** — assert indices: **8** and **9** before **7**.
   - **`{5,7} -> [5,7]`**
   - **`{8,9} -> [8,9]`**
3. Tests for **`resolve_current_regime_model_path`**: tmp **`Path`** dir with only **`current_regime.pkl`** → RF path; with both pickles and **`regime_model: gb`** → GB path; **`gb`** but missing file → RF fallback (capture caplog if using pytest **`caplog`**).

If importing **`run_pipeline`** pulls **`matplotlib`** or slow deps, move **`resolve_pipeline_step_order`** to **`trading_crab_lib/pipeline/step_order.py`** (single function) and import from **`run_pipeline`** + tests — **only if** import fails in CI.
</action>
<acceptance_criteria>
- `PYTHONPATH=src python3 -m pytest tests/unit/test_run_pipeline_step_order.py -q` exits 0.
- New file path exists: **`tests/unit/test_run_pipeline_step_order.py`**.
</acceptance_criteria>
</task>

---

## Verification criteria (execute-phase)

- **`pytest`** for new unit tests green; spot-check **`run_pipeline.py --steps 7,8,9`** on a dev machine logs order **8 → 9 → 7** (manual optional).
- **`REQUIREMENTS.md`** traceability: after execution, set **Phase 27** rows **Complete** for SIGNAL/MODEL/TACTICS/EMAIL/INSTALL (separate commit or same PR as executor).

---

## must_haves (goal-backward)

```yaml
must_haves:
  truths:
    - id: T1
      description: "When steps 7+8 and/or 9 are requested together, step 7 runs after 8/9 so weekly_report.md can include diagnostics/tactics outputs from the same invocation."
    - id: T2
      description: "run_weekly_report.py default steps include 8,9 before 7."
    - id: T3
      description: "dashboard.regime_model selects RF vs GB pickle for step 7 and 07_dashboard with documented fallback."
  artifacts:
    - path: run_pipeline.py
    - path: scripts/run_weekly_report.py
    - path: config/settings.yaml
    - path: src/trading_crab_lib/prediction/dashboard_model.py
    - path: RUNBOOK.md
    - path: tests/unit/test_run_pipeline_step_order.py
```

---

## PLANNING COMPLETE

- **Plans:** 1
- **Waves:** 2
- **Mode:** gap_closure
