---
phase: 2
slug: regime-clustering-interpretation
status: draft
nyquist_compliant: false
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
| 02-01-01 | 01   | 1    | REGIME-01       | unit      | `pytest tests/unit/test_clustering.py -q`                      | ✅ | ✅ green (manifest/skip manual-only) |
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
| Clustering manifest + skip-on-unchanged policy (Plan 01 full spec) | REGIME-01 | `build_clustering_manifest` and pipeline `--force`/skip logic not implemented; Plan 01 SUMMARY reflected an earlier scope (tests only). | Implement `build_clustering_manifest()` in `clustering.py`, wire manifest read/compare and `--force` in `pipelines/03_cluster.py`, add unit tests for manifest determinism/sensitivity; then run `pytest tests/unit/test_clustering.py -q` and second-run skip. |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [ ] `nyquist_compliant: false` set in frontmatter

**Approval:** pending

---

## Validation Audit 2026-03-18

| Metric | Count |
|--------|-------|
| Gaps found | 2 |
| Resolved | 0 |
| Escalated to manual-only | 2 |

:**Gap (REGIME-03 Hybrid Pinning):** Phase 2 Plan 02 requires hybrid naming governance (at least one regime intentionally left unpinned so auto-suggestions remain visible). Current `config/regime_labels.yaml` pins all balanced-cluster IDs implied by `config/settings.yaml` (`balanced_k: 5` => IDs 0..4), so there may be no unpinned regime IDs remaining for human review via auto-suggestions. This is a configuration/governance gap (detectable via tests, but not resolvable without editing the override map).

**Gap:** Plan 01 full spec requires `build_clustering_manifest()` and pipeline skip-when-unchanged (with `--force`). Codebase has no manifest or skip logic; Plan 01 was previously executed with tests-only scope (see 02-regime-clustering-interpretation-01-SUMMARY.md). REGIME-01 clustering math and artifact shape are covered by `test_clustering.py`; manifest/skip coverage is missing until implementation exists. Escalated to Manual-Only with implementation instructions above.

