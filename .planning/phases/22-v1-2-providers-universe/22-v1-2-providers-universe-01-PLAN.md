---
phase: 22-v1-2-providers-universe
plan: 01
type: execute
wave: 1
depends_on:
  - 21-v1-2-email-and-install
files_modified:
  - config/settings.yaml
  - src/trading_crab_lib/ingestion/assets.py
  - RUNBOOK.md
  - tests/unit/test_assets_providers.py
  - .planning/REQUIREMENTS.md
  - .planning/phases/22-v1-2-providers-universe/22-SUMMARY.md
autonomous: true
requirements:
  - DATA-11
user_setup:
  - None for unit tests; optional pip extras: pip install "trading-crab-lib[data-extras]" for live stooq/OpenBB
must_haves:
  truths:
    - "settings.yaml documents the ETF universe and adds explicit provider toggles (yfinance / stooq / OpenBB) with safe defaults matching current behavior."
    - "assets.fetch_all respects toggles: disabled providers are not invoked; ImportError or missing keys never crash the pipeline."
    - "When yfinance returns only partial tickers, stooq (if enabled) is tried for remaining tickers before falling back to OpenBB-only when the matrix would otherwise be empty."
    - "Automated tests cover provider toggles and a stable ingestion contract (wide quarterly DataFrame, index name date) using mocks — no network in CI."
    - "RUNBOOK or assets module docstring notes that Finviz is not a historical price provider for this use case."
  artifacts:
    - path: "config/settings.yaml"
      provides: "assets.etfs + provider flags"
    - path: "src/trading_crab_lib/ingestion/assets.py"
      provides: "config-driven fetch chain + per-ticker stooq"
    - path: "tests/unit/test_assets_providers.py"
      provides: "regression / contract tests"
---

<objective>
Close **DATA-11** for v1.2: **config-driven** optional price providers (yfinance / stooq / OpenBB), **documented** ETF universe, **stronger stooq** use on partial yfinance failure, and **regression tests** for ingestion contracts — while preserving **`asset_prices`** checkpoint shape expectations.
</objective>

**Non-goals:** New paid data vendors with required keys (beyond wiring patterns); macrotrends; changing FRED/multpl ingestion; portfolio template math.

<execution_context>
@.planning/phases/22-v1-2-providers-universe/22-CONTEXT.md
@.planning/REQUIREMENTS.md
@.planning/ROADMAP.md
@config/settings.yaml
@src/trading_crab_lib/ingestion/assets.py
@src/trading_crab_lib/checkpoints.py
@tests/unit/test_end_date_null_fallback.py
</execution_context>

<context>
**Regression guard after each task:**  
`PYTHONPATH=src python -m pytest tests/unit/test_assets_providers.py tests/unit/test_end_date_null_fallback.py -q`

**Optional full slice:**  
`PYTHONPATH=src python -m pytest tests/test_pipelines_ingest_features.py -q` (if touched)
</context>

<tasks>

<task type="auto" tdd="false">
  <name>Task 1 — settings.yaml: provider toggles + ETF documentation</name>
  <read_first>
    - config/settings.yaml (`assets:` block)
    - 22-CONTEXT.md
  </read_first>
  <action>
    1. Under `assets:`, add a **`providers`** subsection with booleans, defaults **all true**, matching today’s effective behavior:
       - e.g. `yfinance: true`, `stooq: true`, `openbb: true`
    2. Add a short **comment block** above `etfs:` describing that this list drives both ingestion and downstream returns/dashboards; note that adding/removing tickers changes expected `asset_prices` columns and may require refresh.
    3. Keep existing `portfolio_templates` unchanged unless a renamed ticker forces a fix (should not if templates only reference current symbols).
  </action>
  <acceptance_criteria>
    - `python -c "from trading_crab_lib.config import load; c=load(); assert 'providers' in c.get('assets',{})"` passes.
    - YAML remains valid; `assets.etfs` is still a list of tickers.
  </acceptance_criteria>
</task>

