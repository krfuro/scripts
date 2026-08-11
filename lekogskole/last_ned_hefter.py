#!/usr/bin/env python3
"""
Last ned og sorter alle gratis oppgavehefter (PDF) fra lekogskole.no

Scriptet crawler hele domenet www.lekogskole.no, leser kategoriene WordPress
legger på hvert innlegg, og lagrer hver PDF i mappen Fag/Klassetrinn/.

Eksempel:
    Matematikk/2. klasse/mitt-gangehefte-nivaa-1.pdf
    Tema/Jul/1. klasse/julehefte-1-klasse.pdf

Regler:
  * Fag vinner over tema  – et mattehefte med juletema havner i Matematikk/
  * Hver PDF lagres kun ett sted – ingen duplikater
  * Filer som allerede finnes et sted i mappetreet flyttes på plass i stedet
    for å lastes ned på nytt

Bruk:
    python3 last_ned_hefter.py [mappe]

Standard mappe er "lekogskole_hefter".
"""

import os
import re
import shutil
import sys
import time
import urllib.parse as up
from collections import deque

import requests
from bs4 import BeautifulSoup

START = "https://www.lekogskole.no/"
DOMENER = {"www.lekogskole.no", "lekogskole.no"}
ROT = sys.argv[1] if len(sys.argv) > 1 else "lekogskole_hefter"
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

HOPP_OVER = re.compile(
    r"(/wp-admin|/wp-login|/feed|\?replytocom|/kurv|/kasse|/min-konto|"
    r"\.(jpg|jpeg|png|gif|svg|webp|css|js|zip|docx?|pptx?)$)", re.I
)

# Rekkefølgen bestemmer prioritet – første treff vinner.
# Fag først, deretter tema, deretter materialtype.
KATEGORIER = [
    # --- Fag ---
    ("matematikk", "Matematikk"),
    ("engelsk", "Engelsk"),
    ("samisk", "Samisk"),
    ("natur", "Naturfag"),
    ("nynorsk", "Norsk (nynorsk)"),
    ("bokmaal", "Norsk (bokmål)"),
    # --- Tema ---
    ("jul", "Tema/Jul"),
    ("halloween", "Tema/Halloween"),
    ("fastelaven", "Tema/Fastelavn"),
    ("aarstidene", "Tema/Årstidene"),
    ("dyr", "Tema/Dyr"),
    ("kroppen", "Tema/Kroppen"),
    ("trafikk", "Tema/Trafikk"),
    ("sosial", "Tema/Sosialt"),
    ("lese", "Tema/Lesing"),
    # --- Materialtype (kun hvis ingenting over passer) ---
    ("plakater", "Plakater"),
    ("laeringsspill", "Læringsspill"),
    ("blandet-oppgaver", "Blandet"),
]

TRINN = {f"{n}-klasse": n for n in range(1, 8)}

# Samlesider: PDF-er som bare ligger her har ingen egen innleggsside og dermed
# ingen kategorier. Da bestemmer siden de ble funnet på hvilken mappe de får.
SAMLESIDER = [
    ("laeringssirkler", "Læringssirkler"),
    ("laeringsplakater", "Plakater"),
    ("plakater", "Plakater"),
    ("laeringsspill", "Læringsspill"),
    ("blandet-oppgaver", "Blandet"),
    ("fargelegging", "Fargelegging"),
    ("barnehage", "Barnehage"),
]

# Siste utvei: gjett fag/tema ut fra ord i filnavnet.
NAVNEHINT = [
    (r"gange|divisjon|pluss|minus|matte|matematikk|tall|volum|omkrets|areal|"
     r"brøk|broek|klokke|geometri|statistikk|regne|algebra|"
     r"stoerre-eller-mindre|mindre-enn", "Matematikk"),
    (r"engelsk|english|animals|numbers|colours|colors|body|family|clothes|"
     r"fruit|food|weather", "Engelsk"),
    (r"nynorsk", "Norsk (nynorsk)"),
    (r"samisk", "Samisk"),
    (r"jul|advent|nisse", "Tema/Jul"),
    (r"halloween|spoekelse|graskar", "Tema/Halloween"),
    (r"fastelaven|fastelavn", "Tema/Fastelavn"),
    (r"hoest|vaar|vinter|sommer|aarstid|saesonn", "Tema/Årstidene"),
    (r"dyr|dino|skillpadde|loeve|krokodille|havet|enhjoerning|unicorn|fugl",
     "Tema/Dyr"),
    (r"kropp|organer|skjelett", "Tema/Kroppen"),
    (r"trafikk|bil|tog|fly|romraket|ufo", "Tema/Trafikk"),
    (r"lese|leseboek|lesekort|bokstav|alfabet|skrive|ord", "Tema/Lesing"),
]


# ---------------------------------------------------------------- hjelpere

def er_intern(url):
    return up.urlparse(url).netloc in DOMENER


def rydd(url):
    p = up.urlparse(url)
    return up.urlunparse((p.scheme, p.netloc, p.path, "", p.query, ""))


def rydd_pdf(url):
    """PDF-lenkene har ?media=... som varierer – fjern query for å unngå duplikater."""
    p = up.urlparse(url)
    return up.urlunparse((p.scheme, p.netloc, p.path, "", "", ""))


def filnavn_fra(url):
    navn = up.unquote(os.path.basename(up.urlparse(url).path))
    return re.sub(r"[^\w\-. æøåÆØÅ]", "_", navn)


def mappe_for(slugs, kilder=(), navn=""):
    """Velg mappe: 1) innleggets kategorier, 2) samlesiden, 3) filnavnet."""
    for slug, mappe in KATEGORIER:
        if slug in slugs:
            return mappe

    for bit, mappe in SAMLESIDER:
        if any(bit in k for k in kilder):
            return mappe

    lav = navn.lower()
    for moenster, mappe in NAVNEHINT:
        if re.search(moenster, lav):
            return mappe

    return "Diverse"


