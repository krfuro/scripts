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
