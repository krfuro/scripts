# Norsk Industri – Grunnkurs Ledelse (GKL)

Denne guiden forklarer steg for steg hvordan du laster ned e-læringskurs fra norskindustri.docebosaas.com og lagrer dem som lokale PDF-filer.

---

## Før du starter – installer nødvendige programmer

Åpne terminalen og kjør:
```bash
pip3 install img2pdf
brew install curl
```

---

## Hvordan det fungerer

Kursene er bygget opp av lysbildevisninger der hvert lysbilde er en JPG-fil lagret på et CDN (innholdsleveringsnettverk). Filene er tilgjengelige uten innlogging så lenge du har riktig URL-mønster.

URL-mønster:
```
https://cdn5.dcbstatic.com/files/n/o/norskindustri_docebosaas_com/
1774432800/E6zHnVngSwBFZnSD_Vl8EQ/authoring/{nr}/{nr}_full_slide{side}_1.jpg
```

Hvert kurs har et unikt `authoring`-nummer og et bestemt antall slides.

---

## Kjente kurs og authoring-numre

| Kurs | Authoring-nr | Antall slides |
|------|-------------|---------------|
| Grupper og kommunikasjon 2025 | 5 | 110 |
| Ledelse 2025 | 6 | 153 |
| Organisasjon og endring 2025 | 7 | 111 |
| Kompetanseutvikling 2025 | 8 | 115 |
| HMS og kvalitetsledelse 2024 | 9 | 109 |
| Økonomistyring 2024 | 10 | 127 |
| Jus og avtaleforhold | ukjent | ikke tilgjengelig på nett |

---

## Steg 1 – Finn authoring-nummer for et nytt kurs

Åpne kurset i Chrome og åpne DevTools (F12) → Network-fanen. Bla litt i lysbildevisningen og se etter forespørsler som inneholder `authoring/`. Nummeret etter `authoring/` er authoring-nummeret.

Alternativt: Les antall slides direkte fra siden ("Side X av Y" i lysbildevisningen) og match mot tabellen over.

---

## Steg 2 – Last ned kurs

Naviger til mappen der du vil lagre kurset og kjør:
```bash
./last_ned_kurs.sh <authoring_nr> <antall_slides> <mappenavn>
```

Eksempel:
```bash
cd ~/Downloads/GKL
./last_ned_kurs.sh 8 115 Kompetanseutvikling-2025
```

Følgende vil skje:
- Scriptet lager en mappe med navnet du oppga
- Alle slides lastes ned som JPG-filer til `mappenavn/slides/`
- Du ser `✓ Slide X/Y` for hver slide som lastes ned
- Når alle er lastet ned lages PDF-en automatisk
- Du finner `mappenavn/mappenavn.pdf` når det er ferdig

---

## Resultat

Du får en PDF med alle kurslysbilde i riktig rekkefølge, klar for offline bruk.

---

## ⚖️ Juridisk disclaimer

Dette scriptet er laget for å laste ned kursmateriell du har **lovlig tilgang til** via din innloggede konto på norskindustri.docebosaas.com.

- ✅ Kun bruk med din egen konto
- ✅ Kun til privat/faglig bruk
- ❌ Ikke del innholdet videre
- ❌ Ikke bruk scriptet for å omgå tilgangsbegrensninger du ikke har rettighet til

---

## ⚖️ Juridisk disclaimer

Dette scriptet er laget for å laste ned kursmateriell du har **lovlig kjøpt tilgang til** via din konto på norskindustri.docebosaas.com. Bruk av scriptet forutsetter at du er innlogget med gyldig konto og har betalt for tilgangen.

### Norsk lov

**Åndsverkloven (lov 15. juni 2018 nr. 40)**

- **§ 2** – Opphaveren har enerett til å råde over sitt åndsverk, herunder å fremstille eksemplar og gjøre det tilgjengelig for allmennheten.
- **§ 26 – Privatkopiering** – Enkelteksemplar av et offentliggjort verk kan fremstilles til privat bruk, forutsatt at kopieringen ikke skjer i ervervsøyemed og at eksemplaret ikke brukes til annet formål. Dette er det juridiske grunnlaget for å laste ned kurs du har lovlig tilgang til, til eget bruk.
- **§ 99 – Forbud mot omgåelse av tekniske beskyttelsessystemer** – Det er forbudt å omgå effektive tekniske beskyttelsessystemer. Dette scriptet omgår ingen slike systemer – det henter kun filer som allerede er åpent tilgjengelige på CDN uten DRM-beskyttelse.
- **§ 81 – Sanksjoner** – Brudd på åndsverkloven kan medføre krav om vederlag og erstatning. Grove eller gjentatte overtredelser kan medføre bøter eller fengsel.

**Straffeloven (lov 20. mai 2005 nr. 28)**

- **§ 202** – Ulovlig bruk av data eller dataprogram kan straffes med bøter eller fengsel inntil 2 år.

### Internasjonal lov og avtaler

**Bernkonvensjonen (1886, revidert sist 1979)**
Norge er tilsluttet Bernkonvensjonen, som gir opphavsrettsbeskyttelse i alle medlemsland automatisk. Kursmateriell produsert av Norsk Industri er beskyttet i alle 181 medlemsland.

**TRIPS-avtalen (Agreement on Trade-Related Aspects of Intellectual Property Rights, 1994)**
Administreres av WTO. Fastsetter minimumsstandarder for opphavsrettsbeskyttelse internasjonalt, inkludert for digitalt innhold.

**EU-direktiv 2001/29/EF (Infosoc-direktivet)**
Implementert i norsk rett gjennom åndsverkloven. Regulerer opphavsrett i informasjonssamfunnet, inkludert digitalt innhold og tekniske beskyttelsessystemer.

**EU-direktiv 2019/790 (DSM-direktivet – Digital Single Market)**
Moderniserer opphavsretten for den digitale tidsalderen. Norge er EØS-land og påvirkes av dette direktivet.

### Hva er lov – og hva er ikke lov

| Handling | Status |
|----------|--------|
| Laste ned kurs du har betalt for til privat bruk | ✅ Lovlig (ÅVL §26) |
| Lagre lokalt for offline bruk | ✅ Lovlig (ÅVL §26) |
| Dele PDF med kolleger | ⚠️ Grå sone – kun innen svært nær krets (ÅVL §26) |
| Distribuere til andre som ikke har betalt | ❌ Ulovlig (ÅVL §2, §81) |
| Bruke innholdet kommersielt | ❌ Ulovlig (ÅVL §2) |
| Laste ned kurs du ikke har tilgang til | ❌ Ulovlig (ÅVL §2, Strl. §202) |
| Publisere PDF åpent på nett | ❌ Ulovlig (ÅVL §2, §81) |

### Ansvarsfraskrivelse

Forfatteren av dette scriptet påtar seg intet ansvar for ulovlig bruk. Brukeren er selv ansvarlig for å sikre at bruk er i tråd med gjeldende lovverk og plattformens brukervilkår. Ved tvil, konsulter en jurist.
