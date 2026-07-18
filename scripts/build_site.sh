#!/usr/bin/env bash
# Builds the full site locally, exactly like the GitHub Actions workflow
# does. Useful for previewing the whole tabbed site (including the
# compiled Snake game) before pushing.
#
# Requires: pip install pygbag
#
# Usage:
#   ./scripts/build_site.sh
#   python -m http.server 8000 --directory site
#   # then visit http://localhost:8000

set -euo pipefail
cd "$(dirname "$0")/.."

echo "Building Snake (Python -> WebAssembly)..."
python -m pygbag --build games/snake/main.py

echo "Assembling site/ ..."
rm -rf site
mkdir -p site/games/snake site/games/tictactoe
cp index.html style.css script.js site/
cp -r games/snake/build/web/* site/games/snake/
cp -r games/tictactoe/* site/games/tictactoe/

echo "Done. Site assembled in ./site"
echo "Preview it with: python -m http.server 8000 --directory site"
