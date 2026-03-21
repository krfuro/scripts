# Maskiner og maskinkjøring – utg. 11

Laster ned og lager PDF av læreboken fra angerman.no.

## Krav
```bash
pip3 install playwright pypdf
python3 -m playwright install chromium
```

## Steg 1 – Last ned boksidene
Åpne boken i Chrome mens du er logget inn på angerman.no:
👉 https://angerman.no/wp-content/uploads/blafiler/full/maskiner-maskinkjoring-utg-11/

Kjør nedlastingsscriptet fra arbeidsmappen din:
```javascript
async function lastNedBolk(fra, til) {
    const BASE = "https://angerman.no/wp-content/uploads/blafiler/full/maskiner-maskinkjoring-utg-11/files/assets/common/";
    const UNI = "?uni=2b3a0141e43b00b97dffb1bc8ece628b";
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
await lastNedBolk(81, 160);
await lastNedBolk(161, 240);
await lastNedBolk(241, 324);
```

## Steg 2 – Flytt filer og lag PDF
```bash
mkdir ~/bok2 && mv ~/Downloads/side*.svg ~/Downloads/page*_1.jpg ~/bok2/
cd ~/bok2
cp /sti/til/lag_pdf.py .
python3 lag_pdf.py
```

Ferdig! Du finner `maskiner-maskinkjoring.pdf` i mappen.

## Info
- 324 sider totalt
- uni-nøkkel: `2b3a0141e43b00b97dffb1bc8ece628b`
