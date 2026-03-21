# Maskiner og maskinkjøring – utg. 11

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
- Scriptet laster ned alle 324 sider som to filer per side:
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
- Du får `maskiner-maskinkjoring.pdf` i mappen når det er ferdig

## Info
- 324 sider totalt
- uni-nøkkel: `2b3a0141e43b00b97dffb1bc8ece628b`
- URL: https://angerman.no/wp-content/uploads/blafiler/full/maskiner-maskinkjoring-utg-11/
