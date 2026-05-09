#!/usr/bin/env bash
# refresh.sh — regenerate the orchestration-agent-context mirror.
#
# Module purpose:
#   Thin shell wrapper around scripts/generate.py. The shell layer:
#     - validates the toolchain (git, jq, python3),
#     - cleans regenerable outputs (chunks/, generated/, generated *.md),
#     - hands off to scripts/generate.py for the actual indexing/chunking/scan,
#     - optionally prints `git status --short` at the end.
#
# Process flow:
#   1. require_bin checks
#   2. clean regenerable outputs (hand-curated docs are NOT touched)
#   3. invoke scripts/generate.py
#   4. show git status
#
# This script is intentionally short. The real work lives in scripts/generate.py
# so it can run cross-platform (macOS bash 3.2 lacks mapfile etc.).
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

require_bin() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "refresh.sh: missing required tool: $1" >&2
    exit 2
  fi
}
require_bin git
require_bin python3

# --- step 1: clean regenerable outputs ------------------------------------
# Hand-curated docs (00-boundary.md, integration/*, AGENTS.md, README.md,
# tasks/*, scripts/*) are intentionally left in place.
echo "refresh.sh: cleaning regenerable outputs"
rm -rf "$ROOT_DIR/xlotyl/chunks" "$ROOT_DIR/stoneforge/chunks"
rm -f  "$ROOT_DIR/xlotyl/01-repo-map.md" \
       "$ROOT_DIR/xlotyl/03-symbol-index.md"
rm -f  "$ROOT_DIR/stoneforge/01-repo-map.md" \
       "$ROOT_DIR/stoneforge/03-symbol-index.md"
# Wipe and recreate generated/. FRESHNESS.md lives there too so it's
# always rewritten with the new manifest.
rm -rf "$ROOT_DIR/generated"
mkdir -p "$ROOT_DIR/generated" \
         "$ROOT_DIR/xlotyl/chunks" \
         "$ROOT_DIR/stoneforge/chunks"

# --- step 2: hand off to the Python generator -----------------------------
echo "refresh.sh: running scripts/generate.py"
python3 "$ROOT_DIR/scripts/generate.py"

# --- step 3: optional git status -------------------------------------------
if [[ -d "$ROOT_DIR/.git" ]]; then
  echo "refresh.sh: git status (short)"
  git -C "$ROOT_DIR" status --short || true
fi

echo "refresh.sh: review generated/source-manifest.json before committing."
