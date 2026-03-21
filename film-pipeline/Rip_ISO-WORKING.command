#!/bin/zsh
BASE="$(cd "$(dirname "$0")" && pwd)"
TARGET="$BASE"
set -euo pipefail
setopt NULL_GLOB

DIR="/Users/krfuro/Movies/backup"
OUTBASE="$DIR/RIPS"
LOG="$DIR/makemkv_$(date +%Y-%m-%d_%H-%M-%S).log"

# Bruk alltid full sti (slipper PATH-trøbbel ved dobbelklikk)
MAKEMKV="/Applications/MakeMKV.app/Contents/MacOS/makemkvcon"

cd "$DIR"
mkdir -p "$OUTBASE"
touch "$LOG"

# Logg ALT til fil + terminal
exec > >(tee -a "$LOG") 2>&1

echo "======================================"
echo " MakeMKV ISO → MKV batch"
echo " ISO-mappe:  $DIR"
echo " Output:     $OUTBASE"
echo " Logg:       $LOG"
echo "======================================"
echo ""

# Verifiser at makemkvcon finnes
if [[ ! -x "$MAKEMKV" ]]; then
  echo "FEIL: Fant ikke makemkvcon her:"
  echo "  $MAKEMKV"
  echo ""
  echo "Sjekk at MakeMKV er installert i /Applications."
  echo -n "Trykk Enter for å avslutte..."
  read -r
  exit 1
fi

isos=( *.iso *.ISO )
if (( ${#isos[@]} == 0 )); then
  echo "Fant ingen ISO-filer i $DIR"
  echo -n "Trykk Enter for å avslutte..."
  read -r
  exit 0
fi

for iso in "${isos[@]}"; do
  name="${iso%.*}"
  out="$OUTBASE/$name"

  echo "--------------------------------------"
  echo "ISO: $iso"
  echo "Ut:  $out"
  echo "Tid: $(date)"
  echo ""

  mkdir -p "$out"

  echo "Starter ripping..."
  echo "Kommando: $MAKEMKV -r --progress=-same --minlength=120 --decrypt mkv \"iso:$DIR/$iso\" all \"$out\""
  echo ""

  "$MAKEMKV" -r --progress=-same --minlength=120 --decrypt mkv "iso:$DIR/$iso" all "$out"

  echo ""
  if ls "$out"/*.mkv >/dev/null 2>&1; then
    echo "OK: MKV laget i $out"
  else
    echo "FEIL: Ingen MKV ble laget for $iso"
    echo "Sjekk loggen: $LOG"
    echo "Tips: Prøv å kjøre:"
    echo "  $MAKEMKV info \"iso:$DIR/$iso\""
  fi
  echo ""
done

echo "======================================"
echo " ALLE ISO-FILER FERDIG"
echo "======================================"
echo ""
echo "Logg lagret i:"
echo "  $LOG"
echo ""
echo -n "Trykk Enter for å lukke..."
read -r
exit 0
