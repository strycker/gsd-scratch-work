---
phase: 20
slug: v1-2-tactics-layer
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-22
---

# Phase 20 — Validation Strategy

> Per-phase validation contract for TACTICS-10 (tactics classification enrichment).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | `pyproject.toml` |
| **Quick run command** | `PYTHONPATH=src python -m pytest tests/test_tactics.py -q` |
| **Full suite command** | `PYTHONPATH=src python -m pytest tests/ -q` |
| **Estimated runtime** | ~30–120 seconds (full suite) |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/test_tactics.py -q`
- **Before merge:** Full suite green
- **Max feedback latency:** &lt; 2 min for tactics-only

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 20-01-01 | 01 | 1 | TACTICS-10 | unit | `pytest tests/test_tactics.py -q` | ⬜ W0 | ⬜ pending |
| 20-01-02 | 01 | 1 | TACTICS-10 | unit | same + grep `as_of` in tactics.py | ⬜ | ⬜ pending |
| 20-01-03 | 01 | 1 | TACTICS-10 | unit | `grep -q entry_bias` or column test | ⬜ | ⬜ pending |
| 20-01-04 | 01 | 1 | TACTICS-10 | doc | `grep TACTICS-10 RUNBOOK.md` | ⬜ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red*

---

## Wave 0 Requirements

- Existing `tests/test_tactics.py` covers baseline classification — extend for Phase 20 columns/rules.
- No new framework install.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Step 9 end-to-end on real ETF parquet | TACTICS-10 | Real data size / paths | After steps 3+6, `python run_pipeline.py --steps 9`; open `tactics_signals.parquet` |

*If all behaviors have unit coverage of logic, manual row is optional.*

---

## Validation Sign-Off

- [ ] All tasks have automated verify or manual table above
- [ ] `pytest tests/test_tactics.py` is green before phase verify-phase
- [ ] `nyquist_compliant: true` set when wave complete

**Approval:** pending
