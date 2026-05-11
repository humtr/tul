#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-$HOME/prj/tul}"
REPO="$(cd "$REPO" && pwd)"
TUL="$REPO/bin/tul"

mkdir -p "$HOME/bin"
cat > "$HOME/bin/tul" <<EOF
#!/usr/bin/env bash
exec python "$TUL" "\$@"
EOF
chmod +x "$HOME/bin/tul"
chmod +x "$TUL"

echo "Installed tul launcher at $HOME/bin/tul"
echo "Next:"
echo "  cd $REPO"
echo "  tul status ."
