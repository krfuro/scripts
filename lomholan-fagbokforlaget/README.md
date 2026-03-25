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