<task type="auto" tdd="true">
  <name>Task 2 — assets.py: respect toggles + per-ticker stooq for misses</name>
  <read_first>
    - src/trading_crab_lib/ingestion/assets.py (full file)
  </read_first>
  <action>
    1. Load provider flags from `cfg["assets"]` with defaults **True** for backward compatibility.
    2. If **yfinance disabled**, skip phases 1–2 (log info) and proceed to enabled fallbacks in configured order.
    3. If **stooq disabled**, skip all stooq calls.
    4. If **openbb disabled**, skip OpenBB.
    5. **Partial-fill path:** After phase 2, compute `still_missing`. If stooq enabled and `still_missing` non-empty, call stooq **per ticker** for those symbols and merge into `results` (even when phase 1 returned some tickers). Only if **no** prices were obtained at all, keep existing “bulk stooq” behavior as an alternative path or collapse to per-ticker only — avoid duplicate work; prefer one clear strategy in code comments.
    6. Preserve quarterly `QE` resample, column naming, and empty-DataFrame return when everything fails.
  </action>
  <acceptance_criteria>
    - `python -m compileall -q src/trading_crab_lib/ingestion/assets.py`
    - New unit tests demonstrate toggles and per-ticker stooq path (mocked).
  </acceptance_criteria>
</task>

<task type="auto" tdd="true">
  <name>Task 3 — tests/unit/test_assets_providers.py</name>
  <read_first>
    - tests/unit/test_end_date_null_fallback.py (mock patterns)
    - tests/conftest.py
  </read_first>
  <action>
    1. **Toggle test:** With mocks, assert that when `stooq` is false, `_fetch_ticker_stooq` / `_fetch_tickers_stooq` are never called (patch at module level).
    2. **Contract test:** With `fetch_all` fully mocked to return a small DataFrame, assert `index.name == "date"` and columns ⊆ configured tickers.
    3. **Partial missing test:** Mock batch yfinance to return one ticker only; mock stooq to return the second; assert final DataFrame has both columns when providers enabled.
    4. Keep tests **network-free**.
  </action>
  <acceptance_criteria>
    - `PYTHONPATH=src python -m pytest tests/unit/test_assets_providers.py -q` passes.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 4 — Docs: RUNBOOK + Finviz note</name>
  <read_first>
    - RUNBOOK.md (ingestion / assets section if present)
  </read_first>
  <action>
    1. Add a short **“Asset prices & providers (DATA-11)”** bullet: where toggles live in `settings.yaml`, optional `pip install` extras for stooq/OpenBB, and that checkpoints may need `--refresh` after ticker changes.
    2. One sentence: **Finviz** is not used for historical ETF OHLCV here (aligns with module docstring).
  </action>
  <acceptance_criteria>
    - Grep finds `DATA-11` or `providers` in RUNBOOK.md.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 5 — Traceability + summary</name>
  <read_first>
    - .planning/REQUIREMENTS.md (DATA-11 line)
  </read_first>
  <action>
    1. Update **REQUIREMENTS.md**: mark **DATA-11** completed with pointer to phase 22 / `22-SUMMARY.md`.
    2. Write **22-SUMMARY.md** (execution summary template: what shipped, verification commands).
    3. Update **22-VALIDATION.md** statuses if present.
  </action>
  <acceptance_criteria>
    - REQUIREMENTS reflects closure; `22-SUMMARY.md` exists post-execute (create stub only if executing later — for planning, note in checklist).
  </acceptance_criteria>
</task>

</tasks>

## Verification checklist (pre-merge)

- [ ] `PYTHONPATH=src python -m pytest tests/unit/test_assets_providers.py tests/unit/test_end_date_null_fallback.py -q`
- [ ] `python -m compileall -q src/trading_crab_lib/ingestion/assets.py`
- [ ] Manual (optional): `python run_pipeline.py --steps 1` with small ETF subset in a scratch config — not required for CI

## Plan metadata

| Field | Value |
|-------|-------|
| Roadmap | Phase 22 — Providers & ETF universe |
| Nyquist | Add/update `22-VALIDATION.md` after implementation |
