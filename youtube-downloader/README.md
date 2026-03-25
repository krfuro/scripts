# YouTube Downloader

Last ned YouTube-videoer i beste kvalitet som MP4-filer.

---

## Før du starter – installer nødvendig program

Åpne terminalen og kjør:
```bash
brew install yt-dlp
```

Dette installerer `yt-dlp` – et verktøy for å laste ned videoer fra YouTube og mange andre nettsteder.

---

## Bruksmåte

### Alternativ 1 – Last ned videoer fra listen i scriptet

Åpne `last_ned_videoer.py` og legg til URL-er i `VIDEOER`-listen øverst. Naviger deretter til mappen der du vil lagre videoene og kjør:

```bash
python3 /sti/til/last_ned_videoer.py
```

Følgende vil skje:
- Scriptet leser URL-listen og starter nedlasting én etter én
- Hver video lastes ned i beste tilgjengelige kvalitet
- Video og lyd slås automatisk sammen til én MP4-fil
- Filnavnet settes automatisk til videotittelen fra YouTube
- Du ser fremdrift i terminalen for hver video
- Når alt er ferdig vises `✅ Alle videoer lastet ned!`

### Alternativ 2 – Send URL-er direkte som argumenter

```bash
python3 last_ned_videoer.py "https://www.youtube.com/watch?v=XXXX" "https://www.youtube.com/watch?v=YYYY"
```

### Alternativ 3 – Bruk yt-dlp direkte uten script

```bash
yt-dlp -f "bestvideo+bestaudio" --merge-output-format mp4 -o "%(title)s.%(ext)s" "URL"
```

---

## Tips

- Naviger alltid til riktig mappe før du kjører scriptet — videoene lagres der du er
- Google-søkelenker og spillelister kan ikke lastes ned på samme måte som direktelenker
- Hvis en video feiler, prøv å oppdatere yt-dlp: `brew upgrade yt-dlp`

---

## Eksempel – Anleggsmaskinførerkurs

Videoer fra kurset (Bjørn Lyng / cada.no) ble lastet ned til:
```
~/Documents/Skole/Anleggsmaskinførerkurs/
```

Med kommandoen:
```bash
cd ~/Documents/Skole/Anleggsmaskinførerkurs
python3 last_ned_videoer.py \
  "https://www.youtube.com/watch?v=TK41ynf3GBI" \
  "https://www.youtube.com/watch?v=25oZv_3SgSE" \
  "https://youtu.be/Xvlk_73bSvc" \
  "https://www.youtube.com/watch?v=nzyqw2YytZE" \
  "https://www.youtube.com/watch?v=DvKtkVsUFSE" \
  "https://www.youtube.com/watch?v=3W4IuP9uQu4" \
  "https://www.youtube.com/watch?v=26hooxzCGkY" \
  "https://www.youtube.com/watch?v=jxF-r4RbqPk" \
  "https://www.youtube.com/watch?v=qE8nTn8FGIA"
```

---

## ⚖️ Juridisk disclaimer

Nedlasting av YouTube-videoer berører både norsk og internasjonal opphavsrett, samt YouTubes egne brukervilkår.

### Norsk lov

**Åndsverkloven (lov 15. juni 2018 nr. 40)**

- **§ 2** – Opphaveren har enerett til å råde over sitt åndsverk, herunder å fremstille eksemplar og gjøre det tilgjengelig for allmennheten.
- **§ 26 – Privatkopiering** – Enkelteksemplar av et offentliggjort verk kan fremstilles til privat bruk, forutsatt at kopieringen ikke skjer i ervervsøyemed og at eksemplaret ikke brukes til annet formål. Privatkopiering fra lovlige kilder til eget bruk er tillatt.
- **§ 99 – Forbud mot omgåelse av tekniske beskyttelsessystemer** – Det er forbudt å omgå effektive tekniske beskyttelsessystemer. yt-dlp omgår ingen DRM, men laster ned fra åpne videostrømmer.
- **§ 81 – Sanksjoner** – Brudd på åndsverkloven kan medføre krav om vederlag og erstatning. Grove eller gjentatte overtredelser kan medføre bøter eller fengsel.

**Straffeloven (lov 20. mai 2005 nr. 28)**

- **§ 202** – Ulovlig bruk av data eller dataprogram kan straffes med bøter eller fengsel inntil 2 år.

### Internasjonal lov og avtaler

**Bernkonvensjonen (1886, revidert sist 1979)**
Norge er tilsluttet Bernkonvensjonen, som gir opphavsrettsbeskyttelse i alle 181 medlemsland automatisk. Videoinnhold er beskyttet internasjonalt.

**TRIPS-avtalen (Agreement on Trade-Related Aspects of Intellectual Property Rights, 1994)**
Administreres av WTO. Fastsetter minimumsstandarder for opphavsrettsbeskyttelse internasjonalt, inkludert for digitalt innhold.

**EU-direktiv 2001/29/EF (Infosoc-direktivet)**
Implementert i norsk rett gjennom åndsverkloven. Regulerer opphavsrett i informasjonssamfunnet.

**EU-direktiv 2019/790 (DSM-direktivet – Digital Single Market)**
Moderniserer opphavsretten for den digitale tidsalderen. Norge er EØS-land og påvirkes av dette direktivet.

### YouTubes brukervilkår

YouTubes Terms of Service forbyr nedlasting av videoer uten eksplisitt tillatelse fra YouTube, med mindre:
- YouTube selv tilbyr en nedlastingsfunksjon (f.eks. YouTube Premium)
- Videoen er lisensiert under Creative Commons eller lignende
- Du har fått skriftlig tillatelse fra rettighetshaveren

Bruk av yt-dlp kan derfor teknisk sett være i strid med YouTubes brukervilkår, selv om innholdet er lovlig tilgjengelig.

### Hva er lov – og hva er ikke lov

| Handling | Status |
|----------|--------|
| Laste ned egne videoer du har lastet opp | ✅ Lovlig |
| Laste ned Creative Commons-lisensierte videoer | ✅ Lovlig |
| Laste ned til privat bruk (ÅVL §26) | ⚠️ Grå sone – lovlig etter norsk lov, men mot YouTubes vilkår |
| Dele nedlastede videoer med andre | ❌ Ulovlig (ÅVL §2, §81) |
| Bruke nedlastet innhold kommersielt | ❌ Ulovlig (ÅVL §2) |
| Publisere nedlastede videoer på nytt | ❌ Ulovlig (ÅVL §2, §81) |

### Ansvarsfraskrivelse

Forfatteren av dette scriptet påtar seg intet ansvar for ulovlig bruk. Brukeren er selv ansvarlig for å sikre at bruken er i tråd med gjeldende lovverk og plattformens brukervilkår. Ved tvil, konsulter en jurist.
