---
status: complete
phase: 31-v1-3-library-workspace-paths
source:
  - 31-SUMMARY.md
  - 31-v1-3-library-workspace-paths-01-SUMMARY.md
started: 2026-03-26T23:00:00Z
updated: 2026-03-26T23:00:00Z
---

## Current Test

[testing complete — milestone closure sign-off]

## Tests

### 1. Library path resolver
expected: `src/trading_crab_lib/paths.py` defines `LibraryPaths` and `resolve_library_paths()`; `__init__.py` exports `ROOT`, `CONFIG_DIR`, `DATA_DIR`, `OUTPUT_DIR` and resolver symbols per 31-SUMMARY.
result: pass

### 2. Unit tests
expected: `tests/unit/test_library_paths.py` present; `pytest tests/unit/test_library_paths.py tests/unit/test_config.py -q` passes (included in full suite).
result: pass

### 3. Import smoke
expected: `python3 -c "import trading_crab_lib as t; print(t.CONFIG_DIR)"` succeeds when run from repo root with package on `PYTHONPATH` / editable install.
result: pass

### 4. README
expected: README documents library-only install / path behavior as described in 31-SUMMARY.
result: pass

### 5. `validate health`
expected: `node .codex/get-shit-done/bin/gsd-tools.cjs validate health` reports `status: healthy`.
result: pass

## Summary

total: 5
passed: 5
issues: 0
pending: 0
skipped: 0

## Gaps

[none]
