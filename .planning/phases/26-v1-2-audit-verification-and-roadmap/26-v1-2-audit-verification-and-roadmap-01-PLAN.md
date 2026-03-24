---
wave: 1
depends_on: []
requirements:
  - CLOSURE-01
  - CLOSURE-02
  - CLOSURE-03
  - DATA-10
  - DATA-11
files_modified:
  - .planning/ROADMAP.md
  - .planning/phases/17-v1-2-expanded-macro-signals/17-VERIFICATION.md
  - .planning/phases/21-v1-2-email-and-install/21-VERIFICATION.md
  - .planning/phases/22-v1-2-providers-universe/22-VERIFICATION.md
  - .planning/phases/23-v1-0-plan-summary-parity/23-VERIFICATION.md
  - .planning/phases/24-v1-0-brownfield-phase-readmes/24-VERIFICATION.md
  - .planning/phases/25-v1-0-phase3-plan04-reconciliation/25-VERIFICATION.md
  - .planning/phases/17-v1-2-expanded-macro-signals/17-VALIDATION.md
  - .planning/phases/18-v1-2-signal-diagnostics/18-VALIDATION.md
  - .planning/phases/19-v1-2-boosted-models/19-VALIDATION.md
autonomous: true
gap_closure: true
source_audit: .planning/v1.2-MILESTONE-AUDIT.md
---

# Phase 26 — Audit verification files & roadmap alignment

**Mode:** Gap closure (no product feature work). **Evidence:** Reuse existing `*-SUMMARY.md`, `*-VALIDATION.md` (where present), `*-VERIFICATION.md` (17–20), and `v1.2-MILESTONE-AUDIT.md`.

---

## Wave 1 — Roadmap + Phase 17 DATA-10 evidence

<task id="26-01-01">
<title>Align ROADMAP Phase 17 with shipped DATA-10</title>
<read_first>
- `.planning/ROADMAP.md` (lines 10–140: Phases list, Phase 17 detail, Progress table)
- `.planning/v1.2-MILESTONE-AUDIT.md` (DATA-10 / roadmap drift)
</read_first>
<action>
1. In **Phases (v1.2 — current)** list, change Phase **17** from `- [ ]` to `- [x]` (same style as phases 18–25).
2. In **Progress** table, row **17**: set **Plans Complete** to `1/1` (or match actual plan count under `17-v1-2-expanded-macro-signals/` — use `ls .planning/phases/17-v1-2-expanded-macro-signals/*-PLAN.md | wc -l` for exact numerator); set **Status** to `Complete`; set **Notes** to `DATA-10` (or `DATA-10 — see 17-VERIFICATION.md`).
3. Do **not** remove Phase 17 success criteria text; only fix checkbox/table drift called out in the audit.
</action>
<acceptance_criteria>
- `grep -n 'Phase 17: v1.2' .planning/ROADMAP.md` shows a line containing `- [x]` for Phase 17 in the v1.2 checklist block (not `- [ ]`).
- Progress table row for phase `17` contains `Complete` (exact word) in the Status column.
- `grep '17 |' .planning/ROADMAP.md | grep -q 'Complete'` exits 0.
</acceptance_criteria>
</task>

<task id="26-01-02">
<title>Promote `17-VERIFICATION.md` to `status: passed` with explicit optional human smoke</title>
<read_first>
- `.planning/phases/17-v1-2-expanded-macro-signals/17-VERIFICATION.md` (full file — frontmatter + Human verification section)
- `.planning/phases/15-v1-gap-regime-profiles-names/15-VERIFICATION.md` (example `status: passed` frontmatter)
</read_first>
<action>
1. In YAML frontmatter: set `status: passed` (replace `human_needed`). Keep `verified` timestamp or bump to execution date if you re-verify content.
2. Set `score:` line to reflect **5/5** plan must-haves at code/test level (keep existing narrative).
3. In the body, change **Overall status** paragraph to state **`passed`** for automated/code criteria; **retain** the existing **Human verification required** section verbatim (live FRED step 1 remains optional / out-of-CI).
4. Add one short bullet under **Gaps summary** or **Recommended fix plans**: "Optional human: live `FRED_API_KEY` step 1 — unchanged; does not block `passed` for CI-verifiable scope."
</action>
<acceptance_criteria>
- `grep -A2 '^---$' .planning/phases/17-v1-2-expanded-macro-signals/17-VERIFICATION.md | head -5` — first frontmatter block includes `status: passed`.
- File still contains the heading `## Human verification required` (exact) OR equivalent `## Human verification` section title preserved from original.
- `grep 'human_needed' .planning/phases/17-v1-2-expanded-macro-signals/17-VERIFICATION.md` exits 1 (no stale `human_needed` string).
</acceptance_criteria>
</task>

