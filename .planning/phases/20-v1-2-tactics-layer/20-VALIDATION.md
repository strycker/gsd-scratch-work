---
phase: 20
slug: v1-2-tactics-layer
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-22
updated: 2026-03-23
---

# Phase 20 — Validation Strategy

> Per-phase validation contract for TACTICS-10 (tactics classification enrichment).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | `pyproject.toml` |
| **Quick run command** | `PYTHONPATH=src python3 -m pytest tests/test_tactics.py -q` |
| **Full suite command** | `PYTHONPATH=src python3 -m pytest tests/ -q` |
| **Estimated runtime** | ~30–120 seconds (full suite) |

---

## Sampling Rate

- **After every task commit:** Run `python3 -m pytest tests/test_tactics.py -q` (with `PYTHONPATH=src`)
- **Before merge:** Full suite green
- **Max feedback latency:** &lt; 2 min for tactics-only

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 20-01-01 | 01 | 1 | TACTICS-10 | unit | `PYTHONPATH=src python3 -m pytest tests/test_tactics.py::test_tactics_classification_basic -q` | ✅ | ✅ green |
| 20-01-02 | 01 | 1 | TACTICS-10 | unit | same file: `as_of` / `quarter_end` / `last_price` in `test_tactics_classification_basic` | ✅ | ✅ green |
| 20-01-03 | 01 | 1 | TACTICS-10 | unit | `test_entry_bias_score_in_unit_interval` + `soft_stop_z` in basic | ✅ | ✅ green |
| 20-01-04 | 01 | 1 | TACTICS-10 | doc | `grep -qi tactics RUNBOOK.md` (step 9 + extended pipeline) | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red*

---

## Wave 0 Requirements

- `tests/test_tactics.py` covers classification, snapshot columns, entry bias bounds, v1 vs v1_2, `min_corr_spy`.
- No new framework install.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Step 9 end-to-end on real ETF parquet | TACTICS-10 | Real data size / paths | After steps 3+6, `python run_pipeline.py --steps 9`; open `tactics_signals.parquet` |

*Optional smoke; unit tests cover core logic.*

---

## Validation Sign-Off

- [x] All tasks have automated verify or manual table above
- [x] `python3 -m pytest tests/test_tactics.py` green (`PYTHONPATH=src`)
- [x] `nyquist_compliant: true` when wave complete

**Approval:** 2026-03-23 — Nyquist retro-validation complete

---

## Validation Audit 2026-03-23

| Metric | Count |
|--------|-------|
| Gaps found | 0 (VALIDATION was draft; tests + RUNBOOK already satisfied TACTICS-10) |
| Resolved | 4 tasks mapped to ✅ |
| Escalated | 0 |

**Evidence:** `PYTHONPATH=src python3 -m pytest tests/test_tactics.py -q` → 4 passed.
