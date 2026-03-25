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
