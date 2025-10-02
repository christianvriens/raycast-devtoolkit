#!/usr/bin/env bash
# Convenience wrapper: update VS Code settings to point to python-tools/.venv
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="$ROOT/scripts/update_vscode_venv.py"
if [ ! -f "$PY" ]; then
  echo "Missing helper script: $PY" >&2
  exit 1
fi

"$(which python3 || true)" "$PY"
