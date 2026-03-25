#!/usr/bin/env python3
"""
Last ned YouTube-videoer fra en liste med URL-er.
Videoene lagres i beste kvalitet som MP4 i mappen scriptet kjøres fra.
"""
import subprocess
import sys

VIDEOER = [
    # Legg til URL-er her
    # "https://www.youtube.com/watch?v=XXXX",
]

def last_ned(urls):
    kommando = [
        "yt-dlp",
        "-f", "bestvideo+bestaudio",
        "--merge-output-format", "mp4",
        "-o", "%(title)s.%(ext)s",
    ] + urls

    result = subprocess.run(kommando)
    if result.returncode == 0:
        print("\n✅ Alle videoer lastet ned!")
    else:
        print("\n❌ Noe gikk galt. Sjekk output over.")

if __name__ == "__main__":
    urls = sys.argv[1:] if len(sys.argv) > 1 else VIDEOER
    if not urls:
        print("Ingen URL-er oppgitt. Legg til i VIDEOER-listen eller send som argument.")
        sys.exit(1)
    print(f"Laster ned {len(urls)} video(er)...\n")
    last_ned(urls)
