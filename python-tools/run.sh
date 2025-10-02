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
# Install project requirements; allow failure to avoid blocking when offline
"$V_PIP" install -r "$REQ" || true

# If the first argument is 'test', install dev requirements and run pytest
if [ "${1-}" = "test" ]; then
  # Install development/test requirements
  DEV_REQ="$TOOLS_DIR/requirements-dev.txt"
  if [ -f "$DEV_REQ" ]; then
    "$V_PIP" install -r "$DEV_REQ" || true
  else
    # Fallback: install pytest directly
    "$V_PIP" install pytest -q || true
  fi

  shift || true
  exec "$V_PY" -m pytest -q "$TOOLS_DIR/tests" "$@"
fi

# Otherwise run the CLI with all args passed through
exec "$V_PY" "$TOOLS_DIR/devtools.py" "$@"
