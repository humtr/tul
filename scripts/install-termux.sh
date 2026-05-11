#!/usr/bin/env bash
set -euo pipefail
REPO="${1:-$HOME/prj/tul}"
python "$REPO/bin/tul" install "$REPO"
