#!/usr/bin/env python3
"""
Last ned gratis ressurser fra malimo.no og sorter dem i fag-/temamapper.

Krever at Chrome-profilen i PROFIL er innlogget på malimo.no
(se README – profilen kopieres fra din vanlige Chrome-profil).

Laster KUN ned ressurser der prisen er "Gratis". Betalte hoppes over.
Av språkvariantene hentes bokmål + filer uten språkmerking.

Bruk:
    python3 last_ned_malimo.py <målmappe> [antall_for_test]
"""
import asyncio, json, os, re, shutil, sys, unicodedata, zipfile
from playwright.async_api import async_playwright

PROFIL = "/tmp/malimo-profil"
CACHE = "/tmp/malimo_produkter.json"
BASE = "https://malimo.no"
ROT = sys.argv[1] if len(sys.argv) > 1 else "Malimo"
# Argument 2: enten et tall (test på N produkter) eller en fil med URL-er
# (én per linje) – nyttig for å kjøre om igjen bare det som feilet.
ARG2 = sys.argv[2] if len(sys.argv) > 2 else ""
LISTEFIL = ARG2 if ARG2 and os.path.exists(ARG2) else ""
GRENSE = int(ARG2) if ARG2.isdigit() else 0     # 0 = alle
SPRAK_OK = ["bokmål", "bokmal"]

KART = [
    (r"matematikk|matte|regning|\btall\b|addisjon|subtraksjon|gange|divisjon", "Matematikk"),
    (r"engelsk", "Engelsk"),
    (r"samisk", "Samisk"),
    (r"naturfag|\bnatur\b|kropp|dinosaur|verdensrom|fotosyntes|smakryp", "Naturfag"),
    (r"nynorsk", "Norsk (nynorsk)"),
    (r"norsk|lesing|lesevindu|skriving|språk|bokstav|alfabet|eventyr|adjektiv|"
     r"verb|substantiv|bokrapport|skrivestarter|ordlist|setning|rim|stavelse", "Norsk (bokmål)"),
    (r"samfunnsfag|politikk|valg|\bfn\b|nettvett", "Samfunnsfag"),
    (r"\bjul\b|advent", "Tema/Jul"),
    (r"påske", "Tema/Påske"),
    (r"halloween", "Tema/Halloween"),
    (r"17\.?\s*mai|nasjonaldag|arbeidernes dag", "Tema/17. mai"),
    (r"vinter|\bvår\b|sommer|høst|årstid|sesong", "Tema/Årstidene"),
    (r"sosial|vennskap|følelser|relasjon|pride", "Tema/Sosialt"),
    (r"trafikk|refleks|kjøretøy|motor", "Tema/Trafikk"),
    (r"\bdyr\b|husdyr|gårdsdyr", "Tema/Dyr"),
    (r"brannvern", "Tema/Brannvern"),
    (r"skolestart", "Skolestart"),
    (r"barnehage", "Barnehage"),
    (r"plakat|dekor|banner|skilt|navnelapp|merkelapp|kalender", "Plakater og dekor"),
    (r"spill|bingo|domino|\blek\b|aktivitet", "Læringsspill"),
    (r"fargelegg|farger|mandala", "Fargelegging"),
    (r"mini-crafts|crafts|forming|klipp og lim", "Forming"),
    (r"mat og helse", "Mat og helse"),
    (r"redigerbar|skjema|timeplan|soveliste|ordenselev|velkomstbrev|"
     r"doskjema|liste\b", "Skjemaer og maler"),
]

VELG_JS = """(sprakOk) => {
  // Hver fil har en avkrysningsboks (button[aria-checked]) med radtekst
  // "filnavn | størrelse | språk". Første boks er "Velg alle" – den hoppes over.
  // Filnavnet har ikke alltid filendelse, så vi kan ikke filtrere på det.
  const bokser = [...document.querySelectorAll('[role=dialog] button[aria-checked]')];
  let valgt = 0, sett = 0;
  bokser.forEach(cb => {
    const rad = cb.closest('li')
             || cb.parentElement?.parentElement?.parentElement
             || cb.parentElement;
    const radTekst = (rad ? rad.innerText : '').toLowerCase();
    if (/velg alle|last ned valgte/.test(radTekst)) return;   // kontrollrad
    if (!radTekst.trim()) return;
    sett++;
    const hopp = ['nynorsk','engelsk','samisk','tegnspråk']
        .some(s => radTekst.includes(s)) && !sprakOk.some(s => radTekst.includes(s));
    if (!hopp) { cb.click(); valgt++; }
  });
  return {sett, valgt};
}"""

TRYKK_JS = """() => {
  const b = [...document.querySelectorAll('[role=dialog] button')]
    .find(x => /last ned valgte/i.test(x.innerText || ''));
  if (b) { b.click(); return true; }
  return false;
}"""


def trygt(navn):
    navn = unicodedata.normalize("NFC", navn)
    return re.sub(r"[^\w\-. æøåÆØÅ()+\[\]]", "_", navn).strip() or "fil"


def mappe_for(tekst):
    lav = tekst.lower()
    for m, mappe in KART:
        if re.search(m, lav):
            return mappe
    return "Diverse"


def pakk_ut(zip_sti, mal):
    """Pakk ut PDF-ene fra zip-en til målmappen. Returner antall filer."""
    n = 0
    try:
        with zipfile.ZipFile(zip_sti) as z:
            for medlem in z.namelist():
                if medlem.endswith("/") or medlem.startswith("__MACOSX"):
                    continue
                navn = trygt(os.path.basename(medlem))
                if not navn:
                    continue
                ut = os.path.join(mal, navn)
                if os.path.exists(ut):
                    n += 1
                    continue
                with z.open(medlem) as src, open(ut, "wb") as dst:
                    shutil.copyfileobj(src, dst)
                n += 1
    except zipfile.BadZipFile:
        # ikke en zip – behandle som vanlig fil
        ut = os.path.join(mal, trygt(os.path.basename(zip_sti)))
        shutil.copy(zip_sti, ut)
        return 1
    return n


