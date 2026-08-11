# Lek og skole – gratis oppgavehefter

Denne guiden forklarer hvordan du laster ned alle gratis oppgavehefter (PDF) fra
[lekogskole.no](https://www.lekogskole.no) – ferdige arbeidshefter for barnetrinnet
i norsk, matematikk, engelsk, naturfag m.m.

---

## Før du starter – installer nødvendige programmer

Åpne terminalen og kjør:

```bash
pip3 install requests beautifulsoup4 --break-system-packages
```

Dette installerer:

- `requests` – henter nettsider og filer
- `beautifulsoup4` – leser HTML-en og finner lenkene

---

## Steg 1 – Last ned alle heftene

```bash
python3 last_ned_hefter.py "Lek og skole"
```

Argumentet er mappenavnet filene havner i (standard: `lekogskole_hefter`).
Scriptet lager mappen i katalogen du står i, så `cd` deg dit du vil ha filene først:

```bash
cd ~/Documents/Skole
python3 /sti/til/last_ned_hefter.py "Lek og skole"
```

Følgende skjer:

1. **Crawling** – scriptet starter på forsiden og følger alle interne lenker på
   `www.lekogskole.no` (kategorisider, klassetrinn, paginering, enkeltinnlegg).
2. **Innsamling** – hver `.pdf`-lenke som dukker opp lagres i en liste. PDF-ene
   ligger ikke på selve domenet, men på CDN-en `usercontent.one` – scriptet
   følger dem dit automatisk.
3. **Nedlasting** – alle PDF-ene lastes ned med originalt filnavn. Filer som
   allerede finnes hoppes over, så scriptet er trygt å kjøre på nytt.

> ⏱ Hele jobben tar ca. 10–20 minutter avhengig av nettforbindelse.

---

## Slik virker scriptet

| Del | Hva den gjør |
|-----|--------------|
| `crawl()` | Bredde-først-søk (kø) gjennom hele domenet. Holder styr på besøkte sider så ingenting hentes to ganger. |
| `HOPP_OVER` | Regex som filtrerer bort støy: `wp-admin`, `wp-login`, `/feed`, kommentarlenker, bilder, CSS/JS. |
| `er_intern()` | Sikrer at crawleren kun følger lenker på `lekogskole.no` – men PDF-lenker til CDN-en samles uansett. |
| `rydd()` | Fjerner `#fragment` fra URL-er så samme side ikke telles flere ganger. |
| `filnavn_fra()` | URL-dekoder filnavnet og fjerner tegn som ikke fungerer i filsystemet (beholder æ/ø/å). |
| `last_ned()` | Sjekker at filen faktisk starter med `%PDF` før den lagres – fanger opp 404-sider som returnerer HTML. |
| `time.sleep(0.3)` | Pause mellom hver sideforespørsel – vær grei med serveren. |

---

## Feilsøking

**«ModuleNotFoundError: No module named 'bs4'»**
Kjør installasjonskommandoen over. På macOS må `--break-system-packages` være med.

**Scriptet finner 0 PDF-er**
Sjekk at du har nett og at `https://www.lekogskole.no` svarer i nettleseren.
Nettstedet kan ha lagt om strukturen – se om PDF-lenkene fortsatt peker til
`usercontent.one`.

**Noen filer feiler med timeout**
Kjør scriptet på nytt. Ferdige filer hoppes over, så bare de manglende hentes.

---

## Informasjon

- **Nettsted:** https://www.lekogskole.no
- **Startside for hefter:** https://www.lekogskole.no/oppgavehefter/
- **CDN for filene:** `usercontent.one/wp/www.lekogskole.no/wp-content/uploads/...`
- **Ingen innlogging nødvendig** – heftene er publisert gratis av nettstedet
- **Målgruppe:** 1.–7. klasse

---

## ⚖️ Juridisk disclaimer

Heftene på lekogskole.no er publisert gratis til bruk i undervisning og hjemme,
men innholdet er fortsatt beskyttet av opphavsrett.

- ✅ Nedlasting og utskrift til eget/barnas bruk er tillatt
- ✅ Bruk i egen klasse/undervisning er tillatt
- ❌ Ikke publiser filene videre på nett eller i egne kanaler
- ❌ Ikke bruk innholdet kommersielt

### Norsk lov

**Åndsverkloven (lov 15. juni 2018 nr. 40)**

- **§ 2** – Opphaveren har enerett til å råde over sitt åndsverk, herunder å
  fremstille eksemplar og gjøre det tilgjengelig for allmennheten.
- **§ 26 – Privatkopiering** – Enkelteksemplar av et offentliggjort verk kan
  fremstilles til privat bruk, forutsatt at kopieringen ikke skjer i
  ervervsøyemed og at eksemplaret ikke brukes til annet formål.
- **§ 43 – Bruk i undervisningsvirksomhet** – Offentliggjort verk kan brukes i
  undervisning innenfor rammene av avtalelisens (Kopinor-avtalen).
- **§ 99 – Forbud mot omgåelse av tekniske beskyttelsessystemer** – Scriptet
  omgår ingen sperrer; filene er åpent publisert uten innlogging eller DRM.
- **§ 81 – Sanksjoner** – Brudd kan medføre krav om vederlag og erstatning.

### Internasjonal lov og avtaler

**Bernkonvensjonen (1886, sist revidert 1979)** – Norge er tilsluttet, og
opphavsrett gjelder automatisk i alle 181 medlemsland.

**TRIPS-avtalen (1994)** – WTO-administrert minimumsstandard for
opphavsrettsbeskyttelse, også for digitalt innhold.

**EU-direktiv 2001/29/EF (Infosoc)** – Implementert i norsk rett gjennom
åndsverkloven.

**EU-direktiv 2019/790 (DSM)** – Moderniserer opphavsretten digitalt; Norge
påvirkes som EØS-land.

### Hva er lov – og hva er ikke lov

| Handling | Status |
|----------|--------|
| Laste ned gratis publiserte hefter til privat bruk | ✅ Lovlig (ÅVL §26) |
| Skrive ut til egne barn / egen klasse | ✅ Lovlig (ÅVL §26, §43) |
| Lagre lokalt for offline bruk | ✅ Lovlig (ÅVL §26) |
| Dele med kolleger på egen skole | ⚠️ Grå sone – sjekk Kopinor-avtalen |
| Legge filene ut på egen nettside eller i delte grupper | ❌ Ulovlig (ÅVL §2, §81) |
| Bruke innholdet kommersielt | ❌ Ulovlig (ÅVL §2) |
| Selge utskrifter eller bearbeidede versjoner | ❌ Ulovlig (ÅVL §2) |

### Ansvarsfraskrivelse

Forfatteren av dette scriptet påtar seg intet ansvar for ulovlig bruk. Brukeren er
selv ansvarlig for å sikre at bruk er i tråd med gjeldende lovverk og nettstedets
brukervilkår. Ved tvil, konsulter en jurist.
