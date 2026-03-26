---
status: complete
phase: 32-v1-3-pypi-release-engineering
source:
  - 32-SUMMARY.md
  - 32-v1-3-pypi-release-engineering-01-SUMMARY.md
started: 2026-03-26T20:00:00Z
updated: 2026-03-26T21:45:00Z
---

## Current Test

[testing complete — user confirmed all items passed]

## Tests

### 1. Reproducible build (build_dist.sh)
expected: |
  bash scripts/build_dist.sh exits 0; dist/ contains wheel + sdist for trading_crab_lib
result: pass

### 2. Package metadata after editable install
expected: |
  With dev deps installed (pip install -e ".[dev]"), pip show trading-crab-lib lists
  Name, Version, Summary, Home-page (or Project-URL), and License consistent with pyproject/README.
result: pass

### 3. README — PyPI install story
expected: |
  README.md contains section "Install from PyPI" (or equivalent), shows pip install trading-crab-lib,
  and links to docs/RELEASING.md for maintainers or TestPyPI.
result: pass

### 4. RELEASING.md — upload commands
expected: |
  docs/RELEASING.md documents twine upload to TestPyPI and production PyPI, and references
  python -m build / twine check.
result: pass

### 5. LICENSE at repository root
expected: |
  File LICENSE exists at repo root and identifies MIT (or SPDX "MIT") and copyright notice.
result: pass

## Summary

total: 5
passed: 5
issues: 0
pending: 0
skipped: 0

## Gaps

[none]
