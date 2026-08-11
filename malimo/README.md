# Malimo – gratis læringsressurser

Laster ned ressursene som er merket **«Pris: Gratis»** på [malimo.no](https://malimo.no)
og sorterer dem i fag- og temamapper.

> ⚠️ **Malimo er en kommersiell abonnementsbutikk.** Dette scriptet laster kun ned
> det som faktisk er gratis. Betalte ressurser hoppes over – se disclaimeren nederst.

---

## Forutsetninger

```bash
pip3 install playwright --break-system-packages
python3 -m playwright install chromium
```

Nedlasting på malimo.no krever innlogging, også for gratisressursene
(«Logg inn for å laste ned. Det er gratis å opprette bruker»). Scriptet bruker
derfor en Chrome-profil som allerede er innlogget.

---

## Steg 1 – Lag en innlogget profil

Logg inn på malimo.no i din vanlige Chrome. Kopier så økten til en egen profil
som scriptet kan bruke – da rører vi ikke Chrome-en du jobber i:

```bash
S="$HOME/Library/Application Support/Google/Chrome/Default"
D="/tmp/malimo-profil/Default"
mkdir -p "$D/IndexedDB"
cp "$HOME/Library/Application Support/Google/Chrome/Local State" /tmp/malimo-profil/
cp "$S/Cookies" "$S/Preferences" "$S/Secure Preferences" "$D/"
cp -R "$S/Local Storage/leveldb" "$D/Local Storage/"
cp -R "$S/IndexedDB/https_malimo.no_0.indexeddb.leveldb" "$D/IndexedDB/"
```

**Hvorfor både Local Storage og IndexedDB?** Malimo lagrer ikke innloggingen i
cookies – økten ligger i nettleserens Local Storage og IndexedDB. Kopierer du bare
`Cookies`, blir profilen utlogget.

---

## Steg 2 – Last ned

```bash
cd ~/den/mappen/du/vil/ha/filene
python3 /sti/til/last_ned_malimo.py "Malimo"
```

Valgfritt andre argument begrenser antall produkter – nyttig for en rask test:

```bash
python3 last_ned_malimo.py "Malimo" 15
```

Følgende skjer:

1. **Kartlegging** – går gjennom alle kategorier i butikken og samler produkt-URL-er.
   Resultatet mellomlagres i `/tmp/malimo_produkter.json`. Slett filen for å
   kartlegge på nytt.
2. **Prissjekk** – hvert produkt åpnes, og kun de med «Pris: Gratis» behandles.
3. **Filvalg** – «Last ned» åpner en dialog med språkvarianter. Scriptet krysser av
   for bokmål og filer uten språkmerking.
4. **Nedlasting** – «Last ned valgte» gir en ZIP, som pakkes ut i riktig mappe.

> ⏱ Full kjøring tar 2–3 timer for ~760 produkter. Kartleggingen alene tar ~11 min.

---

## Mappestrukturen

Samme prinsipp som `lekogskole/` – fag først, så tema:

```
Malimo/
├── Matematikk/   Norsk (bokmål)/   Norsk (nynorsk)/
├── Engelsk/      Naturfag/         Samfunnsfag/      Samisk/
├── Tema/         Jul/  Påske/  Halloween/  17. mai/  Årstidene/
│                 Sosialt/  Trafikk/  Dyr/  Brannvern/
├── Plakater og dekor/   Læringsspill/   Fargelegging/
├── Skolestart/   Barnehage/
└── Diverse/
```

Kategorien utledes av brødsmulestien på produktsiden pluss produktets URL-navn.
Treffer ingen regel, havner filen i `Diverse/` – utvid `KART` i scriptet.

---

## Slik virker scriptet

| Del | Hva den gjør |
|-----|--------------|
| `hent_produktlenker()` | Går gjennom alle kategorier, klikker «vis mer» til antallet slutter å øke. |
| `VELG_JS` | Filnavnet i dialogen er en **utvider**, ikke et valg. Avkrysningsboksen er en egen knapp med `aria-checked` rett før den – denne klikkes. |
| `SPRAK_OK` | Hvilke språk som hentes. Endre til `["nynorsk"]` for nynorsk i stedet. |
| `TRYKK_JS` | Trykker «Last ned valgte» inne i dialogen. |
| `pakk_ut()` | Nedlastingen kommer som ZIP – pakkes ut, og zip-en slettes. Tåler at svaret ikke er en zip. |
| `CACHE` | Produktlisten mellomlagres så kartleggingen ikke gjentas ved ny kjøring. |

---

## Feilsøking

**Alt hoppes over som «betalt»**
Profilen er trolig utlogget. Kjør kopieringen i steg 1 på nytt etter å ha logget
inn i Chrome.

**«ingen filer valgt»**
Dialogen rakk ikke å laste. Øk ventetiden etter klikket på «Last ned».

**Chrome starter ikke med profilen**
En annen prosess bruker mappen. Avslutt tidligere kjøringer, eller slett
`/tmp/malimo-profil/Default/Singleton*`.

---

## ⚖️ Juridisk disclaimer

Malimo AS (org.nr 918 704 639) selger læringsressurser på abonnement. Deler av
innholdet er publisert gratis; resten er betalt.

Kjøps- og brukervilkårene deres slår fast at innhold på nettstedet ikke kan
kopieres uten tillatelse, og at brudd etterfaktureres til tre ganger gjeldende rate.

**Dette scriptet er derfor bygget med én hard begrensning:** det laster kun ned
ressurser der produktsiden viser «Pris: Gratis». Betalte ressurser åpnes ikke og
lastes ikke ned. Scriptet omgår ingen betalingsmur og ingen pålogging – det bruker
en ordinær, innlogget brukerøkt, slik en hvilken som helst bruker ville gjort
manuelt.

- ✅ Laste ned gratisressurser til egen undervisning og egne barn
- ✅ Skrive ut til eget bruk
- ❌ Laste ned betalt materiell du ikke har lisens til
- ❌ Dele filene videre, publisere dem eller bruke dem kommersielt

### Norsk lov

**Åndsverkloven (lov 15. juni 2018 nr. 40)**

- **§ 2** – Opphaveren har enerett til å råde over sitt åndsverk.
- **§ 26 – Privatkopiering** – Enkelteksemplar av offentliggjort verk kan
  fremstilles til privat bruk, ikke i ervervsøyemed.
- **§ 43** – Bruk i undervisning innenfor rammene av avtalelisens (Kopinor).
- **§ 99** – Forbud mot omgåelse av tekniske beskyttelsessystemer. Scriptet omgår
  ingen slike systemer.
- **§ 81** – Brudd kan medføre vederlag og erstatning.

### Hva er lov – og hva er ikke lov

| Handling | Status |
|----------|--------|
| Laste ned ressurser merket «Gratis» med egen bruker | ✅ Lovlig |
| Skrive ut til egne barn / egen klasse | ✅ Lovlig (ÅVL §26, §43) |
| Laste ned betalt materiell uten lisens | ❌ Ulovlig (ÅVL §2, §81) |
| Omgå pålogging eller betalingsmur | ❌ Ulovlig (ÅVL §99) |
| Dele filene videre eller publisere dem | ❌ Ulovlig (ÅVL §2) |
| Bruke innholdet kommersielt | ❌ Ulovlig (ÅVL §2) |

### Ansvarsfraskrivelse

Forfatteren påtar seg intet ansvar for ulovlig bruk. Brukeren er selv ansvarlig for
at bruken er i tråd med lovverket og Malimos brukervilkår. Ved tvil, kontakt
post@malimo.no eller en jurist.
