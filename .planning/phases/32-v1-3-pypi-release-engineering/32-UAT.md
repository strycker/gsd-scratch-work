---
status: testing
phase: 32-v1-3-pypi-release-engineering
source:
  - 32-SUMMARY.md
  - 32-v1-3-pypi-release-engineering-01-SUMMARY.md
started: 2026-03-26T20:00:00Z
updated: 2026-03-26T20:00:00Z
---

## Current Test

number: 1
name: Reproducible build (build_dist.sh)
expected: |
  From the repository root, run: bash scripts/build_dist.sh
  The script exits with status 0. Directory dist/ contains at least one .whl and one .tar.gz
  for trading_crab_lib (names may include trading_crab_lib-0.1.0-...).
awaiting: user response

## Tests

### 1. Reproducible build (build_dist.sh)
expected: |
  bash scripts/build_dist.sh exits 0; dist/ contains wheel + sdist for trading_crab_lib
result: [pending]

### 2. Package metadata after editable install
expected: |
  With dev deps installed (pip install -e ".[dev]"), pip show trading-crab-lib lists
  Name, Version, Summary, Home-page (or Project-URL), and License consistent with pyproject/README.
result: [pending]

### 3. README — PyPI install story
expected: |
  README.md contains section "Install from PyPI" (or equivalent), shows pip install trading-crab-lib,
  and links to docs/RELEASING.md for maintainers or TestPyPI.
result: [pending]

### 4. RELEASING.md — upload commands
expected: |
  docs/RELEASING.md documents twine upload to TestPyPI and production PyPI, and references
  python -m build / twine check.
result: [pending]

### 5. LICENSE at repository root
expected: |
  File LICENSE exists at repo root and identifies MIT (or SPDX "MIT") and copyright notice.
result: [pending]

## Summary

total: 5
passed: 0
issues: 0
pending: 5
skipped: 0

## Gaps

<!-- Populated when a test result is "issue" -->
