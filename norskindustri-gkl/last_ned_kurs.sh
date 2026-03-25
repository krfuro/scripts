#!/bin/zsh
# Last ned e-læringskurs fra norskindustri.docebosaas.com som PDF
# Bruk: ./last_ned_kurs.sh <authoring_nr> <antall_slides> <mappenavn>
# Eksempel: ./last_ned_kurs.sh 8 115 Kompetanseutvikling-2025

AUTHORING=$1
ANTALL=$2
MAPPE=$3
BASE_CDN="https://cdn5.dcbstatic.com/files/n/o/norskindustri_docebosaas_com/1774432800/E6zHnVngSwBFZnSD_Vl8EQ/authoring"

if [[ -z "$AUTHORING" || -z "$ANTALL" || -z "$MAPPE" ]]; then
  echo "Bruk: $0 <authoring_nr> <antall_slides> <mappenavn>"
  exit 1
fi

mkdir -p "${MAPPE}/slides"

echo "Laster ned $ANTALL slides fra authoring/$AUTHORING..."
for i in $(seq 1 $ANTALL); do
  num=$(printf "%03d" $i)
  curl -s -o "${MAPPE}/slides/slide_${num}.jpg" \
    "${BASE_CDN}/${AUTHORING}/${AUTHORING}_full_slide${i}_1.jpg" \
    -H 'referer: https://norskindustri.docebosaas.com/'
  echo "✓ Slide $i/$ANTALL"
done

echo "\nLager PDF..."
python3 -c "
import img2pdf, glob
filer = sorted(glob.glob('${MAPPE}/slides/slide_*.jpg'))
with open('${MAPPE}/${MAPPE}.pdf', 'wb') as f:
    f.write(img2pdf.convert(filer))
print('✅ Ferdig! → ${MAPPE}/${MAPPE}.pdf')
"