async def hent_produktlenker(pg):
    await pg.goto(f"{BASE}/shop", wait_until="networkidle", timeout=60000)
    await pg.wait_for_timeout(3000)
    kats = await pg.eval_on_selector_all(
        "a[href*='/shop/categories/']",
        "es => [...new Set(es.map(e => e.getAttribute('href')))]")
    kats = [k if k.startswith("http") else BASE + k for k in kats]
    print(f"Fant {len(kats)} kategorier")

    produkter = set()
    for i, k in enumerate(kats, 1):
        try:
            await pg.goto(k, wait_until="networkidle", timeout=60000)
            await pg.wait_for_timeout(2500)
            forrige = -1
            for _ in range(40):
                n = await pg.eval_on_selector_all("a[href*='/shop/products/']", "es => es.length")
                if n == forrige:
                    break
                forrige = n
                try:
                    knapp = pg.get_by_role("button", name=re.compile(
                        r"(vis mer|last inn mer|se mer|neste|flere)", re.I)).first
                    if await knapp.count():
                        await knapp.click(timeout=3000)
                        await pg.wait_for_timeout(1800)
                        continue
                except Exception:
                    pass
                break
            nye = await pg.eval_on_selector_all(
                "a[href*='/shop/products/']",
                "es => [...new Set(es.map(e => e.getAttribute('href')))]")
            produkter |= {n if n.startswith("http") else BASE + n for n in nye}
            navn = k.rstrip("/").split("/")[-1][:34]
            print(f"  [{i}/{len(kats)}] {navn:<34} +{len(nye):3}  totalt {len(produkter)}")
        except Exception as e:
            print(f"  [{i}/{len(kats)}] FEIL {k}: {str(e)[:70]}")
    return sorted(produkter)


async def behandle(pg, url, teller, totalt):
    slug = url.rstrip("/").split("/")[-1]
    await pg.goto(url, wait_until="networkidle", timeout=60000)
    await pg.wait_for_timeout(2500)
    txt = await pg.inner_text("body")

    if not re.search(r"Pris\s*\n\s*Gratis", txt):
        return "betalt", 0

    # Brødsmulesti gir kategorien, f.eks. "... Alle kategorier / SESONG / Jul / ..."
    i = txt.find("Alle kategorier")
    sti = " ".join(txt[i:i + 200].split("\n")[1:6]) if i >= 0 else ""
    fag = mappe_for(sti + " " + slug)
    mal = os.path.join(ROT, fag)
    os.makedirs(mal, exist_ok=True)

    try:
        await pg.get_by_text("Last ned", exact=True).first.click(timeout=10000)
        await pg.wait_for_timeout(3500)
    except Exception:
        print(f"  ! [{teller}/{totalt}] fant ikke 'Last ned': {slug[:44]}")
        return "feil", 0

    res = await pg.evaluate(VELG_JS, SPRAK_OK)
    if not res["valgt"]:
        print(f"  ! [{teller}/{totalt}] ingen filer valgt ({res['sett']} sett): {slug[:40]}")
        return "feil", 0
    await pg.wait_for_timeout(1200)

    try:
        async with pg.expect_download(timeout=60000) as dl:
            if not await pg.evaluate(TRYKK_JS):
                raise RuntimeError("fant ikke 'Last ned valgte'")
        d = await dl.value
    except Exception as e:
        print(f"  ! [{teller}/{totalt}] nedlasting feilet: {slug[:36]} ({str(e)[:45]})")
        return "feil", 0

    tmp = os.path.join("/tmp", trygt(d.suggested_filename))
    await d.save_as(tmp)
    n = pakk_ut(tmp, mal)
    os.remove(tmp)

    print(f"  ✓ [{teller}/{totalt}] {fag}/  {slug[:40]}  ({n} fil)")
    return "ok", n


async def main():
    os.makedirs(ROT, exist_ok=True)
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            PROFIL, channel="chrome", headless=False,
            args=["--no-first-run", "--no-default-browser-check"],
            accept_downloads=True)
        pg = ctx.pages[0] if ctx.pages else await ctx.new_page()

        if LISTEFIL:
            prod = [l.strip() for l in open(LISTEFIL) if l.strip()]
            print(f"Kjører på {len(prod)} URL-er fra {LISTEFIL}\n")
        elif os.path.exists(CACHE):
            prod = json.load(open(CACHE))
            print(f"Bruker mellomlagret produktliste ({len(prod)} stk).")
            print(f"Slett {CACHE} for å kartlegge butikken på nytt.\n")
        else:
            prod = await hent_produktlenker(pg)
            json.dump(prod, open(CACHE, "w"))

        if GRENSE:
            prod = prod[:GRENSE]
        print(f"{len(prod)} produkter å sjekke\n")

        stat = {"ok": 0, "betalt": 0, "feil": 0}
        filer = 0
        for i, u in enumerate(prod, 1):
            try:
                s, n = await behandle(pg, u, i, len(prod))
            except Exception as e:
                s, n = "feil", 0
                print(f"  ! [{i}/{len(prod)}] {u.split('/')[-1][:40]}: {str(e)[:70]}")
            stat[s] += 1
            filer += n

        print(f"\n✅ Ferdig. Gratis: {stat['ok']} produkter / {filer} filer")
        print(f"   Betalte hoppet over: {stat['betalt']}   Feil: {stat['feil']}")
        await ctx.close()

asyncio.run(main())
