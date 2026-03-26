#!/usr/bin/env bash
# Run Ruff check + format --check. Resolution order:
#   1. `ruff` on PATH (pipx, global pip, or export PATH="$PWD/.venv/bin:$PATH")
#   2. $PYTHON if set (e.g. make PYTHON=... lint)
#   3. Repo .venv (after `make setup-dev` — ruff is in requirements-dev.txt)
#   4. python3 -m ruff
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

run_ruff_exe() {
  local exe="$1"
  shift
  "$exe" check src tests run_pipeline.py pipelines scripts
  "$exe" format --check src tests run_pipeline.py pipelines scripts
}

run_ruff_module() {
  local py="$1"
  "$py" -m ruff check src tests run_pipeline.py pipelines scripts
  "$py" -m ruff format --check src tests run_pipeline.py pipelines scripts
}

py_has_ruff() {
  local py="$1"
  [[ -n "$py" ]] || return 1
  if [[ -x "$py" ]]; then
    "$py" -m ruff --version >/dev/null 2>&1
  else
    command -v "$py" >/dev/null 2>&1 && "$py" -m ruff --version >/dev/null 2>&1
  fi
}

if command -v ruff >/dev/null 2>&1; then
  run_ruff_exe ruff
  exit 0
fi

if [[ -n "${PYTHON:-}" ]] && py_has_ruff "$PYTHON"; then
  run_ruff_module "$PYTHON"
  exit 0
fi

VENV_PY="$REPO_ROOT/.venv/bin/python"
if [[ -x "$VENV_PY" ]] && py_has_ruff "$VENV_PY"; then
  run_ruff_module "$VENV_PY"
  exit 0
fi

if py_has_ruff python3; then
  run_ruff_module python3
  exit 0
fi

echo "ERROR: Ruff not found. Install it in your environment, e.g.:" >&2
echo "  pip install ruff          # or: pip install -r requirements-dev.txt" >&2
echo "  pipx install ruff         # puts ruff on PATH" >&2
echo "  make setup-dev            # creates .venv with ruff" >&2
echo "  export PATH=\"\$PWD/.venv/bin:\$PATH\"   # so bare 'ruff' resolves" >&2
exit 1
