---
phase: 32
slug: v1-3-pypi-release-engineering
status: complete
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-25
---

# Phase 32 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x |
| **Config file** | `pyproject.toml` (`[tool.pytest.ini_options]`) |
| **Quick run command** | `pytest tests/ -q` |
| **Full suite command** | `pytest tests/ -v` |
| **Estimated runtime** | ~2–5 minutes (excluding `RUN_WHEEL_SMOKE`) |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/ -q`
- **After packaging tasks:** Run `python -m build` + `twine check dist/*` (clean `dist/` first)
- **Before `$gsd-verify-work`:** Full suite green + build check
- **Max feedback latency:** ~180s if wheel smoke included

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 32-01-01 | 01 | 1 | PKG-11 | metadata | `grep -q 'readme' pyproject.toml` (after edit) | `LICENSE` | ⬜ pending |
| 32-01-02 | 01 | 1 | PKG-11 | build | `python -m build` | `dist/*.whl` | ⬜ pending |
| 32-01-03 | 01 | 1 | PKG-11 | docs | `grep -q 'twine' docs/RELEASING.md` | `docs/RELEASING.md` | ⬜ pending |
| 32-01-04 | 01 | 1 | PKG-11 | readme | `grep -qi 'pip install' README.md` | `README.md` | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- Existing **`tests/conftest.py`** + **`pytest`** — no new Wave 0 stubs required unless executor adds CI workflow tests.

*Existing infrastructure covers library tests; packaging verified via build/twine.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|---------------------|
| TestPyPI upload | PKG-11 | Needs PyPI token & project registration | Follow **`docs/RELEASING.md`**; confirm install **`pip install -i https://test.pypi.org/simple/ ...`** |
| Production PyPI first upload | PKG-11 | Credentials / name availability | Same doc; optional Trusted Publishing setup |

---

## Validation Sign-Off

- [ ] All tasks have automated verify or manual table above
- [ ] `nyquist_compliant: true` set in frontmatter after execute

**Approval:** pending
