#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)/.."
TOOLS_DIR="$ROOT/python-tools"
VENV_DIR="$TOOLS_DIR/.venv"
REQ="$TOOLS_DIR/requirements.txt"

# Create venv if missing
if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi

# Use the venv's python/pip
V_PY="$VENV_DIR/bin/python"
V_PIP="$VENV_DIR/bin/pip"

# Upgrade pip and install requirements (idempotent)
"$V_PY" -m pip install --upgrade pip setuptools wheel
"$V_PIP" install -r "$REQ"

# Run the CLI with all args passed through
exec "$V_PY" "$TOOLS_DIR/devtools.py" "$@"
