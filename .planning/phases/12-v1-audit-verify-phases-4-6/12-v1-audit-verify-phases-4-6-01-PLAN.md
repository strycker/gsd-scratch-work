---
phase: 12-v1-audit-verify-phases-4-6
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - run_pipeline.py
  - .planning/phases/04-regime-conditional-etf-portfolio-behavior/04-regime-conditional-etf-portfolio-behavior-VERIFICATION.md
  - .planning/phases/05-recommendations-machine-readable-outputs/05-recommendations-machine-readable-outputs-VERIFICATION.md
  - .planning/phases/06-weekly-report-pipeline/06-weekly-report-pipeline-VERIFICATION.md
  - .planning/REQUIREMENTS.md
  - .planning/ROADMAP.md
  - .planning/phases/12-v1-audit-verify-phases-4-6/12-VALIDATION.md
  - .planning/phases/12-v1-audit-verify-phases-4-6/12-SUMMARY.md
autonomous: true
requirements:
  - PORT-01
  - PORT-02
  - PORT-03
  - UX-01
  - UX-02
  - UX-03
  - REPORT-01
  - REPORT-02
user_setup: []
must_haves:
  truths:
    - "Phase directories 04–06 each contain a single canonical *-VERIFICATION.md tying roadmap requirements to code paths, artifacts, and (where they exist) automated tests."
    - "Each verification report states passed or gaps_found with explicit evidence; any implementation gap (e.g. step 6 parity) is called out rather than silently ignored."
    - ".planning/REQUIREMENTS.md traceability rows for PORT-01..03, UX-01..03, REPORT-01..02 are set to Complete only when verification supports them; otherwise remain Pending with a pointer to gaps_found."
    - "12-VALIDATION.md exists with Nyquist-style verification map for this gap-closure phase (Wave 0: planning docs + optional pytest smoke for returns/reporting if extended)."
  artifacts:
    - path: ".planning/phases/04-regime-conditional-etf-portfolio-behavior/04-regime-conditional-etf-portfolio-behavior-VERIFICATION.md"
      provides: "Evidence map for PORT-*"
      min_lines: 80
    - path: ".planning/phases/05-recommendations-machine-readable-outputs/05-recommendations-machine-readable-outputs-VERIFICATION.md"
      provides: "Evidence map for UX-*"
      min_lines: 80
    - path: ".planning/phases/06-weekly-report-pipeline/06-weekly-report-pipeline-VERIFICATION.md"
      provides: "Evidence map for REPORT-*"
      min_lines: 80
    - path: ".planning/phases/12-v1-audit-verify-phases-4-6/12-VALIDATION.md"
      provides: "Phase 12 validation contract"
      min_lines: 40
  key_links:
    - from: "run_pipeline.py"
      to: "data/regimes/asset_return_profile.parquet"
      via: "step6_asset_returns → returns_by_regime"
      pattern: "step6_asset_returns"
    - from: "pipelines/06_asset_returns.py"
      to: "data/regimes/template_behavior_by_regime.parquet"
      via: "portfolio_templates + compute_template_returns"
      pattern: "template_behavior"
    - from: "run_pipeline.py"
      to: "outputs/reports/"
      via: "step7_dashboard — dashboard.csv, trade_recommendations.csv, weekly_report.md"
      pattern: "step7_dashboard"
    - from: "scripts/run_weekly_report.py"
      to: "run_pipeline.py"
      via: "subprocess steps 2–7 or 1–7"
      pattern: "run_pipeline"
---

<objective>
Produce GSD-grade **verification evidence** for roadmap Phases **4–6** so milestone audit closure for **PORT-01..03**, **UX-01..03**, and **REPORT-01..02** is traceable to code and artifacts. Primary deliverables are three `*-VERIFICATION.md` files (one per phase directory) and an updated **REQUIREMENTS.md** traceability table. Secondary: add **12-VALIDATION.md** so Phase 12 is Nyquist-addressable.

**Non-goal:** Large new features — if verification exposes a real gap (e.g. `run_pipeline` step 6 missing portfolio-template artifacts present in `pipelines/06_asset_returns.py`), record **gaps_found** and either fix in a minimal follow-up commit within this phase or file explicit deferral to Phase 13+/code.
</objective>

