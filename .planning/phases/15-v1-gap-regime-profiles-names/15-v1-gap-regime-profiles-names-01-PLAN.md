---
phase: 15-v1-gap-regime-profiles-names
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - src/trading_crab_lib/regime.py
  - pipelines/04_regime_label.py
  - config/regime_labels.yaml
  - tests/unit/test_regime_etf_profile_artifact.py
  - .planning/phases/02-regime-clustering-interpretation/02-regime-clustering-interpretation-VERIFICATION.md
  - .planning/REQUIREMENTS.md
  - .planning/phases/15-v1-gap-regime-profiles-names/15-SUMMARY.md
autonomous: true
requirements:
  - REGIME-02
  - REGIME-03
must_haves:
  truths:
    - "REGIME-02 evidence: macro-feature statistics live in data/regimes/profiles.parquet; ETF/proxy return behavior by regime lives in data/regimes/etf_behavior_by_regime.parquet (step 6), and this split is documented in code docs + Phase 2 VERIFICATION."
    - "REGIME-03 evidence: config/regime_labels.yaml pins every balanced_cluster ID for clustering.balanced_k (currently 5 → integer keys 0–4), no stray cluster IDs."
    - "Automated test links build_profiles (macro) and behavior_tables (ETF path) for REGIME-02 regression guard."
    - "02-regime-clustering-interpretation-VERIFICATION.md frontmatter status is passed for roadmap audit (human-only visual truth may remain noted inline without reopening gaps_found)."
  artifacts:
    - path: "src/trading_crab_lib/regime.py"
      provides: "Module docstring subsection listing canonical regime artifact paths"
    - path: "tests/unit/test_regime_etf_profile_artifact.py"
      provides: "pytest coverage for behavior_tables + column contract"
    - path: "config/regime_labels.yaml"
      provides: "Pinned names for clusters 0–4 only"
---

<objective>
Close **Phase 15** gap-closure items from `.planning/v1.0-MILESTONE-AUDIT.md`: satisfy **REGIME-02** and **REGIME-03** with a documented macro-vs-ETF artifact split (no requirement to denormalize ETF stats into `profiles.parquet`), fix `config/regime_labels.yaml` to match **`clustering.balanced_k: 5`** in `config/settings.yaml` (cluster IDs **0–4** only), add a focused unit test, and bring **Phase 2 VERIFICATION** to **`passed`**.
</objective>

<execution_context>
@.planning/phases/15-v1-gap-regime-profiles-names/15-CONTEXT.md
@.planning/v1.0-MILESTONE-AUDIT.md
@.planning/ROADMAP.md
@.planning/REQUIREMENTS.md
@.planning/phases/02-regime-clustering-interpretation/02-regime-clustering-interpretation-VERIFICATION.md
@src/trading_crab_lib/regime.py
@src/trading_crab_lib/asset_returns.py
@pipelines/04_regime_label.py
@pipelines/06_asset_returns.py
@config/regime_labels.yaml
@config/settings.yaml
</execution_context>

<context>
**Decision (locked):** ETF return distributions by regime are **not** merged into `profiles.parquet` (step 4 has no aligned ETF returns). The canonical ETF/regime table is **`data/regimes/etf_behavior_by_regime.parquet`** written by **`pipelines/06_asset_returns.py`** via `behavior_tables()`. Macro profiles remain **`data/regimes/profiles.parquet`** from `build_profiles()`.

**Naming:** `config/settings.yaml` sets `clustering.balanced_k: 5` → canonical cluster IDs **0, 1, 2, 3, 4**. Current `regime_labels.yaml` includes key **5**; that is **invalid** for k=5 and must be removed. Move the string `"Crisis / Deleveraging"` from former key `5` to key **`4`** if cluster 4 is still unnamed, or choose a distinct human label for 4 after reviewing `data/regimes/regime_names_suggested.yaml` when present (if file missing in repo, use `"Crisis / Deleveraging"` for **4** and delete key **5**).
</context>

