#!/usr/bin/env bash
# Run the opt-in wheel smoke test (sets RUN_WHEEL_SMOKE=1).
# Requires Python 3.10+, pytest (e.g. pip install -e ".[dev]"), and network for pip dependency install.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY="${PYTHON:-}"
if [[ -z "$PY" && -x "$ROOT/.venv/bin/python" ]]; then
  PY="$ROOT/.venv/bin/python"
elif [[ -z "$PY" ]]; then
  PY="python3"
fi
export RUN_WHEEL_SMOKE=1
exec "$PY" -m pytest tests/integration/test_wheel_smoke.py -v "$@"
