#!/bin/zsh
BASE="$(cd "$(dirname "$0")" && pwd)"
TARGET="$BASE"
set -e

cd "$(dirname "$0")"

echo "======================================"
echo " FLATTEN RIPS"
echo " Flytter MKV-filer + rydder mapper"
echo "======================================"
echo ""

echo "Fjerner macOS-skrot (.DS_Store)..."
find . -type f -name ".DS_Store" -delete

echo "Flytter MKV-filer ut av undermapper..."
find . -mindepth 2 -type f -name "*.mkv" -exec mv -n {} . \;

echo "Fjerner tomme mapper..."
find . -type d -empty -delete

echo ""
echo "Ferdig."
echo ""
echo -n "Trykk Enter for å lukke..."
read -r
