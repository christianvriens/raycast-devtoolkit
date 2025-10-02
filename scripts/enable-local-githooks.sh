#!/usr/bin/env bash
set -euo pipefail

# Configure git to use the repository's .githooks directory
git config core.hooksPath .githooks
echo "Configured git to use .githooks as hooks path"
