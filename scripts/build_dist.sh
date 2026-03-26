#!/usr/bin/env bash
# Reproducible sdist + wheel for trading-crab-lib (PEP 517).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY="${PYTHON:-}"
if [[ -z "$PY" && -x "$ROOT/.venv/bin/python" ]]; then
  PY="$ROOT/.venv/bin/python"
elif [[ -z "$PY" ]]; then
  PY="python3"
fi
rm -rf dist/ build/
"$PY" -m build
"$PY" -m twine check dist/*
echo "dist/:"
ls -la dist/
echo "build_dist: OK"