<execution_context>
@.planning/v1.0-MILESTONE-AUDIT.md
@.planning/ROADMAP.md
@.planning/REQUIREMENTS.md
@.planning/phases/12-v1-audit-verify-phases-4-6/12-CONTEXT.md
@CLAUDE.md
@run_pipeline.py
@pipelines/06_asset_returns.py
@pipelines/07_dashboard.py
@scripts/run_weekly_report.py
@src/trading_crab_lib/asset_returns.py
@src/trading_crab_lib/reporting.py
@tests/unit/test_returns.py
</execution_context>

<context>
**Audit trigger:** v1.0 milestone audit found **Pending** traceability for eight requirement IDs and **missing** `*-VERIFICATION.md` under phase dirs **04–06**.

**Code reality (discovery snapshot — confirm while executing):**
- **PORT-01:** `returns_by_regime`, `rank_assets_by_regime` in `src/trading_crab_lib/asset_returns.py`; step 6 writes `data/regimes/asset_return_profile.parquet`; `tests/unit/test_returns.py` covers regime profiles and ranking helpers.
- **PORT-02:** `config/settings.yaml` may define `assets.portfolio_templates`; **standalone** `pipelines/06_asset_returns.py` can write `template_behavior_by_regime.parquet`. **`run_pipeline.step6_asset_returns`** (as of planning) may **not** mirror template behavior — verify and document as **gap** or align implementations.
- **PORT-03:** `step7_dashboard` uses `predict_current`, transition matrix, `asset_return_profile` / ranked signals, and `simple_regime_portfolio` / `blended_regime_portfolio` / `generate_recommendation` from `reporting.py` — map to “current + near-term regime” expectations in REQUIREMENTS.
- **UX-01..03:** Dashboard printing, `trade_recommendations.csv`, explanations inside `generate_recommendation` / weekly markdown — cite `reporting.py` and step 7.
- **REPORT-01..02:** `scripts/run_weekly_report.py` drives `run_pipeline.py` steps; `write_weekly_report_md` produces `outputs/reports/weekly_report.md`; email body building in `trading_crab_lib.email`.

**Package paths:** Use `src/trading_crab_lib/` in all new/edited verification text (not `market_regime`).
</context>

<tasks>

<task type="auto" tdd="false">
  <name>Task 1: Discovery pass — parity and artifact matrix</name>
  <files>run_pipeline.py, pipelines/06_asset_returns.py, pipelines/07_dashboard.py, src/trading_crab_lib/reporting.py, config/settings.yaml</files>
  <behavior>
    Build a short matrix (can live inside Task notes or the Phase 04 VERIFICATION): For each requirement ID, list **entrypoint** (function / script), **on-disk artifacts**, **tests** (if any). Explicitly diff **step6** in `run_pipeline.py` vs `pipelines/06_asset_returns.py` for `etf_behavior_by_regime.parquet`, `template_behavior_by_regime.parquet`, and `compute_template_returns`.
  </behavior>
  <action>
    Read the listed files; record findings in draft form before writing verification prose.
  </action>
  <verify>
    Matrix covers all eight REQ-IDs and notes any missing test coverage.
  </verify>
</task>

<task type="auto" tdd="false">
  <name>Task 2: Write Phase 04 VERIFICATION (PORT-01..03)</name>
  <files>.planning/phases/04-regime-conditional-etf-portfolio-behavior/04-regime-conditional-etf-portfolio-behavior-VERIFICATION.md</files>
  <behavior>
    YAML frontmatter: `phase`, `verified` (date), `status: passed | gaps_found`, `score` if applicable. Body: goal, observable truths table, artifacts table, key_links table, requirements table mapping PORT-01..03 to evidence. If template / ETF-behavior artifacts are only produced by standalone pipeline, state **gaps_found** and cite whether canonical path is `run_pipeline` or `pipelines/06_asset_returns.py`.
  </behavior>
  <action>
    Create the file following the tone/structure of `01-data-and-constraints-foundations-VERIFICATION.md` / `03-supervised-regime-behavior-models-VERIFICATION.md`.
  </action>
  <verify>
    File exists; each PORT-* row has ≥1 concrete code or artifact reference.
  </verify>
