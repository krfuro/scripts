#!/bin/zsh
set -u
setopt NULL_GLOB

BASE="$(cd "$(dirname "$0")" && pwd)"
TARGET="$BASE"

OUT="$TARGET/ENCODED"
mkdir -p "$OUT"

LOG="$TARGET/handbrake_$(date +%Y-%m-%d_%H-%M-%S).log"

PRESET="MakeMKV_to_Plex_AllTracks"

echo "======================================" | tee -a "$LOG"
echo " HandBrake batch: MKV -> MP4" | tee -a "$LOG"
echo " Mappe:   $TARGET" | tee -a "$LOG"
echo " Output:  $OUT" | tee -a "$LOG"
echo " Preset:  $PRESET" | tee -a "$LOG"
echo " Logg:    $LOG" | tee -a "$LOG"
echo "======================================" | tee -a "$LOG"
echo "" | tee -a "$LOG"

# Sjekk at HandBrakeCLI finnes
if ! command -v HandBrakeCLI >/dev/null 2>&1; then
  echo "FEIL: HandBrakeCLI ikke funnet i PATH." | tee -a "$LOG"
  echo "Tips: Installer HandBrake (og/eller legg HandBrakeCLI i PATH)." | tee -a "$LOG"
  echo -n "Trykk Enter for å lukke..."
  read -r
  exit 1
fi

# Sjekk at preset finnes
if ! HandBrakeCLI --preset-list 2>&1 | grep -Fq "$PRESET"; then
  echo "FEIL: Finner ikke preset: $PRESET" | tee -a "$LOG"
  echo "Åpne HandBrake GUI -> lagre presetet med nøyaktig samme navn." | tee -a "$LOG"
  echo -n "Trykk Enter for å lukke..."
  read -r
  exit 1
fi

# Finn filer
files=("$TARGET"/*.mkv)
if (( ${#files[@]} == 0 )); then
  echo "Ingen MKV-filer funnet i mappa." | tee -a "$LOG"
  echo -n "Trykk Enter for å lukke..."
  read -r
  exit 0
fi

total=${#files[@]}
idx=0
converted=0
skipped=0

for in in "${files[@]}"; do
  ((idx++))
  bn="$(basename "$in")"
  out="$OUT/${bn%.mkv}.mp4"

  echo "--------------------------------------" | tee -a "$LOG"
  echo "[$idx/$total] $bn" | tee -a "$LOG"
  echo "Ut: $(basename "$out")" | tee -a "$LOG"

  if [[ -e "$out" ]]; then
    echo "SKIP: finnes allerede" | tee -a "$LOG"
    ((skipped++))
    continue
  fi

  # Kjør HandBrake
  # (HandBrakeCLI viser egen progresjon i terminalen)
  if HandBrakeCLI -i "$in" -o "$out" --preset "$PRESET" 2>&1 | tee -a "$LOG"; then
    echo "OK: ferdig" | tee -a "$LOG"
    ((converted++))
  else
    echo "FEIL: HandBrake feilet for $bn" | tee -a "$LOG"
  fi
done

echo "" | tee -a "$LOG"
echo "======================================" | tee -a "$LOG"
echo " FERDIG" | tee -a "$LOG"
echo " Konvertert: $converted" | tee -a "$LOG"
echo " Skippet:    $skipped" | tee -a "$LOG"
echo " Logg:       $LOG" | tee -a "$LOG"
echo "======================================" | tee -a "$LOG"
echo -n "Trykk Enter for å lukke..."
read -r
