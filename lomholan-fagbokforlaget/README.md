# LØM Holan – Fagbokforlaget

Denne guiden forklarer steg for steg hvordan du laster ned alle ressursfiler (PDF, PPTX, DOCX, XLSX) fra lomholan.fagbokforlaget.no.

---

## Før du starter – installer nødvendige programmer

Åpne terminalen og kjør disse kommandoene én etter én:
```bash
pip3 install playwright httpx --break-system-packages
python3 -m playwright install chromium
```

Dette installerer:
- `playwright` – lar Python styre en nettleser automatisk
- `httpx` – lar Python laste ned filer fra internett
- `chromium` – nettleseren som brukes av scriptet

---

## Steg 1 – Last ned alle filer

Naviger til mappen der du vil lagre filene og kjør:
```bash
python3 last_ned.py
```

Følgende vil skje:
- Et usynlig Chrome-vindu åpnes automatisk
- Scriptet går gjennom alle tre fagene (Organisasjon og ledelse, Økonomistyring, Markedsføringsledelse)
- For hvert fag går det gjennom kapittel 1–19 og klikker på alle nedlastingsknapper
- Alle fil-IDer fanges opp fra API-et i bakgrunnen
- Etter skanning lastes alle filer ned automatisk til mappen `lomholan_filer/`
- Du ser `Skanner: ...` og `Laster ned: ...` etter hvert som det jobber

> ⏱ Dette tar ca. 10–15 minutter totalt

---

## Resultat

Du finner alle nedlastede filer i mappen `lomholan_filer/`. Typisk innhold:

- **PDF** – løsningsforslag og oppgaver per kapittel
- **PPTX** – PowerPoint-presentasjoner med illustrasjoner
- **DOCX** – maler, eksempler og skjemaer
- **XLSX / XLS / XLSM** – regneark og kalkyler

---

## Informasjon
- **Nettsted:** https://lomholan.fagbokforlaget.no
- **Fag:** Organisasjon og ledelse, Økonomistyring, Markedsføringsledelse
- **Namespace:** `65758e40-59ac-4e2b-8b7b-3d44e37b5114`
- **Ingen innlogging nødvendig** – filene er åpent tilgjengelige

---

## ⚖️ Juridisk disclaimer

Innholdet på lomholan.fagbokforlaget.no er åpent tilgjengelig, men er beskyttet av opphavsrett.

- ✅ Nedlasting til privat bruk er tillatt
- ❌ Ikke distribuer eller del filene videre
- ❌ Ikke bruk innholdet kommersielt
