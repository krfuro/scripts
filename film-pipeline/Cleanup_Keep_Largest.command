#!/bin/zsh
BASE="$(cd "$(dirname "$0")" && pwd)"
TARGET="$BASE"
set -u
setopt NULL_GLOB

TRASH="$HOME/.Trash"
LOG="$BASE/cleanup_keep_largest_$(date +%Y-%m-%d_%H-%M-%S).log"

# 1 = bare vis hva som skjer, 0 = utfør (flytt til Papirkurv)
DRY_RUN=0

# hvilke filtyper regnes som "video"
VIDEO_EXT_RE='\.((mkv)|(mp4)|(m4v)|(avi)|(mov)|(m2ts)|(ts)|(vob))$'

touch "$LOG"

log() { echo "$@" | tee -a "$LOG"; }

log "======================================"
log " Cleanup: behold største VIDEO-fil per mappe"
log " Base: $BASE"
log " Mode: $( [ "$DRY_RUN" -eq 1 ] && echo 'DRY RUN' || echo 'EXECUTE (to Trash)' )"
log " Logg: $LOG"
log "======================================"
log ""

# Gå gjennom alle toppnivå-mapper i BASE
for dir in "$BASE"/*; do
  [[ -d "$dir" ]] || continue

  log "--------------------------------------"
  log "Mappe: $(basename "$dir")"

  # Ikke la én feil stoppe alt
  {
    # Fjern .DS_Store
    if [ "$DRY_RUN" -eq 1 ]; then
      find "$dir" -type f -name ".DS_Store" -print | sed 's/^/  (ville slettet) /' | tee -a "$LOG" >/dev/null || true
    else
      find "$dir" -type f -name ".DS_Store" -delete || true
    fi

    # Finn største VIDEO-fil (rekursivt)
    largest_path=""
    largest_size=-1

    while IFS= read -r -d '' f; do
      bn="$(basename "$f")"
      [[ "$bn" == ".DS_Store" ]] && continue
      # kun video
      echo "$f" | grep -Eiq "$VIDEO_EXT_RE" || continue
      size=$(stat -f%z "$f" 2>/dev/null || echo 0)
      if (( size > largest_size )); then
        largest_size=$size
        largest_path="$f"
      fi
    done < <(find "$dir" -type f -print0)

    # Hvis ingen video funnet: behold største fil uansett
    if [[ -z "$largest_path" ]]; then
      while IFS= read -r -d '' f; do
        bn="$(basename "$f")"
        [[ "$bn" == ".DS_Store" ]] && continue
        size=$(stat -f%z "$f" 2>/dev/null || echo 0)
        if (( size > largest_size )); then
          largest_size=$size
          largest_path="$f"
        fi
      done < <(find "$dir" -type f -print0)
    fi

    if [[ -z "$largest_path" ]]; then
      log "  Ingen filer funnet."
      return 0
    fi

    log "  Beholder: $(basename "$largest_path")  (${largest_size} bytes)"

    moved=0
    # Flytt ALT annet (rekursivt) til Trash
    while IFS= read -r -d '' f; do
      [[ "$f" == "$largest_path" ]] && continue
      bn="$(basename "$f")"
      [[ "$bn" == ".DS_Store" ]] && continue

      dest="$TRASH/$bn"
      # unngå kollisjon i Trash
      [[ -e "$dest" ]] && dest="$TRASH/${bn}_$(date +%s)"

      if [ "$DRY_RUN" -eq 1 ]; then
        log "  (ville flyttet til Trash) $bn"
      else
        mv "$f" "$dest" 2>/dev/null || {
          log "  FEIL: klarte ikke flytte: $f"
          continue
        }
        ((moved++))
      fi
    done < <(find "$dir" -type f -print0)

    # Slett tomme mapper (inkl. tomme undermapper)
    if [ "$DRY_RUN" -eq 0 ]; then
      find "$dir" -type d -empty -delete 2>/dev/null || true
    fi

    log "  Antall filer flyttet: $moved"
  } || {
    log "  FEIL i denne mappa – fortsetter til neste."
  }
done

log ""
log "Ferdig."
log ""

if [ "$DRY_RUN" -eq 1 ]; then
  log "OBS: Dette var DRY RUN. Sett DRY_RUN=0 for å utføre."
fi

echo -n "Trykk Enter for å lukke..."
read -r
