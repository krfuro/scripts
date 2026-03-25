# Sikkerhet, ansvar og kontroll – utg. 19

Denne guiden forklarer steg for steg hvordan du laster ned læreboken fra angerman.no og lager en lokal PDF-fil du kan bruke offline.

---

## Før du starter – installer nødvendige programmer

Åpne terminalen og kjør disse kommandoene én etter én:
```bash
pip3 install playwright pypdf
python3 -m playwright install chromium
```

Dette installerer:
- `playwright` – lar Python styre en nettleser automatisk
- `pypdf` – lar Python sette sammen PDF-filer
- `chromium` – nettleseren som brukes av scriptene

---

## Steg 1 – Logg inn på angerman.no

1. Åpne Chrome
2. Gå til https://angerman.no
3. Logg inn med din konto (e-post og passord)
4. Bekreft at du er logget inn før du går videre

---

## Steg 2 – Last ned boksidene

Åpne terminalen, naviger til mappen der du vil lagre boken, og kjør:
```bash
python3 last_ned_sider.py
```

Følgende vil skje:
- Et Chrome-vindu åpnes automatisk på boksiden
- Scriptet venter 3 sekunder på at siden laster
- Alle 112 sider lastes ned automatisk – to filer per side:
  - `side0001.svg` – inneholder all tekst og vektorgrafik (søkbar i PDF)
  - `page0001_1.jpg` – inneholder bakgrunnsbilde med illustrasjoner og farger
- Du ser `✓ Side 1/112` osv. etter hvert som sider lastes ned
- Chrome-vinduet lukkes automatisk når alt er ferdig
- Du vil da ha 224 filer i mappen (112 SVG + 112 JPG)

> ⚠️ Ikke lukk Chrome-vinduet manuelt mens scriptet kjører

---

## Steg 3 – Lag PDF

Kjør følgende kommando i samme mappe:
```bash
python3 lag_pdf.py
```

Følgende vil skje:
- Scriptet finner automatisk alle nedlastede SVG- og JPG-filer i mappen
- Et usynlig Chrome-vindu åpnes for å rendre hver side korrekt
- Hver side bygges opp slik: JPG-bakgrunn + SVG-tekst lagt oppå
- Du ser `✓ Side 0001`, `✓ Side 0002` osv. etter hvert som sider behandles
- Sider uten SVG (blanke sider) inkluderes automatisk med kun bakgrunn
- Alle sider slås til slutt sammen til én fil
- Når scriptet er ferdig finner du `sikkerhet-ansvar-kontroll.pdf` i mappen

> ⏱ Dette tar ca. 5–10 minutter for 112 sider

---

## Resultat

Du har nå en komplett PDF med:
- ✅ Alle 112 sider i riktig rekkefølge
- ✅ Bilder og illustrasjoner
- ✅ Søkbar tekst (du kan bruke Ctrl+F / Cmd+F i PDF-leseren)
- ✅ Korrekte fonter og layout

---

## Bokinformasjon
- **Tittel:** Sikkerhet, ansvar og kontroll
- **Utgave:** 19
- **Sider:** 112
- **URL:** https://angerman.no/wp-content/uploads/blafiler/full/sikkerhet-ansvar-kontroll-utgave-19/
- **uni-nøkkel:** `c8fa0e9d753f575f88b7fec412b95894`


---

## ⚖️ Juridisk disclaimer

Dette scriptet er laget for lovlig bruk av innhold du har **betalt for eller har rettmessig tilgang til**. Brukeren er selv ansvarlig for å sikre at bruken er i tråd med gjeldende lovverk og plattformens brukervilkår.

### Norsk lov

**Åndsverkloven (lov 15. juni 2018 nr. 40)**

- **§ 2** – Opphaveren har enerett til å råde over sitt åndsverk, herunder å fremstille eksemplar og gjøre det tilgjengelig for allmennheten.
- **§ 26 – Privatkopiering** – Enkelteksemplar av et offentliggjort verk kan fremstilles til privat bruk, forutsatt at kopieringen ikke skjer i ervervsøyemed og at eksemplaret ikke brukes til annet formål. Dette er det juridiske grunnlaget for å laste ned innhold du har lovlig tilgang til, til eget bruk.
- **§ 99 – Forbud mot omgåelse av tekniske beskyttelsessystemer** – Det er forbudt å omgå effektive tekniske beskyttelsessystemer. Brukeren er ansvarlig for å sikre at bruken ikke bryter denne paragrafen.
- **§ 81 – Sanksjoner** – Brudd på åndsverkloven kan medføre krav om vederlag og erstatning. Grove eller gjentatte overtredelser kan medføre bøter eller fengsel.

**Straffeloven (lov 20. mai 2005 nr. 28)**

- **§ 202** – Ulovlig bruk av data eller dataprogram kan straffes med bøter eller fengsel inntil 2 år.

### Internasjonal lov og avtaler

**Bernkonvensjonen (1886, revidert sist 1979)**
Norge er tilsluttet Bernkonvensjonen, som gir opphavsrettsbeskyttelse i alle 181 medlemsland automatisk.

**TRIPS-avtalen (Agreement on Trade-Related Aspects of Intellectual Property Rights, 1994)**
Administreres av WTO. Fastsetter minimumsstandarder for opphavsrettsbeskyttelse internasjonalt, inkludert for digitalt innhold.

**EU-direktiv 2001/29/EF (Infosoc-direktivet)**
Implementert i norsk rett gjennom åndsverkloven. Regulerer opphavsrett i informasjonssamfunnet, inkludert digitalt innhold og tekniske beskyttelsessystemer.

**EU-direktiv 2019/790 (DSM-direktivet – Digital Single Market)**
Moderniserer opphavsretten for den digitale tidsalderen. Norge er EØS-land og påvirkes av dette direktivet.

### Hva er lov – og hva er ikke lov

| Handling | Status |
|----------|--------|
| Laste ned innhold du har betalt for til privat bruk | ✅ Lovlig (ÅVL §26) |
| Lagre lokalt for offline bruk | ✅ Lovlig (ÅVL §26) |
| Dele med nær familie/omgangskrets | ⚠️ Grå sone (ÅVL §26) |
| Distribuere til andre som ikke har tilgang | ❌ Ulovlig (ÅVL §2, §81) |
| Bruke innholdet kommersielt | ❌ Ulovlig (ÅVL §2) |
| Publisere innhold åpent på nett | ❌ Ulovlig (ÅVL §2, §81) |

### Ansvarsfraskrivelse

Forfatteren av dette scriptet påtar seg intet ansvar for ulovlig bruk. Brukeren er selv ansvarlig for å sikre at bruk er i tråd med gjeldende lovverk og plattformens brukervilkår. Ved tvil, konsulter en jurist.