</task>

<task type="auto" tdd="false">
  <name>Task 3: Write Phase 05 VERIFICATION (UX-01..03)</name>
  <files>.planning/phases/05-recommendations-machine-readable-outputs/05-recommendations-machine-readable-outputs-VERIFICATION.md</files>
  <behavior>
    Map UX-* to `step7_dashboard` (`run_pipeline.py`), `pipelines/07_dashboard.py`, `reporting.py` (`asset_signals`, `generate_recommendation`, `save_dashboard_csv`, `write_weekly_report_md`), and outputs under `outputs/reports/` (e.g. `dashboard.csv`, `trade_recommendations.csv`, optional JSON). Note human judgment for “good enough” explanations.
  </behavior>
  <action>
    Author verification document with frontmatter and structured tables.
  </action>
  <verify>
    UX-03 explicitly lists machine-readable filenames and generators.
  </verify>
</task>

<task type="auto" tdd="false">
  <name>Task 4: Write Phase 06 VERIFICATION (REPORT-01..02)</name>
  <files>.planning/phases/06-weekly-report-pipeline/06-weekly-report-pipeline-VERIFICATION.md</files>
  <behavior>
    Map REPORT-01 to `scripts/run_weekly_report.py` + `run_pipeline.py` step orchestration; REPORT-02 to `weekly_report.md` content contract and `email_body.txt` archive path. Mention `--send-email` only as related Phase 7 scope if needed, without claiming PORT-04 satisfied here.
  </behavior>
  <action>
    Author verification document.
  </action>
  <verify>
    Document includes exact script entrypoint and default step ranges (2–7 vs 1–7).
  </verify>
</task>

<task type="auto" tdd="false">
  <name>Task 5: Add Phase 12 VALIDATION + update REQUIREMENTS traceability</name>
  <files>.planning/phases/12-v1-audit-verify-phases-4-6/12-VALIDATION.md, .planning/REQUIREMENTS.md</files>
  <behavior>
    `12-VALIDATION.md`: Wave 0 checklist referencing the three new verification files + grep/spot-check commands (`pytest tests/unit/test_returns.py -q`, etc.). Set `nyquist_compliant: false` until Wave 0 executed.

    **REQUIREMENTS.md:** For each of the eight IDs, set **Status** to **Complete** only if Tasks 2–4 **status: passed** for that row’s scope; if any verification is **gaps_found**, keep **Pending** and add a one-line footnote under the table pointing to the relevant VERIFICATION section. Do not claim Complete without matching evidence.
  </behavior>
  <action>
    Edit REQUIREMENTS minimally (traceability table only unless footnote needs a small **Notes** column — prefer footnote under table).
  </action>
  <verify>
    No requirement marked Complete contradicts its phase VERIFICATION frontmatter.
  </verify>
</task>

<task type="auto" tdd="false">
  <name>Task 6: ROADMAP bookkeeping + commit</name>
  <files>.planning/ROADMAP.md</files>
  <behavior>
    Under Phase 12 **Plans**, mark plan **01** as present with `[ ]` checkbox until executed; set **Plans** count to `1`. Update Phase 12 **Progress** row `Plans Complete` if your process tracks it (optional `0/1` → `1/1` only after execute-phase).

    Commit planning changes with message like `docs(12): add gap-closure verification plan for phases 4–6`.
  </behavior>
  <action>
    Patch ROADMAP Phase 12 plan list; run `gsd-tools commit` for changed planning files.
  </action>
  <verify>
    `gsd-tools phases list` unchanged count; git shows committed PLAN + ROADMAP updates.
  </verify>
</task>

</tasks>

<notes>
**Optional code fix (if Product owner wants “passed” with no gaps):** Align `run_pipeline.step6_asset_returns` with `pipelines/06_asset_returns.py` (ETF behavior parquet, template returns/behavior, config-driven thresholds). Only in-scope if Task 1 confirms drift; otherwise defer to a future execute plan with tests.
</notes>