<tasks>

<task type="auto" tdd="false">
  <name>Task 1 — Document canonical regime artifacts (REGIME-02 split)</name>
  <read_first>
    - src/trading_crab_lib/regime.py
    - pipelines/04_regime_label.py
    - pipelines/06_asset_returns.py
  </read_first>
  <action>
    1. In **`src/trading_crab_lib/regime.py`**, extend the top module docstring (after the existing 3-line summary) with a markdown-style subsection titled **Regime artifacts (macro vs ETF)** containing **exactly these bullet strings**:
       - ``- `data/regimes/profiles.parquet` — per-cluster mean/median/std over **feature columns** (step 4 / `build_profiles`).``
       - ``- `data/regimes/etf_behavior_by_regime.parquet` — per-regime **ETF or proxy return** behavior metrics from `behavior_tables()` (step 6).``
       - ``- `data/regimes/asset_return_profile.parquet` — intermediate wide profile from `returns_by_regime()` (step 6); optional for diagnostics.``
    2. In **`pipelines/04_regime_label.py`**, in the top docstring “Writes …” list, append one line: ``  (ETF/proxy return statistics by regime → data/regimes/etf_behavior_by_regime.parquet from step 6.)``
  </action>
  <acceptance_criteria>
    - `grep -n "etf_behavior_by_regime.parquet" src/trading_crab_lib/regime.py` returns at least one match.
    - `grep -n "etf_behavior_by_regime.parquet" pipelines/04_regime_label.py` returns at least one match.
    - `grep -n "profiles.parquet" src/trading_crab_lib/regime.py` returns at least one match in the new artifact subsection.
  </acceptance_criteria>
</task>

