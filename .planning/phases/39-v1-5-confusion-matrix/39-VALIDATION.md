---
phase: 39
slug: v1-5-confusion-matrix
status: complete
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-26
updated: 2026-03-26
---

# Phase 39 — Validation Strategy (Nyquist)

> Validation contract for **TMPL-03** (confusion matrix visualization). Reconstructed in **State B** (no prior `*-VALIDATION.md`; **39-01-SUMMARY.md** present).

---

## Test infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (via `pyproject.toml`) |
| **Config file** | `pyproject.toml` (`[tool.pytest.ini_options]`) |
| **Quick run command** | `python3 -m pytest tests/unit/test_plot_confusion_matrix.py -q` |
| **Full suite command** | `python3 -m pytest tests/ -q` |
| **Estimated runtime** | ~3–5 s (file only); full suite ~minutes |

---

## Sampling rate

- **After task-level changes:** `pytest tests/unit/test_plot_confusion_matrix.py -q`
- **Before milestone audit:** Full suite green per project CI / `make lint` as applicable

---

## Per-task verification map

| Task ID | Plan | Wave | Requirement | Test type | Automated command | Status |
|---------|------|------|-------------|-----------|---------------------|--------|
| 39-01-01 | 01 | 1 | TMPL-03 — heatmap + parquet contract | unit | `pytest tests/unit/test_plot_confusion_matrix.py -q` | ✅ green |
| 39-01-02 | 01 | 1 | TMPL-03 — `run_pipeline` + `05_predict` wiring | unit (static source) | same file: `test_run_pipeline_step5_wires_confusion_plot`, `test_standalone_predict_script_supports_confusion_plot` | ✅ green |
| 39-01-03 | 01 | 1 | TMPL-03 — docs / backlog strings | manual / review | Goal-backward: **39-VERIFICATION.md**; no pytest for prose | ✅ satisfied (verification report) |

---

## Wave 0 requirements

- [x] Existing pytest + `tests/unit/test_plot_confusion_matrix.py` covers phase behaviors.
- [x] No new framework install required.

---

## Manual-only verifications

| Behavior | Requirement | Why manual | Test instructions |
|----------|-------------|------------|---------------------|
| PNG appearance (heatmap readability) | TMPL-03 | Pixel/layout QA | After `run_pipeline.py --steps 5 --plots` or `pipelines/05_predict.py --plots`, open `outputs/plots/05_confusion_matrix.png`. |

---

## Validation sign-off

- [x] All tasks have automated verification **or** documented manual-only with instructions
- [x] `tests/unit/test_plot_confusion_matrix.py` exercises plot smoke, aggregation contract, horizon filter, and static wiring
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-03-26 (validate-phase reconstruction + test strengthening)

---

## Validation audit — 2026-03-26

| Metric | Count |
|--------|-------|
| Gaps found | 0 (post-hoc: aggregation + wiring tests added during validate-phase) |
| Resolved | 5 tests in `test_plot_confusion_matrix.py` |
| Escalated | 0 |

**Note:** `gsd-tools verify artifacts` did not parse PLAN `must_haves.artifacts` YAML shape for phase 39; coverage confirmed manually and via **39-VERIFICATION.md**.