---

## Wave 2 — Missing `*-VERIFICATION.md` for phases 21–25

<task id="26-02-01">
<title>Add `21-VERIFICATION.md` (EMAIL-10, INSTALL-20)</title>
<read_first>
- `.planning/phases/21-v1-2-email-and-install/21-SUMMARY.md`
- `.planning/phases/21-v1-2-email-and-install/21-VALIDATION.md`
- `.planning/phases/21-v1-2-email-and-install/21-v1-2-email-and-install-01-PLAN.md` (must_haves if present)
- `.planning/phases/15-v1-gap-regime-profiles-names/15-VERIFICATION.md` (structure)
</read_first>
<action>
Create **`.planning/phases/21-v1-2-email-and-install/21-VERIFICATION.md`** with:
- Frontmatter: `phase: 21-v1-2-email-and-install`, `verified: <ISO8601 date>`, `status: passed`, `requirements: [EMAIL-10, INSTALL-20]`.
- Sections: Phase goal (from ROADMAP Phase 21); **Observable truths** table mapping each **21** plan `must_have` / SUMMARY bullet to repo paths: `src/trading_crab_lib/email.py`, `run_pipeline.py` / `scripts/run_weekly_report.py`, `config/email.example.yaml`, `scripts/setup.sh`, `tests/test_gitignore_secrets.py`, `tests/test_email_weekly.py`, `RUNBOOK.md` SMTP section.
- **Requirements coverage:** both EMAIL-10 and INSTALL-20 marked satisfied with pointers to `21-SUMMARY.md` commands.
- **Note:** Cite `v1.2-MILESTONE-AUDIT.md` integration finding (step 7 vs 8/9 / `run_weekly_report.py` scope) as **deferred to Phase 27** — do not claim fixed here.
</action>
<acceptance_criteria>
- `test -f .planning/phases/21-v1-2-email-and-install/21-VERIFICATION.md` exits 0.
- `grep -q 'EMAIL-10' .planning/phases/21-v1-2-email-and-install/21-VERIFICATION.md` exits 0.
- `grep -q 'INSTALL-20' .planning/phases/21-v1-2-email-and-install/21-VERIFICATION.md` exits 0.
- `grep -q 'Phase 27' .planning/phases/21-v1-2-email-and-install/21-VERIFICATION.md` exits 0 (audit deferral pointer).
</acceptance_criteria>
</task>

<task id="26-02-02">
<title>Add `22-VERIFICATION.md` (DATA-11)</title>
<read_first>
- `.planning/phases/22-v1-2-providers-universe/22-SUMMARY.md`
- `.planning/phases/22-v1-2-providers-universe/22-VALIDATION.md`
- `.planning/phases/22-v1-2-providers-universe/22-v1-2-providers-universe-01-PLAN.md`
- `tests/unit/test_assets_providers.py` (first 80 lines)
</read_first>
<action>
Create **`.planning/phases/22-v1-2-providers-universe/22-VERIFICATION.md`** with frontmatter `status: passed`, `requirements: [DATA-11]`. Truth table: `config/settings.yaml` `assets.providers`; `src/trading_crab_lib/ingestion/assets.py` `_provider_flags`, stooq merge behavior; `tests/unit/test_assets_providers.py`; `RUNBOOK.md` DATA-11 section if present. Link to `22-SUMMARY.md` verification commands.
</action>
<acceptance_criteria>
- `test -f .planning/phases/22-v1-2-providers-universe/22-VERIFICATION.md` exits 0.
- `grep -q 'DATA-11' .planning/phases/22-v1-2-providers-universe/22-VERIFICATION.md` exits 0.
- `grep -q 'test_assets_providers' .planning/phases/22-v1-2-providers-universe/22-VERIFICATION.md` exits 0.
</acceptance_criteria>
</task>