<task type="auto" tdd="true">
  <name>Task 2 — Unit test: behavior_tables column contract (REGIME-02)</name>
  <read_first>
    - src/trading_crab_lib/asset_returns.py
    - tests/unit/test_regime.py
  </read_first>
  <action>
    Create **`tests/unit/test_regime_etf_profile_artifact.py`** with:
    - A synthetic quarterly `DatetimeIndex` or `PeriodIndex` shared by a small `returns` DataFrame (2 ETF columns, 12 rows) and a `cluster_labels` Series with values in `{0, 1}`.
    - Call `behavior_tables(returns, cluster_labels)` imported from `trading_crab_lib.asset_returns`.
    - Assert the result is non-empty and contains **all** of these column names (exact strings): `regime`, `asset`, `median_return`, `q25`, `q75`, `hit_rate`, `n_quarters`, `signal_absolute`, `tertile`, `signal_display`, `score_relative`, `score_absolute`, `rank`.
    - Module docstring must contain the literal substring **REGIME-02** and **etf_behavior_by_regime.parquet**.
  </action>
  <acceptance_criteria>
    - `pytest tests/unit/test_regime_etf_profile_artifact.py -q` exits **0**.
    - `grep -n "REGIME-02" tests/unit/test_regime_etf_profile_artifact.py` returns at least one match.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 3 — Pin regime_labels.yaml for balanced_k=5 (REGIME-03)</name>
  <read_first>
    - config/regime_labels.yaml
    - config/settings.yaml (only the `balanced_k` line under `clustering:`)
    - src/trading_crab_lib/regime.py (`load_name_overrides`)
  </read_first>
  <action>
    Edit **`config/regime_labels.yaml`** so that:
    1. Active mappings cover **exactly** integer cluster IDs **0, 1, 2, 3, 4** (YAML keys **0–4**), each a non-empty quoted human-readable string.
    2. Remove the **`5:`** key entirely (invalid for `balanced_k: 5`).
    3. If cluster **4** lacks a name after removal of `5:`, set **`4: "Crisis / Deleveraging"`** (reuse the old `5` label) unless `data/regimes/regime_names_suggested.yaml` exists in the workspace and contains a clearly better string for `4` — if that file exists, prefer the suggested name for `4` from its contents.
    4. Replace the old multi-line `## 4 and other IDs…` / `## 5` comment block with a single-line comment: `# Pinned for balanced_cluster IDs 0..4 (clustering.balanced_k=5 in config/settings.yaml).`
  </action>
  <acceptance_criteria>
    - `grep -n "^5:" config/regime_labels.yaml` returns **no** matches.
    - `grep -n "^4:" config/regime_labels.yaml` returns **at least one** match.
    - `python -c "import yaml; from pathlib import Path; r=yaml.safe_load(Path('config/regime_labels.yaml').read_text()); assert r and set(r.keys())=={0,1,2,3,4}"` exits **0**.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 4 — Phase 2 VERIFICATION + REQUIREMENTS closure</name>
  <read_first>
    - .planning/phases/02-regime-clustering-interpretation/02-regime-clustering-interpretation-VERIFICATION.md
    - .planning/REQUIREMENTS.md (Traceability rows for REGIME-02/03)
  </read_first>
  <action>
    1. Update **`.planning/phases/02-regime-clustering-interpretation/02-regime-clustering-interpretation-VERIFICATION.md`**:
       - Set YAML frontmatter **`status: passed`** and **`score:`** reflecting 6/6 automated truths **or** keep a single **`human_needed`** entry only under a "Residual (manual)" prose section **without** using frontmatter `gaps_found`.
       - Remove or rewrite frontmatter **`gaps:`** list: either delete the entire `gaps:` key from frontmatter **or** set it to YAML empty list `gaps: []` so the file no longer claims open product gaps for ETF artifact / yaml pins.
       - In the body **Observable Truths** table, set row 4 (macro + ETF profile) to **✓ VERIFIED** with evidence text stating **`profiles.parquet` = macro**, **`etf_behavior_by_regime.parquet` = ETF/proxy behavior (step 6), citing `src/trading_crab_lib/regime.py` docstring.
       - Set row 5 (pinned names) to **✓ VERIFIED** citing `config/regime_labels.yaml` keys 0–4.
       - Update **Requirements Coverage** table: REGIME-02 and REGIME-03 rows **PASS** with evidence pointers to the new test file and yaml.
    2. Update **`.planning/REQUIREMENTS.md`** traceability: **REGIME-02** and **REGIME-03** → **Phase 15** (or **Phase 2** if you prefer original phase ownership — use **Phase 15** for gap-closure traceability) and **`Status`** column **Complete** for both rows.
    3. Append **`.planning/phases/15-v1-gap-regime-profiles-names/15-SUMMARY.md`** (≥15 substantive lines) listing files touched, pytest command run, and any manual follow-up for regime **visual** inspection (notebooks).
  </action>
  <acceptance_criteria>
    - `grep -n "^status: passed" .planning/phases/02-regime-clustering-interpretation/02-regime-clustering-interpretation-VERIFICATION.md` matches the frontmatter line **status: passed** (line 4 area).
    - `grep "REGIME-02" .planning/REQUIREMENTS.md | grep Complete` returns at least one line.
    - `grep "REGIME-03" .planning/REQUIREMENTS.md | grep Complete` returns at least one line.
    - `wc -l .planning/phases/15-v1-gap-regime-profiles-names/15-SUMMARY.md` first column is ≥ **15**.
  </acceptance_criteria>
</task>

</tasks>

<verification>
- `pytest tests/unit/test_regime_etf_profile_artifact.py tests/unit/test_regime.py -q` exits 0.
- `python -c "import yaml; from pathlib import Path; r=yaml.safe_load(Path('config/regime_labels.yaml').read_text()); assert set(r.keys())=={0,1,2,3,4}"` exits 0.
</verification>

<success_criteria>
- REGIME-02 and REGIME-03 are **Complete** in REQUIREMENTS with cited artifacts and tests.
- Phase 2 VERIFICATION is **passed**; v1.0 re-audit can treat requirement gaps as closed for names + ETF profile evidence.
</success_criteria>
