#!/usr/bin/env bash
# Initialize and update all git submodules to the commits recorded in this repo.
# Run from repo root: bash scripts/sync_submodules.sh
# Used by `make submodules`, `make setup`, and recommended before local work/CI.
#
# Requires: git, network access to submodule remotes (GitHub).
# Skip: SKIP_SUBMODULE_SYNC=1 (e.g. offline or no submodule access)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if [[ "${SKIP_SUBMODULE_SYNC:-}" == "1" ]]; then
  echo "SKIP_SUBMODULE_SYNC=1 — skipping git submodule update"
  exit 0
fi

if [[ ! -d .git ]]; then
  echo "No .git directory — skipping submodule sync"
  exit 0
fi

if [[ ! -f .gitmodules ]]; then
  echo "No .gitmodules — skipping submodule sync"
  exit 0
fi

git submodule sync --recursive
git submodule update --init --recursive --jobs 4
