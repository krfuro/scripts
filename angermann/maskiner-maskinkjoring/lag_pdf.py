import asyncio
from playwright.async_api import async_playwright
import glob, os, re
from pypdf import PdfWriter, PdfReader

BASE = "https://angerman.no/wp-content/uploads/blafiler/full/maskiner-maskinkjoring-utg-11"
os.makedirs("sider_pdf", exist_ok=True)

async def main():
    jpg_numre = set(re.search(r'page(\d+)_1\.jpg', f).group(1) for f in glob.glob('page*_1.jpg'))
    svg_numre = set(re.search(r'side(\d+)\.svg', f).group(1) for f in glob.glob('side*.svg'))
    alle_numre = sorted(jpg_numre | svg_numre)
    print(f"Fant {len(alle_numre)} unike sider")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"{BASE}/10/")
        await page.wait_for_timeout(2000)

        for num in alle_numre:
            jpg = f"page{num}_1.jpg"
            svg = f"side{num}.svg"
            pdf_ut = f"sider_pdf/{num}.pdf"
            jpg_finnes = os.path.exists(jpg)
            svg_finnes = os.path.exists(svg)
            bakgrunn = f"<img class='bakgrunn' src='file://{os.path.abspath(jpg)}'>" if jpg_finnes else ""
            tekst = f"<img class='tekst' src='file://{os.path.abspath(svg)}'>" if svg_finnes else ""
            html = f"""<!DOCTYPE html>
<html><head><style>
  * {{ margin:0; padding:0; }}
  body {{ width:595px; height:842px; overflow:hidden; position:relative; background:white; }}
  .bakgrunn {{ position:absolute; top:0; left:0; width:595px; height:842px; }}
  .tekst {{ position:absolute; top:0; left:0; width:595px; height:842px; }}
</style></head><body>{bakgrunn}{tekst}</body></html>"""
            html_fil = f"/tmp/side_{num}.html"
            with open(html_fil, "w") as f:
                f.write(html)
            await page.goto(f"file://{html_fil}")
            await page.wait_for_timeout(300)
            pdf_bytes = await page.pdf(
                width="595px", height="842px",
                print_background=True,
                margin={"top":"0","bottom":"0","left":"0","right":"0"}
            )
            with open(pdf_ut, "wb") as f:
                f.write(pdf_bytes)
            print(f"✓ Side {num}" + ("" if svg_finnes else " (blank)"))

        await browser.close()

    writer = PdfWriter()
    for p in sorted(glob.glob("sider_pdf/*.pdf")):
        for side in PdfReader(p).pages:
            writer.add_page(side)
    with open("maskiner-maskinkjoring.pdf", "wb") as f:
        writer.write(f)
    print("✅ Ferdig! → maskiner-maskinkjoring.pdf")

asyncio.run(main())