<task id="26-02-03">
<title>Add `23-VERIFICATION.md` (CLOSURE-01)</title>
<read_first>
- `.planning/phases/23-v1-0-plan-summary-parity/23-SUMMARY.md`
- `.planning/phases/23-v1-0-plan-summary-parity/23-VALIDATION.md`
- `.planning/phases/23-v1-0-plan-summary-parity/23-v1-0-plan-summary-parity-01-PLAN.md`
</read_first>
<action>
Create **`.planning/phases/23-v1-0-plan-summary-parity/23-VERIFICATION.md`**: goal **CLOSURE-01**; truths: six `*-01-SUMMARY.md` files + `gsd-tools validate health` / I001 as described in `23-SUMMARY.md`; `status: passed` if evidence matches shipped state. Include table listing each plan→summary basename pair from `23-SUMMARY.md`.
</action>
<acceptance_criteria>
- `test -f .planning/phases/23-v1-0-plan-summary-parity/23-VERIFICATION.md` exits 0.
- `grep -q 'CLOSURE-01' .planning/phases/23-v1-0-plan-summary-parity/23-VERIFICATION.md` exits 0.
- `grep -q 'validate health' .planning/phases/23-v1-0-plan-summary-parity/23-VERIFICATION.md` exits 0.
</acceptance_criteria>
</task>

<task id="26-02-04">
<title>Add `24-VERIFICATION.md` (CLOSURE-02)</title>
<read_first>
- `.planning/phases/24-v1-0-brownfield-phase-readmes/24-SUMMARY.md`
- `.planning/phases/24-v1-0-brownfield-phase-readmes/24-VALIDATION.md`
- `.planning/phases/24-v1-0-brownfield-phase-readmes/24-v1-0-brownfield-phase-readmes-01-PLAN.md`
</read_first>
<action>
Create **`.planning/phases/24-v1-0-brownfield-phase-readmes/24-VERIFICATION.md`**: truths = each brownfield directory from CLOSURE-02 list has `README.md` with pointers to `*-VERIFICATION.md` / `*-VALIDATION.md` / pipeline entrypoints; use `glob` or `find` evidence from repo. `status: passed`.
</action>
<acceptance_criteria>
- `test -f .planning/phases/24-v1-0-brownfield-phase-readmes/24-VERIFICATION.md` exits 0.
- `grep -q 'CLOSURE-02' .planning/phases/24-v1-0-brownfield-phase-readmes/24-VERIFICATION.md` exits 0.
- `grep -q 'README.md' .planning/phases/24-v1-0-brownfield-phase-readmes/24-VERIFICATION.md` exits 0.
</acceptance_criteria>
</task>

<task id="26-02-05">
<title>Add `25-VERIFICATION.md` (CLOSURE-03)</title>
<read_first>
- `.planning/phases/25-v1-0-phase3-plan04-reconciliation/25-SUMMARY.md`
- `.planning/phases/25-v1-0-phase3-plan04-reconciliation/25-VALIDATION.md`
- `.planning/phases/25-v1-0-phase3-plan04-reconciliation/25-v1-0-phase3-plan04-reconciliation-01-PLAN.md`
- `.planning/phases/03-supervised-regime-behavior-models/03-supervised-regime-behavior-models-04-SUMMARY.md`
</read_first>
<action>
Create **`.planning/phases/25-v1-0-phase3-plan04-reconciliation/25-VERIFICATION.md`**: truths = reconciliation matrix / waiver from `03-supervised-regime-behavior-models-04-SUMMARY.md` + `25-SUMMARY.md`; pointer to `03-*-VERIFICATION.md` updates if cited. `status: passed`.
</action>
<acceptance_criteria>
- `test -f .planning/phases/25-v1-0-phase3-plan04-reconciliation/25-VERIFICATION.md` exits 0.
- `grep -q 'CLOSURE-03' .planning/phases/25-v1-0-phase3-plan04-reconciliation/25-VERIFICATION.md` exits 0.
- `grep -q '03-supervised-regime-behavior-models-04' .planning/phases/25-v1-0-phase3-plan04-reconciliation/25-VERIFICATION.md` exits 0.
</acceptance_criteria>
</task>

---

## Wave 3 — Nyquist `*-VALIDATION.md` for phases 17–19

