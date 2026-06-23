#!/usr/bin/env bash
set -euo pipefail

fail() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

require_file() {
  [ -f "$1" ] || fail "missing required file: $1"
}

require_text() {
  local file="$1"
  local text="$2"
  grep -Fq "$text" "$file" || fail "missing required text in $file: $text"
}

require_file README.md
require_file docs/status/current.md
require_file docs/manifest.md
require_file docs/roadmap.md
require_file docs/commands.md
require_file docs/package-spec.md

require_text README.md "LLM entrypoint"
require_text README.md "tul run"
require_text README.md "tul update"
require_text README.md "git add -A"
require_text README.md "tul-package.yml + files/ + README.md"
require_text README.md "Artifact model"
require_text README.md "Document ownership"

printf 'doc invariants ok\n'
