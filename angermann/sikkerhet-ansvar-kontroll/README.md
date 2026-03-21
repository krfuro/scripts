# Sikkerhet, ansvar og kontroll – utg. 19

Laster ned og lager PDF av læreboken fra angerman.no.

## Krav
```bash
pip3 install playwright pypdf
python3 -m playwright install chromium
```

## Steg 1 – Last ned boksidene

Kjør `last_ned_sider.py` fra arbeidsmappen din:
```bash
python3 last_ned_sider.py
```

Følgende vil skje:
- En Chrome-nettleser åpnes automatisk
- Boken lastes inn (du må være logget inn på angerman.no fra før)
- Scriptet laster ned alle 112 sider som to filer per side:
  - `side0001.svg` – tekstlaget (søkbar tekst, vektorgrafik)
  - `page0001_1.jpg` – bakgrunnsbilde (bilder og illustrasjoner)
- Filene lagres direkte i arbeidsmappen
- Nettleseren lukkes automatisk når alt er ferdig

## Steg 2 – Lag PDF

Kjør `lag_pdf.py` fra samme mappe:
```bash
python3 lag_pdf.py
```

Følgende vil skje:
- Scriptet finner automatisk alle nedlastede sider i mappen
- Hver side bygges opp ved å legge SVG-tekstlaget oppå JPG-bakgrunnen
- Sidene slås sammen til én PDF-fil
- Du får `sikkerhet-ansvar-kontroll.pdf` i mappen når det er ferdig

## Info
- 112 sider totalt
- uni-nøkkel: `c8fa0e9d753f575f88b7fec412b95894`
- URL: https://angerman.no/wp-content/uploads/blafiler/full/sikkerhet-ansvar-kontroll-utgave-19/
