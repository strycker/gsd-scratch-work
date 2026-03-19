---
phase: 2
slug: regime-clustering-interpretation
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-16
---

# Phase 2 — Validation Strategy

> Per-phase validation contract for clustering, profiling, and naming behavior.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.x |
| **Config file** | pyproject.toml |
| **Quick run command** | `pytest tests/unit/test_clustering.py tests/unit/test_regime.py tests/unit/test_forward_window_probabilities.py -q` |
| **Full suite command** | `pytest -q` |
| **Estimated runtime** | ~60 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/unit/test_clustering.py tests/unit/test_regime.py -q`
- **After every plan wave:** Run `pytest tests/unit/test_clustering.py tests/unit/test_regime.py -q`
- **Before `$gsd-verify-work`:** Full suite (`pytest -q`) must be green
- **Max feedback latency:** 60 seconds

---

## Per-Task Verification Map

| Task ID  | Plan | Wave | Requirement     | Test Type | Automated Command                                              | File Exists | Status  |
|----------|------|------|-----------------|-----------|----------------------------------------------------------------|------------|---------|
| 02-01-01 | 01   | 1    | REGIME-01       | unit      | `pytest tests/unit/test_clustering.py tests/unit/test_pipeline_03_cluster_manifest.py -q` | ✅ | ✅ green |
| 02-02-01 | 02   | 2    | REGIME-02, REGIME-03 | unit  | `pytest tests/unit/test_regime.py -q`                          | ✅ | ✅ green |
| 02-03-01 | 03   | 3    | REGIME-02, REGIME-03 | unit  | `pytest tests/unit/test_forward_window_probabilities.py -q`     | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `tests/unit/test_clustering.py` — unit tests for PCA + KMeans clustering, artifact creation under `data/regimes/`.
- [x] `tests/unit/test_regime.py` — unit tests for regime profiles, naming, and transition matrices driven by `regime_labels.yaml`.
- [x] `tests/unit/test_forward_window_probabilities.py` — unit tests for forward-window probability semantics and determinism.

---

## Manual-Only Verifications

| Behavior                                      | Requirement | Why Manual                                     | Test Instructions |
|-----------------------------------------------|------------|-----------------------------------------------|-------------------|
| Visual inspection of regime profiles and clustering stability across reruns | REGIME-01, REGIME-02 | Requires notebook/plot-based inspection        | Run `python pipelines/03_cluster.py` and `python pipelines/04_regime_label.py`, then inspect relevant notebooks/plots. |
| Visual inspection of dashboard naming and pinned override semantics | REGIME-03 | Requires end-to-end artifact generation from real data | Run `python pipelines/04_regime_label.py` then `python pipelines/07_dashboard.py` and verify at least one unpinned regime uses an auto-suggested name while pinned IDs override. |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending

---

## Validation Audit 2026-03-18

| Metric | Count |
|--------|-------|
| Gaps found | 2 |
| Resolved | 2 |
| Escalated to manual-only | 0 |

**Resolved (REGIME-03 Hybrid Pinning):**
- `config/regime_labels.yaml` intentionally leaves at least one ID unpinned (e.g. ID 4).
- Dashboard loader merges auto-suggestions with pinned overrides so unpinned IDs still have names.
- Automated: `pytest tests/unit/test_hybrid_naming_dashboard.py -q`

**Resolved (REGIME-01 Manifest + Skip/Force):**
- `build_clustering_manifest()` exists in `src/market_regime/clustering.py`.
- `pipelines/03_cluster.py` writes/compares `data/regimes/clustering_manifest.json`, skips on match, and supports `--force`.
- Automated: `pytest tests/unit/test_pipeline_03_cluster_manifest.py -q` (covers skip-on-match and `--force` override).