<task id="26-03-01">
<title>Add `17-VALIDATION.md`, `18-VALIDATION.md`, `19-VALIDATION.md` (parity with phases 20–25)</title>
<read_first>
- `.codex/get-shit-done/templates/VALIDATION.md`
- `.planning/phases/20-v1-2-tactics-layer/20-VALIDATION.md`
- `.planning/phases/17-v1-2-expanded-macro-signals/17-VERIFICATION.md` (pytest commands)
- `.planning/phases/18-v1-2-signal-diagnostics/18-VERIFICATION.md` (pytest commands)
- `.planning/phases/19-v1-2-boosted-models/19-VERIFICATION.md` (pytest commands)
</read_first>
<action>
For each of **17**, **18**, **19**:
1. Create **`.planning/phases/{NN}-v1-2-*/{NN}-VALIDATION.md`** (exact directory names: `17-v1-2-expanded-macro-signals`, `18-v1-2-signal-diagnostics`, `19-v1-2-boosted-models`).
2. Frontmatter: `phase: {N}`, `slug:` matching sibling `*-CONTEXT.md` or folder convention, `status: validated`, `nyquist_compliant: true`, `wave_0_complete: true`, `created: 2026-03-24` (or current date), `validated: 2026-03-24`.
3. Body: **Test Infrastructure** table — copy **exact** pytest command lines from each phase’s `*-VERIFICATION.md` **Automated verification commands** fenced blocks (e.g. `tests/unit/test_transforms.py` for 17; diagnostics tests for 18; `tests/test_models_boosting.py` for 19).
4. **Per-Task Verification Map:** minimal table pointing to gap-closure evidence (VERIFICATION report + tests).
</action>
<acceptance_criteria>
- `test -f .planning/phases/17-v1-2-expanded-macro-signals/17-VALIDATION.md` exits 0.
- `test -f .planning/phases/18-v1-2-signal-diagnostics/18-VALIDATION.md` exits 0.
- `test -f .planning/phases/19-v1-2-boosted-models/19-VALIDATION.md` exits 0.
- Each file’s frontmatter includes `nyquist_compliant: true` (`grep -l 'nyquist_compliant: true' ...` returns three files).
- Each file references `pytest` at least once (`grep -q pytest` on each file exits 0).
</acceptance_criteria>
</task>

---

## Verification criteria (execute-phase)

- All **acceptance_criteria** grep/test commands in tasks pass.
- `ls .planning/phases/21-v1-2-email-and-install/21-VERIFICATION.md` … `25-.../25-VERIFICATION.md` — five new files.
- Optional: `node .codex/get-shit-done/bin/gsd-tools.cjs validate health` — note any pre-existing I001 outside CLOSURE-01 scope in **25-VERIFICATION** notes, not as blocker for this phase.

---

## must_haves (goal-backward / `$gsd-verify-phase`)

```yaml
must_haves:
  truths:
    - id: T1
      description: "ROADMAP Phase 17 checkbox and Progress row show Complete for DATA-10 shipped work."
    - id: T2
      description: "`17-VERIFICATION.md` frontmatter `status: passed`; optional human FRED smoke documented as non-blocking."
    - id: T3
      description: "Phases 21–25 each have `*-VERIFICATION.md` with `status: passed` and REQ-ID coverage."
    - id: T4
      description: "Phases 17–19 each have `*-VALIDATION.md` with `nyquist_compliant: true` and pytest commands from VERIFICATION."
  artifacts:
    - path: .planning/ROADMAP.md
    - path: .planning/phases/17-v1-2-expanded-macro-signals/17-VERIFICATION.md
    - path: .planning/phases/21-v1-2-email-and-install/21-VERIFICATION.md
    - path: .planning/phases/22-v1-2-providers-universe/22-VERIFICATION.md
    - path: .planning/phases/23-v1-0-plan-summary-parity/23-VERIFICATION.md
    - path: .planning/phases/24-v1-0-brownfield-phase-readmes/24-VERIFICATION.md
    - path: .planning/phases/25-v1-0-phase3-plan04-reconciliation/25-VERIFICATION.md
    - path: .planning/phases/17-v1-2-expanded-macro-signals/17-VALIDATION.md
    - path: .planning/phases/18-v1-2-signal-diagnostics/18-VALIDATION.md
    - path: .planning/phases/19-v1-2-boosted-models/19-VALIDATION.md
```

---

## PLANNING COMPLETE

- **Plans:** 1 (`26-v1-2-audit-verification-and-roadmap-01-PLAN.md`)
- **Waves:** 3 (roadmap + 17-VER; five VERIFICATION files; three VALIDATION files)
- **Mode:** gap_closure + documentation only
