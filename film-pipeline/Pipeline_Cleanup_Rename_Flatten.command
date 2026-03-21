#!/bin/zsh
set -u
setopt NULL_GLOB

BASE="$(cd "$(dirname "$0")" && pwd)"
TRASH="$HOME/.Trash"
LOG="$BASE/pipeline_$(date +%Y-%m-%d_%H-%M-%S).log"

# 1 = bare vis hva som vil skje, 0 = utfør
DRY_RUN=0

VIDEO_EXT_RE='\.((mkv)|(mp4)|(m4v)|(avi)|(mov)|(m2ts)|(ts)|(vob))$'

touch "$LOG"
log(){ echo "$@" | tee -a "$LOG"; }

fmt_gib(){
  python3 - <<PY 2>/dev/null
b=int($1)
print(f"{b/(1024**3):.2f} GiB")
PY
}

pause_with_summary(){
  local title="$1"
  shift
  log ""
  log "=================="
  log "$title"
  log "=================="
  while (( $# )); do
    log "$1"
    shift
  done
  log ""
  echo -n "Trykk Enter for å fortsette..."
  read -r
  echo ""
}

pick_largest_video_in_dir(){
  local dir="$1"
  local largest_path=""
  local largest_size=-1

  while IFS= read -r -d '' f; do
    echo "$f" | grep -Eiq "$VIDEO_EXT_RE" || continue
    size=$(stat -f%z "$f" 2>/dev/null || echo 0)
    if (( size > largest_size )); then
      largest_size=$size
      largest_path="$f"
    fi
  done < <(find "$dir" -type f -print0)

  echo "$largest_path"
}

stage_header(){
  log "======================================"
  log "$1"
  log "Base: $BASE"
  log "Mode: $( [ "$DRY_RUN" -eq 1 ] && echo 'DRY RUN' || echo 'EXECUTE (Trash/Move)' )"
  log "Logg: $LOG"
  log "======================================"
  log ""
}

# -----------------------
# STEG 1: Cleanup
# -----------------------
stage_header "STEG 1/3: Cleanup – behold største VIDEO-fil per mappe (resten -> Papirkurv)"

s1_folders=0
s1_skipped_no_video=0
s1_files_moved=0
s1_bytes_moved=0

for dir in "$BASE"/*; do
  [[ -d "$dir" ]] || continue
  folder="$(basename "$dir")"
  ((s1_folders++))

  log "--------------------------------------"
  log "Mappe: $folder"

  if [ "$DRY_RUN" -eq 0 ]; then
    find "$dir" -type f -name ".DS_Store" -delete 2>/dev/null || true
  fi

  keep="$(pick_largest_video_in_dir "$dir")"
  if [[ -z "$keep" ]]; then
    log "  Ingen videofiler – hopper over."
    ((s1_skipped_no_video++))
    continue
  fi

  keep_size=$(stat -f%z "$keep" 2>/dev/null || echo 0)
  log "  Beholder: $(basename "$keep")  ($(fmt_gib "$keep_size"))"

  moved_here=0
  while IFS= read -r -d '' f; do
    [[ "$f" == "$keep" ]] && continue
    bn="$(basename "$f")"
    [[ "$bn" == ".DS_Store" ]] && continue

    size=$(stat -f%z "$f" 2>/dev/null || echo 0)
    dest="$TRASH/$bn"
    [[ -e "$dest" ]] && dest="$TRASH/${bn}_$(date +%s)"

    if [ "$DRY_RUN" -eq 0 ]; then
      mv "$f" "$dest" 2>/dev/null || { log "  FEIL: klarte ikke flytte: $f"; continue; }
      ((moved_here++))
      ((s1_files_moved++))
      ((s1_bytes_moved+=size))
    fi
  done < <(find "$dir" -type f -print0)

  log "  Flyttet til Papirkurv (i denne mappa): $moved_here"
done

pause_with_summary "STEG 1 FERDIG – OPPSUMMERING" \
  "Hva gjorde steg 1: Beholdt største VIDEO-fil i hver undermappe, flyttet resten til Papirkurv." \
  "Mapper behandlet: $s1_folders" \
  "Mapper uten videofil (hoppet over): $s1_skipped_no_video" \
  "Filer flyttet til Papirkurv: $s1_files_moved" \
  "Data flyttet til Papirkurv: $(fmt_gib "$s1_bytes_moved")"

# -----------------------
# STEG 2: Rename
# -----------------------
stage_header "STEG 2/3: Rename – filnavn = mappenavn (inni hver undermappe)"

s2_folders=0
s2_skipped_no_video=0
s2_already_ok=0
s2_renamed=0
s2_skipped_target_exists=0

for dir in "$BASE"/*; do
  [[ -d "$dir" ]] || continue
  folder="$(basename "$dir")"
  ((s2_folders++))

  keep="$(pick_largest_video_in_dir "$dir")"
  if [[ -z "$keep" ]]; then
    ((s2_skipped_no_video++))
    continue
  fi

  ext="${keep##*.}"
  new="$dir/$folder.$ext"

  if [[ "$keep" == "$new" ]]; then
    ((s2_already_ok++))
    continue
  fi
  if [[ -e "$new" ]]; then
    log "Mappe: $folder → SKIP (mål finnes): $(basename "$new")"
    ((s2_skipped_target_exists++))
    continue
  fi

  log "Mappe: $folder → Omdøper: $(basename "$keep") → $(basename "$new")"
  if [ "$DRY_RUN" -eq 0 ]; then
    mv -n "$keep" "$new" 2>/dev/null || { log "  FEIL ved omdøping"; continue; }
    ((s2_renamed++))
  fi
done

pause_with_summary "STEG 2 FERDIG – OPPSUMMERING" \
  "Hva gjorde steg 2: Omdøpte beholdt videofil til samme navn som mappen (beholdt filtype)." \
  "Mapper behandlet: $s2_folders" \
  "Mapper uten videofil (hoppet over): $s2_skipped_no_video" \
  "Allerede riktig navn: $s2_already_ok" \
  "Omdøpt: $s2_renamed" \
  "Hoppet over pga eksisterende målfil: $s2_skipped_target_exists"

# -----------------------
# STEG 3: Flatten + slett tom undermappe
# -----------------------
stage_header "STEG 3/3: Flatten – flytt fil til rot + slett tom undermappe"

s3_folders=0
s3_skipped_no_video=0
s3_moved_to_root=0
s3_skipped_dest_exists=0
s3_dirs_deleted=0

for dir in "$BASE"/*; do
  [[ -d "$dir" ]] || continue
  folder="$(basename "$dir")"
  ((s3_folders++))

  keep="$(pick_largest_video_in_dir "$dir")"
  if [[ -z "$keep" ]]; then
    ((s3_skipped_no_video++))
    continue
  fi

  bn="$(basename "$keep")"
  dest="$BASE/$bn"

  if [[ -e "$dest" ]]; then
    log "Mappe: $folder → SKIP (finnes i rot): $bn"
    ((s3_skipped_dest_exists++))
  else
    log "Mappe: $folder → Flytter til rot: $bn"
    if [ "$DRY_RUN" -eq 0 ]; then
      mv "$keep" "$dest" 2>/dev/null || { log "  FEIL ved flytting"; continue; }
      ((s3_moved_to_root++))
    fi
  fi

  if [ "$DRY_RUN" -eq 0 ]; then
    empty_count=$(find "$dir" -type d -empty 2>/dev/null | wc -l | tr -d ' ')
    if [[ "$empty_count" != "0" ]]; then
      find "$dir" -type d -empty -delete 2>/dev/null || true
      ((s3_dirs_deleted+=empty_count))
    fi
  fi
done

pause_with_summary "STEG 3 FERDIG – OPPSUMMERING" \
  "Hva gjorde steg 3: Flyttet beholdt videofil ut i rotmappa og slettet tomme undermapper." \
  "Mapper behandlet: $s3_folders" \
  "Mapper uten videofil (hoppet over): $s3_skipped_no_video" \
  "Flyttet filer til rot: $s3_moved_to_root" \
  "Hoppet over pga fil finnes i rot: $s3_skipped_dest_exists" \
  "Tomme undermapper slettet: $s3_dirs_deleted"

log "======================================"
log "FERDIG: Cleanup + Rename + Flatten"
log "Logg: $LOG"
log "======================================"
log ""

osascript -e 'display notification "Pipeline ferdig" with title "RIPS"'
echo -n "Trykk Enter for å lukke..."
read -r
exit 0
