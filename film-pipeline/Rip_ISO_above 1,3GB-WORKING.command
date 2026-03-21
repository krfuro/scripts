#!/bin/zsh
BASE="$(cd "$(dirname "$0")" && pwd)"
TARGET="$BASE"
set -euo pipefail
setopt NULL_GLOB

DIR="/Users/krfuro/Movies/backup"
OUTBASE="$DIR/RIPS"
LOG="$DIR/makemkv_$(date +%Y-%m-%d_%H-%M-%S).log"
MAKEMKV="/Applications/MakeMKV.app/Contents/MacOS/makemkvcon"

THRESH_GIB="1.3"
THRESH_BYTES=$(python3 -c 'print(int(1.3 * 1024**3))')

cd "$DIR"
mkdir -p "$OUTBASE"
touch "$LOG"

export TERM=dumb
exec > >(tee -a "$LOG") 2>&1

echo "======================================"
echo " MakeMKV ISO → MKV batch"
echo " ISO-mappe:  $DIR"
echo " Output:     $OUTBASE"
echo " Logg:       $LOG"
echo " Filter:     Kun titler >= ${THRESH_GIB} GiB"
echo "======================================"
echo ""

if [[ ! -x "$MAKEMKV" ]]; then
  echo "FEIL: makemkvcon ikke funnet her:"
  echo "  $MAKEMKV"
  echo -n "Trykk Enter for å avslutte..."
  read -r
  exit 1
fi

get_titles_over_threshold() {
  local src="$1"
  local tmp
  tmp="$(mktemp)"
  "$MAKEMKV" -r info "$src" > "$tmp" 2>/dev/null || true

  python3 -c '
import sys, re
thr=int(sys.argv[1])
sizes={}
rx=re.compile(r"^TINFO:(\d+),\d+,\d+,\"(.*)\"")

for line in sys.stdin:
    m=rx.match(line.strip())
    if not m: 
        continue
    tid=int(m.group(1)); val=m.group(2)

    b=None
    if val.isdigit():
        b=int(val)
    else:
        m2=re.search(r"(\d+)\s*bytes", val, re.I)
        if m2: b=int(m2.group(1))

    if b is not None:
        sizes[tid]=max(sizes.get(tid,0), b)

for tid in sorted(sizes):
    if sizes[tid] >= thr:
        print(tid)
' "$THRESH_BYTES" < "$tmp"

  rm -f "$tmp"
}

print_titles_table() {
  local src="$1"
  local tmp
  tmp="$(mktemp)"
  "$MAKEMKV" -r info "$src" > "$tmp" 2>/dev/null || true

  python3 -c '
import sys, re
sizes={}
times={}
rx=re.compile(r"^TINFO:(\d+),\d+,\d+,\"(.*)\"")

for line in sys.stdin:
    m=rx.match(line.strip())
    if not m:
        continue
    tid=int(m.group(1)); val=m.group(2)

    # varighet (typisk h:mm:ss eller mm:ss)
    if re.fullmatch(r"\d{1,2}:\d{2}(:\d{2})?", val):
        # velg "lengste" format hvis flere
        prev=times.get(tid)
        if prev is None or len(val) > len(prev):
            times[tid]=val

    # størrelse
    b=None
    if val.isdigit():
        b=int(val)
    else:
        m2=re.search(r"(\d+)\s*bytes", val, re.I)
        if m2: b=int(m2.group(1))
    if b is not None:
        sizes[tid]=max(sizes.get(tid,0), b)

def fmt(b):
    if not b: return "-"
    return f"{b/(1024**3):.2f} GiB"

title_ids=sorted(set(times) | set(sizes))

print("")
print("Tilgjengelige titler i ISO:")
print("  ID   Varighet    Størrelse")
print("  ---  ---------   ---------")
for tid in title_ids:
    print(f"  {tid:<3}  {times.get(tid,'-'):<9}   {fmt(sizes.get(tid))}")
print("")
' < "$tmp"

  rm -f "$tmp"
}

rename_mkvs() {
  local out="$1"
  local base="$(basename "$out")"
  local files=("$out"/*.mkv)
  (( ${#files[@]} == 0 )) && return

  local i=1
  for f in "${files[@]}"; do
    local new
    if (( ${#files[@]} == 1 )); then
      new="$out/$base.mkv"
    else
      new="$out/$base - Part $i.mkv"
    fi
    [[ "$f" != "$new" ]] && mv -n "$f" "$new"
    ((i++))
  done
}

isos=( *.iso *.ISO )
if (( ${#isos[@]} == 0 )); then
  echo "Fant ingen ISO-filer."
  echo -n "Trykk Enter for å avslutte..."
  read -r
  exit 0
fi

for iso in "${isos[@]}"; do
  local_name="${iso%.*}"
  out="$OUTBASE/$local_name"
  src="iso:$DIR/$iso"

  echo "--------------------------------------"
  echo "ISO: $iso"
  echo "Ut:  $out"
  echo "Tid: $(date)"
  echo ""

  mkdir -p "$out"

  titles=($(get_titles_over_threshold "$src"))

  if (( ${#titles[@]} > 0 )); then
    echo "Titler >= ${THRESH_GIB} GiB: ${titles[*]}"
    echo ""
    for tid in "${titles[@]}"; do
      echo "-> Ripper title $tid"
      caffeinate -dimsu "$MAKEMKV" -r --progress=-same --decrypt mkv "$src" "$tid" "$out"
      echo ""
    done
  else
    echo "Ingen titler >= ${THRESH_GIB} GiB."
    print_titles_table "$src"
    echo "Hva vil du gjøre?"
    echo "  - all        (ripp alt)"
    echo "  - 0,1,2      (ripp spesifikke title-id'er)"
    echo "  - skip       (hopp over)"
    echo -n "Valg: "
    read -r choice
    choice="${choice:l}"

    if [[ "$choice" == "all" ]]; then
      caffeinate -dimsu "$MAKEMKV" -r --progress=-same --decrypt mkv "$src" all "$out"
      echo ""
    elif [[ "$choice" == "skip" || -z "$choice" ]]; then
      echo "Hopper over."
      echo ""
      continue
    else
      IFS=',' read -rA tids <<< "$choice"
      for tid in "${tids[@]}"; do
        tid="${tid//[[:space:]]/}"
        [[ -z "$tid" ]] && continue
        echo "-> Ripper title $tid"
        caffeinate -dimsu "$MAKEMKV" -r --progress=-same --decrypt mkv "$src" "$tid" "$out"
        echo ""
      done
    fi
  fi

  rename_mkvs "$out"

  if ls "$out"/*.mkv >/dev/null 2>&1; then
    echo "OK: MKV ferdig i $out"
  else
    echo "ADVARSEL: Ingen MKV laget (sjekk logg)."
  fi
  echo ""
done

osascript -e 'display notification "MakeMKV-ripping er ferdig." with title "Rip_ISO"'
echo -n "Trykk Enter for å lukke..."
read -r
exit 0
