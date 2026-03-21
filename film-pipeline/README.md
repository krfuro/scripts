# Film-pipeline – MakeMKV → HandBrake → Plex

Samling av scripts for å rippe, rydde og klargjøre filmer fra ISO til Plex-klar MP4.

---

## Før du starter – installer nødvendige programmer

- **MakeMKV** – https://www.makemkv.com – ripper ISO til MKV
- **HandBrake** – https://handbrake.fr – konverterer MKV til MP4

---

## Anbefalt rekkefølge
```
1. Rip_ISO_above_1_3GB-WORKING.command    ← ripp ISO til MKV
2. Pipeline_Cleanup_Rename_Flatten.command ← rydd og klargjør
3. HandBrake (manuelt via GUI inntil videre)
4. Plex skanner inn filene automatisk
```

---

## Script-oversikt

### 1. Rip_ISO-WORKING.command
Ripper **alle** titler fra ISO-filer til MKV via MakeMKV.

Følgende vil skje:
- Scriptet finner alle `.iso`-filer i mappen det ligger i
- Lager en undermappe per film under `RIPS/`
- Ripper alle titler fra hver ISO til MKV-format
- Logger hele prosessen til en loggfil med tidsstempel
- Viser `OK` eller `FEIL` for hver fil når den er ferdig

---

### 2. Rip_ISO_above_1_3GB-WORKING.command
Smartere versjon – ripper kun titler over 1,3 GiB (filtrerer bort reklame og bonusmateriale).

Følgende vil skje:
- Analyserer hver ISO og lister titler med varighet og størrelse
- Ripper automatisk alle titler >= 1,3 GiB
- Hvis ingen titler er store nok, vises en tabell og du kan velge manuelt:
  - `all` – ripp alt
  - `0,1,2` – ripp spesifikke titler
  - `skip` – hopp over denne ISO-en
- Sender Mac-varsling når alt er ferdig
- Hindrer Mac fra å sove under ripping (`caffeinate`)

---

### 3. Cleanup_Keep_Largest.command
Rydder opp i rippa filer – beholder kun hovedfilmen.

Følgende vil skje:
- Går gjennom hver filmmappe
- Beholder den største videofilen (mkv/mp4/m4v/avi/m2ts/ts/vob)
- Flytter alt annet (reklame, trailere, småfiler) til Papirkurven
- Skriver ut hva som beholdes og hva som kastes

---

### 4. Flatten_RIPS.command
Rydder mappestruktur – flytter MKV-filer ut av undermapper.

Følgende vil skje:
- Finner alle `.mkv`-filer i undermapper
- Flytter dem opp til rotmappen
- Sletter tomme undermapper
- Fjerner `.DS_Store`-filer

---

### 5. Pipeline_Cleanup_Rename_Flatten.command
Alt-i-ett pipeline – kjør denne etter ripping for å klargjøre til HandBrake.

Følgende vil skje:
1. **Cleanup** – beholder kun største videofil per mappe
2. **Rename** – gir filen samme navn som mappen
3. **Flatten** – flytter filen til rotmappen og sletter tom undermappe

> Dette er hovedscriptet du bruker mellom ripping og HandBrake.

---

### 6. HandBrake_Batch_MKV_to_MP4.command ⚠️ BETA – ikke ferdigstilt

Dette scriptet er under utvikling og skal på sikt batch-konvertere MKV til MP4 via HandBrakeCLI. **Ikke bruk dette i produksjon ennå.**

---

## HandBrake-preset

Filen `MakeMKV_to_Plex_AllTracks.json` er et HandBrake-preset optimalisert for Plex:
- **Format:** MP4
- **Video:** x264, 1080p, CRF 22
- **Lyd:** Alle spor beholdes (AAC, AC3, EAC3, DTS)
- **Teksting:** Alle spor beholdes, norsk og engelsk prioritert
- **Kapitler:** Beholdes

### Importer presetet i HandBrake:
1. Åpne HandBrake
2. Velg `Presets` → `Import from file`
3. Velg `MakeMKV_to_Plex_AllTracks.json`

---

## Praktisk bruk

Alle scripts er laget for å **dobbelklikkes** i Finder:
1. Kopier ønsket `.command`-fil inn i mappen du vil jobbe i
2. Dobbelklikk scriptet
3. Et terminalvindu åpnes og viser fremdrift

> Første gang må du kanskje høyreklikke → Åpne for å godkjenne scriptet i macOS.

---

## Mappestruktur eksempel
```
Movies/backup/
├── Film1.iso
├── Film2.iso
├── RIPS/
│   ├── Film1/
│   │   └── Film1.mkv
│   └── Film2/
│       └── Film2.mkv
└── MP4/
    ├── Film1.mp4
    └── Film2.mp4
```

---

## ⚖️ Juridisk disclaimer

Dette scriptet er laget for **privat sikkerhetskopiering av egeneide fysiske medier** (DVD/Blu-ray).

Etter norsk **Åndsverkloven §26** er kopiering til privat bruk tillatt, forutsatt at:
- ✅ Du eier den fysiske DVD-en du ripper
- ✅ Kopien kun brukes privat (ikke deles, selges eller distribueres)
- ✅ Kopien ikke gjøres tilgjengelig for andre enn nær familie/omgangskrets

**Merk:** Omgåelse av kopibeskyttelse (DRM) på DVD er en juridisk grå sone i Norge. Loven tillater privatkopiering, men beskytter samtidig tekniske sperrer. Bruk scriptet på eget ansvar.

Dette scriptet er **ikke** laget for eller ment til:
- ❌ Kopiering av lånte, leide eller piratkopierte medier
- ❌ Distribusjon eller deling av kopier
- ❌ Kommersiell bruk
