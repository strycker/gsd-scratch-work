---
phase: 21-v1-2-email-and-install
plan: 01
type: execute
wave: 1
depends_on:
  - 20-v1-2-tactics-layer
files_modified:
  - scripts/setup.sh
  - scripts/README.md
  - RUNBOOK.md
  - tests/test_gitignore_secrets.py
  - .planning/REQUIREMENTS.md
  - .planning/phases/21-v1-2-email-and-install/21-SUMMARY.md
autonomous: true
requirements:
  - EMAIL-10
  - INSTALL-20
user_setup:
  - None for unit tests; optional real SMTP for manual smoke
must_haves:
  truths:
    - "scripts/setup.sh copies config/email.example.yaml to config/email.local.yaml when the latter is missing (non-destructive), matching install_trading_crab.sh behavior."
    - "RUNBOOK.md documents the --send-email / run_weekly_report.py SMTP path and points to config/email.example.yaml."
    - "Automated test asserts .gitignore (or equivalent) ignores config/email.local.yaml and .env."
    - "scripts/README.md documents a two-command happy path: setup then weekly report with --send-email (with prerequisites stated)."
    - "No secrets committed; existing email.py and CLI remain the implementation source of truth."
  artifacts:
    - path: "scripts/setup.sh"
      provides: "optional email.local.yaml scaffold"
    - path: "RUNBOOK.md"
      provides: "SMTP / EMAIL-10 operator section"
    - path: "tests/test_gitignore_secrets.py"
      provides: "gitignore contract test"
    - path: "scripts/README.md"
      provides: "happy path + --send-email"
---

<objective>
Close **EMAIL-10** and **INSTALL-20** for v1.2 by **hardening operator docs** and **setup parity** (scaffold `email.local.yaml` in `setup.sh`), adding a **gitignore contract test**, and updating **REQUIREMENTS** traceability — without re-implementing SMTP (already in `trading_crab_lib/email.py`).
</objective>

**Non-goals:** New email providers; mandatory HTML bodies; changing `email.py` API unless a bug is found during review.

<execution_context>
@.planning/phases/21-v1-2-email-and-install/21-CONTEXT.md
@.planning/REQUIREMENTS.md
@.planning/ROADMAP.md
@src/trading_crab_lib/email.py
@run_pipeline.py
@scripts/run_weekly_report.py
@scripts/setup.sh
@config/email.example.yaml
@.gitignore
</execution_context>

<context>
**Regression guard:**  
`PYTHONPATH=src python -m pytest tests/test_gitignore_secrets.py tests/test_email_weekly.py tests/test_scripts_weekly_report.py -q` after tasks.
</context>

<tasks>

<task type="auto" tdd="true">
  <name>Task 1 — setup.sh: scaffold email.local.yaml</name>
  <read_first>
    - scripts/setup.sh (full file)
    - scripts/install_trading_crab.sh (email copy block ~lines 39–41)
    - config/email.example.yaml
  </read_first>
  <action>
    1. After the `.env` block (section 5), add **section 5b** (or renumber): if `config/email.local.yaml` is missing and `config/email.example.yaml` exists, `cp` example → local and print a yellow **ACTION REQUIRED** line: edit SMTP fields (reference Gmail/app-password docs link from `email.example.yaml` comments).
    2. Do not overwrite existing `email.local.yaml`.
    3. Update the final "Next steps" echo to mention optional weekly email when `email.local.yaml` is configured.
  </action>
  <acceptance_criteria>
    - `grep -n email.example.yaml scripts/setup.sh` returns at least one match.
    - `grep -n email.local.yaml scripts/setup.sh` returns at least one match.
    - `bash -n scripts/setup.sh` exits 0.
  </acceptance_criteria>
</task>

<task type="auto" tdd="true">
  <name>Task 2 — tests/test_gitignore_secrets.py</name>
  <read_first>
    - .gitignore
    - tests/conftest.py (if path helpers exist)
  </read_first>
  <action>
    1. Add `tests/test_gitignore_secrets.py` that reads **repository root** `.gitignore` text and asserts **both** `.env` and `config/email.local.yaml` (or `email.local.yaml` / `**/email.local.yaml`) appear as ignored patterns (substring match is acceptable; document if pattern is `config/email.local.yaml` exactly).
    2. Keep test hermetic (no subprocess `git`).
  </action>
  <acceptance_criteria>
    - `pytest tests/test_gitignore_secrets.py -q` exits 0.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 3 — RUNBOOK.md + scripts/README.md</name>
  <read_first>
    - RUNBOOK.md (Environment-only email section ~188)
    - scripts/README.md (run_weekly_report section)
  </read_first>
  <action>
    1. Add a dedicated subsection **SMTP / weekly email (EMAIL-10)** under extended pipeline or environment: document `python run_pipeline.py --steps ... --weekly-report --send-email` (or the minimal step set that produces `weekly_report.md` before send), `scripts/run_weekly_report.py --send-email`, `config/email.example.yaml` → `email.local.yaml`, link to `trading_crab_lib/email.py`.
    2. In `scripts/README.md`, add **Happy path (new machine)** with two commands: `bash scripts/setup.sh` then `python scripts/run_weekly_report.py --send-email` with bullet prerequisites (FRED keys, prior pipeline outputs or `--full`).
  </action>
  <acceptance_criteria>
    - `grep -n EMAIL-10 RUNBOOK.md` returns at least one match OR `grep -n "send-email" RUNBOOK.md` matches updated section.
    - `grep -n "Happy path" scripts/README.md` returns at least one match.
  </acceptance_criteria>
</task>

<task type="auto" tdd="false">
  <name>Task 4 — REQUIREMENTS + 21-SUMMARY</name>
  <read_first>
    - .planning/REQUIREMENTS.md
  </read_first>
  <action>
    1. Mark **EMAIL-10** and **INSTALL-20** complete with pointers to `setup.sh`, `RUNBOOK`, `email.py`, `test_gitignore_secrets.py`.
    2. Update traceability table rows for Phase 21 → Complete.
    3. Create `21-SUMMARY.md` on execute-phase completion.
  </action>
  <acceptance_criteria>
    - `grep EMAIL-10 .planning/REQUIREMENTS.md` shows `[x]` or Complete.
    - `grep INSTALL-20 .planning/REQUIREMENTS.md` shows `[x]` or Complete.
  </acceptance_criteria>
</task>

</tasks>

<verification>

## Automated

- `PYTHONPATH=src python -m pytest tests/test_gitignore_secrets.py tests/test_email_weekly.py tests/test_scripts_weekly_report.py -q`
- `python -c "from trading_crab_lib.config import load; load()"`

## Manual

- Configure `config/email.local.yaml` (test mailbox) and run `python scripts/run_weekly_report.py --send-email` after a successful weekly report artifact run.

</verification>

---

## PLANNING COMPLETE
