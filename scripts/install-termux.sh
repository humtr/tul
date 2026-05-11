#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-$HOME/prj/tul}"
DEST="${TUL_BIN_DEST:-$HOME/bin/tul}"
LIB_DEST="${TUL_LIB_DEST:-$HOME/.config/tul/lib}"

cd "$REPO"
python -m py_compile bin/tul
python -m py_compile lib/tulcore/*.py

mkdir -p "$(dirname "$DEST")" "$LIB_DEST"
cp -f bin/tul "$DEST"
chmod +x "$DEST"
rm -rf "$LIB_DEST/tulcore"
cp -a lib/tulcore "$LIB_DEST/"

echo "Installed tul:"
echo "  $DEST"
echo "  $LIB_DEST/tulcore"
