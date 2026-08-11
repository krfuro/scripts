#!/usr/bin/env python3
"""
Last ned alle gratis oppgavehefter (PDF) fra lekogskole.no

Scriptet crawler hele domenet www.lekogskole.no, finner alle lenker til
PDF-filer (som ligger på usercontent.one-CDN-en) og laster dem ned til
en lokal mappe.

Bruk:
    python3 last_ned_hefter.py [mappe]

Standard mappe er "lekogskole_hefter".
"""

import os
import re
import sys
import time
import urllib.parse as up
from collections import deque

import requests
from bs4 import BeautifulSoup

START = "https://www.lekogskole.no/"
DOMENER = {"www.lekogskole.no", "lekogskole.no"}
MAPPE = sys.argv[1] if len(sys.argv) > 1 else "lekogskole_hefter"
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

# Sider vi ikke trenger å crawle (støy)
HOPP_OVER = re.compile(
    r"(/wp-admin|/wp-login|/feed|\?replytocom|/kurv|/kasse|/min-konto|"
    r"\.(jpg|jpeg|png|gif|svg|webp|css|js|zip|docx?|pptx?)$)", re.I
)


def er_intern(url: str) -> bool:
    return up.urlparse(url).netloc in DOMENER


def rydd(url: str) -> str:
    """Fjern fragment og trailing '?'-støy."""
    p = up.urlparse(url)
    return up.urlunparse((p.scheme, p.netloc, p.path, "", p.query, ""))


def crawl() -> dict:
    """Gå gjennom hele domenet og returner {pdf_url: sist_sette_sidetittel}."""
    besokt, pdf_er = set(), {}
    ko = deque([START])

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
        tittel = (soup.title.string or "").strip() if soup.title else ""
        print(f"[{len(besokt):4}] {url}")

        for a in soup.find_all("a", href=True):
            lenke = rydd(up.urljoin(url, a["href"]))
            if lenke.lower().split("?")[0].endswith(".pdf"):
                if lenke not in pdf_er:
                    tekst = a.get_text(strip=True) or tittel
                    pdf_er[lenke] = tekst
                    print(f"       + PDF: {tekst[:60]}")
            elif er_intern(lenke) and not HOPP_OVER.search(lenke) and lenke not in besokt:
                ko.append(lenke)

        time.sleep(0.3)  # vær grei med serveren

    return pdf_er


def filnavn_fra(url: str) -> str:
    navn = up.unquote(os.path.basename(up.urlparse(url).path))
    return re.sub(r"[^\w\-. æøåÆØÅ]", "_", navn)


def last_ned(pdf_er: dict) -> None:
    os.makedirs(MAPPE, exist_ok=True)
    for i, (url, tittel) in enumerate(sorted(pdf_er.items()), 1):
        navn = filnavn_fra(url)
        sti = os.path.join(MAPPE, navn)
        if os.path.exists(sti):
            print(f"[{i}/{len(pdf_er)}] Hopper over (finnes): {navn}")
            continue
        try:
            r = requests.get(url, headers=HEADERS, timeout=60)
            r.raise_for_status()
            if not r.content.startswith(b"%PDF"):
                print(f"[{i}/{len(pdf_er)}] ! Ikke en PDF: {navn}")
                continue
            with open(sti, "wb") as f:
                f.write(r.content)
            print(f"[{i}/{len(pdf_er)}] ✓ {navn} ({len(r.content)//1024} kB)")
        except Exception as e:
            print(f"[{i}/{len(pdf_er)}] ! Feil: {navn} – {e}")


if __name__ == "__main__":
    print("Steg 1: Crawler www.lekogskole.no ...\n")
    pdf_er = crawl()
    print(f"\nFant {len(pdf_er)} PDF-er.\n\nSteg 2: Laster ned ...\n")
    last_ned(pdf_er)
    print(f"\n✅ Ferdig! Filene ligger i '{MAPPE}/'")
