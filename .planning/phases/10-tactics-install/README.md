# Phase 10 — Tactics layer + install & env automation

The v1.0 work for **config-driven tactics (tests)** and **install/env scripts** is **shipped**. This directory is a **brownfield** GSD anchor.

**Evidence**

- [Verification](./10-tactics-install-VERIFICATION.md) — TACTICS-03, INSTALL-10.
- [Validation](./10-VALIDATION.md).

**Primary entrypoints**

- `config/settings.yaml` — `tactics:` thresholds.
- `tests/test_tactics.py` — automated TACTICS-03 coverage.
- `scripts/setup.sh` — venv, deps, `.env` scaffold, directory layout.
- `scripts/install_trading_crab.sh` — conda-friendly install + smoke pytest.
- `scripts/check_env.sh` — import + single pytest node.
- **`scripts/README.md`** — documented happy paths and script behavior.

See repo-root **`RUNBOOK.md`** for weekly report and email flows.
