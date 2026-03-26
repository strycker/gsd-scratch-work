---
phase: 11-core-cleanup
plan: 01
type: retrospective
wave: 1
depends_on: []
files_modified: []
autonomous: false
requirements:
  - CORE-01
  - CORE-02
user_setup: []
must_haves:
  truths:
    - "Brownfield closure: data/outputs trees, end_date null, imports; evidence in VERIFICATION."
---

# Plan 01 — Phase 11 brownfield PLAN/SUMMARY closure

**Objective:** GSD **Complete** via retrospective PLAN/SUMMARY.

**As-built:** `scripts/setup.sh` scaffold, `end_date` null handling, `test_end_date_null_fallback.py` — **README.md**, **11-core-cleanup-VERIFICATION.md**.
