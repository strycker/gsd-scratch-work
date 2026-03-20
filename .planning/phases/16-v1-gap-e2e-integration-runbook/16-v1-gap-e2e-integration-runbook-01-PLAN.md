---
phase: 16-v1-gap-e2e-integration-runbook
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - RUNBOOK.md
  - ARCHITECTURE.md
  - .planning/phases/16-v1-gap-e2e-integration-runbook/16-SUMMARY.md
autonomous: true
requirements:
  - CORE-01
  - MODEL-01
  - MODEL-02
  - MODEL-03
  - MODEL-04
  - REGIME-03
  - PORT-01
  - DIAG-01
  - DIAG-02
  - TACTICS-01
  - TACTICS-02
  - REPORT-01
  - REPORT-02
must_haves:
  truths:
    - "Repo root RUNBOOK.md exists with locked H2 sections + v1.0 audit integration index table mapping each gaps.integration / relevant tech_debt bullet to a section anchor."
    - "Golden-path and partial-rerun recipes use copy-paste commands aligned with run_pipeline.py COMMON WORKFLOWS (workflows ①–⑦ minimum)."
    - "Single market_code strategy end-to-end is explicit (predicted vs clustered vs grok vs omitted); stale partial reruns called out."
    - "Steps 1–7 vs 8–9 documented; DIAG/TACTICS/report dependencies on step 8–9 artifacts stated without new product scope."
    - "ARCHITECTURE.md links to RUNBOOK.md in one short line or subsection per 16-CONTEXT.md."
  artifacts:
    - path: "RUNBOOK.md"
      provides: "Canonical operational runbook for milestone audit integration closure"
    - path: "ARCHITECTURE.md"
      provides: "Pointer to RUNBOOK for operational flows"
---

<objective>
Execute **Phase 16**: add **`RUNBOOK.md`** at repo root closing **`$gsd-audit-milestone` `gaps.integration`** (semantic `market_code` discipline, golden + partial paths, checkpoint staleness, post–re-cluster checklist, steps **8–9**), plus a **single** pointer from **`ARCHITECTURE.md`**. Documentation only — align wording with **`run_pipeline.py`** header, link **`CLAUDE.md`** for full CLI.
</objective>

<execution_context>
@.planning/phases/16-v1-gap-e2e-integration-runbook/16-CONTEXT.md
@.planning/v1.0-MILESTONE-AUDIT.md
@.planning/ROADMAP.md
@.planning/REQUIREMENTS.md
@CLAUDE.md
@run_pipeline.py
@ARCHITECTURE.md
</execution_context>

<context>
**Audit YAML to map** (`.planning/v1.0-MILESTONE-AUDIT.md`): `gaps.integration` three findings + `tech_debt.operational` (checkpoint freshness, REPORT-03/INSTALL-10). Each row in the index table must cite the **exact** subsection heading text in `RUNBOOK.md` (for grep/re-audit).

**Invariant reminder:** Centered `features` for cluster 3–4; causal `features_supervised` for step 5+ per `ARCHITECTURE.md` §1 — runbook must state this once to prevent supervised/overlay mistakes.
</context>

<tasks>

