#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-$HOME/prj/tul}"
DEST="${TUL_BIN_DEST:-$HOME/bin/tul}"

if [ ! -f "$REPO/bin/tul" ]; then
  echo "ERROR: missing $REPO/bin/tul" >&2
  exit 1
fi

mkdir -p "$(dirname "$DEST")"
cp -f "$REPO/bin/tul" "$DEST"
chmod +x "$DEST"

echo "Installed:"
echo "  $DEST"
echo
echo "Run:"
echo "  tul status $REPO"