def trinn_for(slugs):
    """Lag undermappe for klassetrinn, f.eks. '1. klasse' eller '1.-2. klasse'."""
    nivaa = sorted(TRINN[s] for s in slugs if s in TRINN)
    if not nivaa:
        return "Uten klassetrinn"
    if len(nivaa) == 1:
        return f"{nivaa[0]}. klasse"
    return f"{nivaa[0]}.-{nivaa[-1]}. klasse"


def kategorier_i(artikkel):
    """Hent 'category-xxx'-klassene WordPress legger på <article>."""
    return {
        k[len("category-"):]
        for k in (artikkel.get("class") or [])
        if k.startswith("category-")
    }


# ---------------------------------------------------------------- crawling

def crawl():
    """Gå gjennom domenet og returner {pdf_url: {"slugs": set, "kilder": set}}."""
    besokt, pdf_er = set(), {}
    ko = deque([START])

    def registrer(pdf_url, slugs, kilde):
        post = pdf_er.setdefault(rydd_pdf(pdf_url), {"slugs": set(), "kilder": set()})
        post["slugs"].update(slugs)
        post["kilder"].add(kilde)

    while ko:
        url = ko.popleft()
        if url in besokt:
            continue
        besokt.add(url)

        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
        except Exception as e:
            print(f"  ! Feil på {url}: {e}")
            continue
        if r.status_code != 200 or "text/html" not in r.headers.get("content-type", ""):
            continue

        soup = BeautifulSoup(r.text, "html.parser")
        print(f"[{len(besokt):4}] {url}")

        # Innlegget selv (ikke «relaterte innlegg» i sidestolpen)
        hoved = soup.select_one("article.ast-article-single") or soup.select_one("article")
        slugs = kategorier_i(hoved) if hoved else set()

        # PDF-er inne i selve innlegget arver innleggets kategorier
        if hoved:
            for a in hoved.find_all("a", href=True):
                lenke = up.urljoin(url, a["href"])
                if ".pdf" in lenke.lower():
                    registrer(lenke, slugs, url)

        # Følg interne lenker videre
        for a in soup.find_all("a", href=True):
            lenke = rydd(up.urljoin(url, a["href"]))
            if lenke.lower().split("?")[0].endswith(".pdf"):
                registrer(lenke, set(), url)
            elif er_intern(lenke) and not HOPP_OVER.search(lenke) and lenke not in besokt:
                ko.append(lenke)

        time.sleep(0.3)

    return pdf_er


# ---------------------------------------------------------------- nedlasting

def finn_eksisterende(navn):
    """Let etter filen et sted i mappetreet fra før (så vi slipper ny nedlasting)."""
    for rot, _, filer in os.walk(ROT):
        if navn in filer:
            return os.path.join(rot, navn)
    return None


def last_ned(pdf_er):
    fordeling, urestet = {}, []
    for i, (url, info) in enumerate(sorted(pdf_er.items()), 1):
        slugs, kilder = info["slugs"], info["kilder"]
        navn = filnavn_fra(url)
        fag = mappe_for(slugs, kilder, navn)
        if fag == "Diverse":
            urestet.append((navn, sorted(kilder)[:2]))
        undermappe = os.path.join(fag, trinn_for(slugs))
        mappe = os.path.join(ROT, undermappe)
        sti = os.path.join(mappe, navn)
        fordeling[undermappe] = fordeling.get(undermappe, 0) + 1

        if os.path.exists(sti):
            continue

        os.makedirs(mappe, exist_ok=True)
        gammel = finn_eksisterende(navn)
        if gammel:
            shutil.move(gammel, sti)
            print(f"[{i}/{len(pdf_er)}] → flyttet: {undermappe}/{navn}")
            continue

        try:
            r = requests.get(url, headers=HEADERS, timeout=60)
            r.raise_for_status()
            if not r.content.startswith(b"%PDF"):
                print(f"[{i}/{len(pdf_er)}] ! Ikke en PDF: {navn}")
                continue
            with open(sti, "wb") as f:
                f.write(r.content)
            print(f"[{i}/{len(pdf_er)}] ✓ {undermappe}/{navn} ({len(r.content)//1024} kB)")
        except Exception as e:
            print(f"[{i}/{len(pdf_er)}] ! Feil: {navn} – {e}")

    return fordeling, urestet


def rydd_tomme():
    """Fjern mapper som ble stående igjen tomme etter flytting.

    Kjøres i runder: når en undermappe fjernes kan foreldremappen bli tom,
    og den oppdages først i neste runde.
    """
    while True:
        fjernet = 0
        for rot, _, _ in os.walk(ROT, topdown=False):
            if rot != ROT and not os.listdir(rot):
                os.rmdir(rot)
                fjernet += 1
        if not fjernet:
            break


if __name__ == "__main__":
    print("Steg 1: Crawler www.lekogskole.no ...\n")
    pdf_er = crawl()
    print(f"\nFant {len(pdf_er)} PDF-er.\n\nSteg 2: Laster ned og sorterer ...\n")
    fordeling, urestet = last_ned(pdf_er)
    rydd_tomme()

    print(f"\n✅ Ferdig! Filene ligger i '{ROT}/'\n")
    print("Fordeling:")
    for mappe in sorted(fordeling):
        print(f"  {fordeling[mappe]:4}  {mappe}")

    if urestet:
        print(f"\nUsortert ({len(urestet)}) – havnet i Diverse/:")
        for navn, kilder in urestet:
            print(f"  {navn}")
            for k in kilder:
                print(f"      funnet på: {k}")