<task type="auto" tdd="false">
  <name>Task 1 — Author RUNBOOK.md (structure + content)</name>
  <read_first>
    - run_pipeline.py (lines 1–143: steps list + flags + COMMON WORKFLOWS + MARKET CODE EXPLAINED)
    - ARCHITECTURE.md (§1 two feature files, §10 clustering_features / regime_labels)
    - .planning/v1.0-MILESTONE-AUDIT.md (YAML `gaps.integration`, `tech_debt.operational`)
    - CLAUDE.md (How to Run / CLI reference pointer)
  </read_first>
  <action>
    Create **`RUNBOOK.md`** at **repository root** with these **H2 headings** (exact strings for grep/anchors):
    - `## Prerequisites`
    - `## Golden path`
    - `## Partial reruns and when to use them`
    - `## market_code and save-market-code`
    - `## Checkpoint hygiene and staleness`
    - `## After re-clustering (regime_labels checklist)`
    - `## Extended pipeline: steps 8 and 9`
    - `## Environment-only: email and setup (REPORT-03 / INSTALL-10)`
    - `## v1.0 milestone audit — integration index`

    Content requirements:
    1. **Prerequisites:** venv, `pip install -e ".[dev]"`, `cp .env.example .env`, `FRED_API_KEY`, optional `k-means-constrained`; link `CLAUDE.md` Environment Setup.
    2. **Golden path:** At least two copy-paste blocks: (a) fresh scrape `python run_pipeline.py --refresh --recompute --plots` with **either** `--market-code grok --save-market-code` **or** fully data-driven `--save-market-code` only — taken from `run_pipeline.py` workflows ①–②; (b) fast rerun `python run_pipeline.py --steps 3,4,5,6,7 --plots` with note to pass consistent `--market-code` when overlays matter.
    3. **Partial reruns:** Include workflow ⑧ `--recompute --steps 2,3,4,5,6,7` and workflow ④–⑤–⑦ patterns from `run_pipeline.py`; state **single** `market_code` source for a coherent run (recommend **`predicted`** after full 1–5, or **`clustered`** after `--save-market-code`, or **`grok`** for baseline; warn against mixing without rerunning 4–7).
    4. **market_code section:** Paraphrase **MARKET CODE EXPLAINED** + list checkpoints snippet from `run_pipeline.py` (the `CheckpointManager` listing one-liner); include worked examples ⑤⑥⑦ as fenced code blocks.
    5. **Checkpoint hygiene:** `--refresh` vs `--recompute` vs `--refresh-assets` per `run_pipeline.py`; manifest under `data/checkpoints/`; explicitly warn that changing `clustering_features` or `regime_labels.yaml` / label column without recomputing yields **stale** classifiers vs returns (cite `ARCHITECTURE.md` §10).
    6. **After re-clustering:** Bullet checklist: run step 3+; verify `balanced_k`; update `config/regime_labels.yaml` if IDs change; re-run 4–7.
    7. **Steps 8–9:** Table or bullets: step 8 = diagnostics (`outputs/reports/diagnostics/`); step 9 = `tactics_signals.parquet`; weekly report **may** include tactics block when artifact exists (align with `REQUIREMENTS` / `CLAUDE.md`); example: `python run_pipeline.py --steps 1,2,3,4,5,6,7,8,9 --plots` or minimal `8,9` after core artifacts exist.
    8. **Environment-only:** REPORT-03 / INSTALL-10 — SMTP/secrets not required for file-based `outputs/reports/`; link `scripts/README.md` or installer docs if present.
    9. **Audit index:** Markdown table with columns: **Audit source** | **RUNBOOK section**. Rows must cover all three `gaps.integration` findings + both `tech_debt.operational` strings (paraphrase audit text in first column).

    Keep file **≤ 320 lines** unless essential; link out rather than duplicate full `CLAUDE.md` flag table.
  </action>
  <acceptance_criteria>
    - `test -f RUNBOOK.md` and `grep -c '^## ' RUNBOOK.md` returns **at least 9** (nine H2 sections as listed).
    - `grep -n 'v1.0 milestone audit — integration index' RUNBOOK.md` returns at least one match (exact H2 line).
    - `grep -n 'market_code_predicted' RUNBOOK.md` returns at least one match.
    - `grep -n 'steps 8' RUNBOOK.md` returns at least one match (extended pipeline section).
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 2 — Pointer from ARCHITECTURE.md</name>
  <read_first>
    - ARCHITECTURE.md (first 15 lines)
  </read_first>
  <action>
    After the opening title block (after the first `---` horizontal rule following the intro paragraph), insert a **short** paragraph (2–4 lines max):

    - Must contain the literal substring **`RUNBOOK.md`** as a markdown link target: `[RUNBOOK.md](RUNBOOK.md)` or `` `RUNBOOK.md` ``.
    - Must state that **operational** commands / golden paths / `market_code` discipline live there.

    Do not move or rewrite existing ADR sections.
  </action>
  <acceptance_criteria>
    - `grep -n 'RUNBOOK.md' ARCHITECTURE.md` returns **≥ 1** match in the first **40** lines of the file.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 3 — Phase execution summary</name>
  <read_first>
    - .planning/phases/15-v1-gap-regime-profiles-names/15-SUMMARY.md (style reference)
  </read_first>
  <action>
    Create **`.planning/phases/16-v1-gap-e2e-integration-runbook/16-SUMMARY.md`** (≥15 lines) listing: files touched, how audit index maps to sections, and suggested next step `$gsd-audit-milestone` or `$gsd-verify-phase 16`.
  </action>
  <acceptance_criteria>
    - `wc -l .planning/phases/16-v1-gap-e2e-integration-runbook/16-SUMMARY.md | awk '{print $1}'` outputs an integer **≥ 15**.
  </acceptance_criteria>
</task>

</tasks>

<verification>
- `grep -E '^## ' RUNBOOK.md | wc -l` ≥ 9
- `grep 'RUNBOOK.md' ARCHITECTURE.md | head -1` non-empty
</verification>

<success_criteria>
- ROADMAP Phase 16 success criteria 1–2 satisfied by `RUNBOOK.md` + `ARCHITECTURE.md` pointer.
- Requirement evidence targets (CORE/MODEL/REGIME/PORT/DIAG/TACTICS/REPORT) referenced by operational clarity in docs without flipping REQUIREMENTS rows to Pending.
</success_criteria>
