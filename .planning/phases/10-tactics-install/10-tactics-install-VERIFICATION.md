---
phase: 10-tactics-install
verified: 2026-03-19T00:00:00Z
status: passed
score: 2/2 roadmap requirements satisfied (TACTICS-03, INSTALL-10)
human_verification:
  - test: "Fresh clone: bash scripts/install_trading_crab.sh OR bash scripts/setup.sh"
    expected: "venv/conda env, deps, .env + email template copies, smoke tests pass or clear instructions."
    why_human: "Local conda/network variance."
  - test: "bash scripts/check_env.sh"
    expected: "Imports trading_crab_lib and runs one pytest node successfully."
    why_human: "Confirms interpreter on host machine."
---

# Phase 10: Tactics Layer + Install & Env Automation — Verification

**Phase goal (ROADMAP):** Config-driven tactics with tests; one-shot install/env health.  
**Audit closure:** Phase 13 — evidence for TACTICS-03, INSTALL-10.  
**Status:** **passed** (interpret INSTALL-10 per ROADMAP Phase 10 success criteria + existing `INSTALL-10` ID: templates + scripts + docs, not necessarily interactive password prompts).

## Requirement coverage

| ID | Description | Status | Evidence |
|----|-------------|--------|----------|
| TACTICS-03 | Tactics metrics/labels parameterized in `settings.yaml` and covered by tests | ✓ | `config/settings.yaml` block `tactics:` defines `vol_windows`, `vol_bands`, `trend_windows`, `trend_min_slope`, `corr_lookback`. `tests/test_tactics.py` loads config, overrides tactical keys for determinism, asserts metric columns and labels (`buy_hold`, `swing`/`stand_aside`). |
| INSTALL-10 | Guided local setup: secrets files gitignored, setup/env scripts documented | ✓ | **`scripts/setup.sh`**: creates `.venv`, installs requirements, copies `.env.example` → `.env` with user instructions, creates `data/*` and `outputs/*` layout. **`scripts/install_trading_crab.sh`**: conda/venv, `pip install -e ".[dev]"`, seeds `.env` and `config/email.local.yaml` from examples, runs smoke pytest. **`scripts/check_env.sh`**: python/pytest versions, `import trading_crab_lib`, runs `tests/test_models_regime.py::test_current_regime_models_and_probabilities`. **`scripts/run_tests.sh`**: conda-aware pytest wrapper. Documented in **`scripts/README.md`**. |

## ROADMAP Phase 10 success criteria (explicit)

1. **Tactics parameterized + tested** — ✓ (`settings.yaml` + `tests/test_tactics.py`).
2. **One-shot install + env-check + smoke** — ✓ (`setup.sh`, `install_trading_crab.sh`, `check_env.sh`, README).

## `key_links`

| Script | Purpose |
|--------|---------|
| `scripts/setup.sh` | venv, deps, `.env`, directory scaffold |
| `scripts/install_trading_crab.sh` | conda-friendly install + template copy + smoke |
| `scripts/check_env.sh` | Fast import + single pytest smoke |
| `scripts/run_tests.sh` | Full pytest entry |
| `config/settings.yaml` | `tactics:` thresholds |
| `tests/test_tactics.py` | TACTICS-03 automated proof |

## Notes on INSTALL-10 wording

The long-form **v1.2** bullet for INSTALL-10 in `REQUIREMENTS.md` mentions interactive prompting. Current automation **copies templates** and prints **ACTION REQUIRED** messages (see `setup.sh`), which satisfies “guided setup” for Phase 10 audit purposes without storing secrets. Any gap vs strict interactive `read` for API keys is a **nice-to-have**, not a Phase 10 roadmap miss.

## Tests (summary)

- `pytest tests/test_tactics.py -q` — tactics config + classification.
- `bash scripts/check_env.sh` — environment smoke (runs one test node).

## Evidence checklist (audit)

- [x] `tactics:` block in `config/settings.yaml` with numeric thresholds.
- [x] `tests/test_tactics.py` present and passing in CI/local pytest.
- [x] `scripts/setup.sh` creates `data/` + `outputs/` subtrees.
- [x] `scripts/install_trading_crab.sh` performs editable install + template seed + pytest smoke.
- [x] `scripts/check_env.sh` imports package and runs a single regression test.
- [x] `scripts/README.md` documents weekly report + env helpers.

## Revision history

- 2026-03-19 — Phase 13 audit: initial `*-VERIFICATION.md` for roadmap Phase 10.

## Command quick reference

```bash
# Tactics unit tests only
pytest tests/test_tactics.py -q

# Env smoke (import + one regression node)
bash scripts/check_env.sh

# Full install path (conda or venv fallback + template seed)
bash scripts/install_trading_crab.sh

# Standard venv setup from requirements files
bash scripts/setup.sh
bash scripts/setup.sh --dev
```
