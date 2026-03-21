# Sikkerhet, ansvar og kontroll – utg. 19

Laster ned og lager PDF av læreboken fra angerman.no.

## Krav
```bash
pip3 install playwright pypdf
python3 -m playwright install chromium
```

## Steg 1 – Last ned boksidene
Åpne boken i Chrome mens du er logget inn på angerman.no:
👉 https://angerman.no/wp-content/uploads/blafiler/full/sikkerhet-ansvar-kontroll-utgave-19/

Åpne DevTools → Console (F12) og lim inn og kjør dette i bolker:
```javascript
async function lastNedBolk(fra, til) {
    const BASE = "https://angerman.no/wp-content/uploads/blafiler/full/sikkerhet-ansvar-kontroll-utgave-19/files/assets/common/";
    const UNI = "?uni=c8fa0e9d753f575f88b7fec412b95894";
    for (let i = fra; i <= til; i++) {
        const num = String(i).padStart(4, '0');
        for (const [url, navn] of [
            [`${BASE}page-vectorlayers/${num}.svg${UNI}`, `side${num}.svg`],
            [`${BASE}page-html5-substrates/page${num}_1.jpg${UNI}`, `page${num}_1.jpg`]
        ]) {
            const r = await fetch(url);
            if (r.ok) {
                const a = document.createElement('a');
                a.href = URL.createObjectURL(await r.blob());
                a.download = navn; a.click();
                URL.revokeObjectURL(a.href);
            }
            await new Promise(res => setTimeout(res, 150));
        }
    }
    return 'Ferdig!';
}
await lastNedBolk(1, 80);
await lastNedBolk(81, 112);
```

## Steg 2 – Flytt filer og lag PDF
```bash
mkdir ~/bok1 && mv ~/Downloads/side*.svg ~/Downloads/page*_1.jpg ~/bok1/
cd ~/bok1
cp /sti/til/lag_pdf.py .
python3 lag_pdf.py
```

Ferdig! Du finner `sikkerhet-ansvar-kontroll.pdf` i mappen.

## Info
- 112 sider totalt
- uni-nøkkel: `c8fa0e9d753f575f88b7fec412b95894`
