#!/usr/bin/env bash
# Run the opt-in pipeline step01 ingest smoke test (sets RUN_PIPELINE_INGEST_SMOKE=1).
# Slow: loads pipelines/01_ingest.py and exercises main() with mocked FRED/multpl.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PY="${PYTHON:-python3}"
export RUN_PIPELINE_INGEST_SMOKE=1
exec "$PY" -m pytest \
  tests/test_pipelines_ingest_features.py::test_step01_ingest_writes_macro_raw_without_network \
  -v "$@"
