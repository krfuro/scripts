# Lek og skole – gratis oppgavehefter

Denne guiden forklarer hvordan du laster ned alle gratis oppgavehefter (PDF) fra
[lekogskole.no](https://www.lekogskole.no) – ferdige arbeidshefter for barnetrinnet
i norsk, matematikk, engelsk, naturfag m.m. – og sorterer dem automatisk i mapper
etter fag og klassetrinn.

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

## Steg 1 – Last ned og sorter

```bash
cd ~/den/mappen/du/vil/ha/filene
python3 /sti/til/last_ned_hefter.py "Lek og skole"
```

Argumentet er navnet på rotmappen filene havner i (standard: `lekogskole_hefter`).

Følgende skjer:

1. **Crawling** – scriptet starter på forsiden og følger alle interne lenker på
   `www.lekogskole.no` (kategorisider, klassetrinn, paginering, enkeltinnlegg).
2. **Kategorisering** – WordPress legger kategoriene som CSS-klasser på hvert
   innlegg (`category-matematikk`, `category-2-klasse`). Scriptet leser disse
   direkte fra `<article>`-taggen.
3. **Nedlasting** – hver PDF lagres i `Fag/Klassetrinn/`. Filer som allerede
   finnes hoppes over, og filer som ligger feil sted flyttes på plass.

> ⏱ Hele jobben tar ca. 8–15 minutter. Kjøres den på nytt hentes kun nye hefter.

---

## Mappestrukturen

```
Lek og skole/
├── Matematikk/
│   ├── 1. klasse/
│   ├── 2.-3. klasse/
│   └── …
├── Norsk (bokmål)/
├── Norsk (nynorsk)/
├── Engelsk/
├── Naturfag/
├── Samisk/
├── Tema/
│   ├── Jul/  Halloween/  Fastelavn/  Årstidene/
│   └── Dyr/  Kroppen/  Trafikk/  Sosialt/  Lesing/
├── Plakater/
├── Læringssirkler/
├── Læringsspill/
├── Fargelegging/
├── Barnehage/
└── Blandet/
```

### Sorteringsregler

**Fag vinner over tema.** Et julehefte i matematikk havner i `Matematikk/`, ikke i
`Tema/Jul/`. Temamappene inneholder derfor kun hefter som ikke tilhører et fag.

**Hver PDF lagres kun ett sted** – ingen duplikater.

**Klassetrinn** hentes fra innleggets kategorier. Dekker et hefte flere trinn blir
mappen et intervall, f.eks. `2.-4. klasse`. Hefter uten trinn havner i
`Uten klassetrinn/`.

Prioriteringen når mappe skal velges:

1. **Innleggets kategorier** – fag først (matematikk, engelsk, samisk, natur,
   nynorsk, bokmål), så tema, så materialtype.
2. **Samlesiden** – PDF-er på `/laeringssirkler/`, `/laeringsplakater/`,
   `/laeringsspill/`, `/blandet-oppgaver/`, `/fargelegging/` og `/barnehage/` har
   ingen egen innleggsside, og sorteres etter siden de ble funnet på.
3. **Filnavnet** – siste utvei, se `NAVNEHINT` i scriptet.

Hefter som ikke treffer noen av reglene havner i `Diverse/` og listes opp til slutt
i terminalen, med lenke til siden de ble funnet på – slik at reglene kan utvides.

---

## ⚠️ Merk: klassetrinn i filnavnet stemmer ikke

Nettstedet er oversatt fra dansk, og **filnavnene har beholdt de danske
klassetrinnene**. Danmark har `0. klasse` (børnehaveklasse) som første år, så norsk
trinn ligger konsekvent **ett hakk over** tallet i filnavnet.

| Filnavn | Nettstedets norske kategori | Mappe |
|---------|------------------------------|-------|
| `matematikk-4-klasse.pdf` | 5. klasse | `Matematikk/5. klasse/` |
| `Naturens-krefter-4.-6.-klasse-.pdf` | 5.–7. klasse | `Naturfag/5.-7. klasse/` |
| `Halloween-1.-klasse-norsk.pdf` | 2. klasse | `Matematikk/2. klasse/` |

**Mappen er riktig, filnavnet er ikke.** Scriptet bruker nettstedets egne norske
kategorier, som er det heftene faktisk er tilpasset. Se bort fra tallet i filnavnet.

---

## Slik virker scriptet

| Del | Hva den gjør |
|-----|--------------|
| `crawl()` | Bredde-først-søk gjennom hele domenet. Registrerer for hver PDF både kategoriene og hvilke sider den ble funnet på. |
| `kategorier_i()` | Plukker ut `category-*`-klassene WordPress legger på `<article>`. |
| `article.ast-article-single` | Sikrer at vi leser kategoriene til selve innlegget, ikke til «relaterte innlegg» i sidestolpen. |
| `mappe_for()` | Velger fag-/temamappe etter prioriteringen over. |
| `trinn_for()` | Lager klassetrinn-mappen, inkl. intervaller som `2.-4. klasse`. |
| `rydd_pdf()` | Fjerner `?media=…` fra PDF-lenkene – samme fil lenkes med ulik query. |
| `finn_eksisterende()` | Leter etter filen i mappetreet fra før, og flytter den i stedet for å laste ned på nytt. |
| `rydd_tomme()` | Fjerner tomme mapper etter flytting. Kjøres i runder, siden en foreldremappe først blir tom etter at undermappen er slettet. |
| `time.sleep(0.3)` | Pause mellom hver sideforespørsel – vær grei med serveren. |

---

## Feilsøking

**«ModuleNotFoundError: No module named 'bs4'»**
Kjør installasjonskommandoen over. På macOS må `--break-system-packages` være med.

**Scriptet finner 0 PDF-er**
Sjekk at du har nett og at `https://www.lekogskole.no` svarer i nettleseren.
Nettstedet kan ha lagt om strukturen – se om PDF-lenkene fortsatt peker til
`usercontent.one`.

**Mange filer havner i `Diverse/`**
Se listen scriptet skriver ut til slutt. Den viser hvilken side hver fil ble funnet
på – legg siden inn i `SAMLESIDER` eller et nytt mønster i `NAVNEHINT`.

**Noen filer feiler med timeout**
Kjør scriptet på nytt. Ferdige filer hoppes over, så bare de manglende hentes.

---

## Informasjon

- **Nettsted:** https://www.lekogskole.no
- **Startside for hefter:** https://www.lekogskole.no/oppgavehefter/
- **CDN for filene:** `usercontent.one/wp/www.lekogskole.no/wp-content/uploads/...`
- **Ingen innlogging nødvendig** – heftene er publisert gratis av nettstedet
- **Målgruppe:** barnehage og 1.–7. klasse
- **Omfang per august 2026:** 336 PDF-er, ca. 205 MB

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
