"""
Last ned alle sider fra boken via nettleseren.
Kjør dette MENS boken er åpen i Chrome og du er innlogget.
"""
import asyncio
from playwright.async_api import async_playwright
import os

UNI = "c8fa0e9d753f575f88b7fec412b95894"
BASE = "https://angerman.no/wp-content/uploads/blafiler/full/sikkerhet-ansvar-kontroll-utgave-19"
TOTAL_SIDER = 112

async def main():
    print("Starter nedlasting av boksider...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Logg inn og naviger til boken
        await page.goto(f"{BASE}/10/")
        print("⏳ Logger inn og laster boken...")
        await page.wait_for_timeout(3000)

        os.makedirs(".", exist_ok=True)

        for i in range(1, TOTAL_SIDER + 1):
            num = f"{i:04d}"

            # Last ned SVG
            svg_url = f"{BASE}/files/assets/common/page-vectorlayers/{num}.svg?uni={UNI}"
            r = await page.request.get(svg_url)
            if r.ok:
                with open(f"side{num}.svg", "wb") as f:
                    f.write(await r.body())

            # Last ned JPG
            jpg_url = f"{BASE}/files/assets/common/page-html5-substrates/page{num}_1.jpg?uni={UNI}"
            r = await page.request.get(jpg_url)
            if r.ok:
                with open(f"page{num}_1.jpg", "wb") as f:
                    f.write(await r.body())

            print(f"✓ Side {i}/{TOTAL_SIDER}")

        await browser.close()
    print("✅ Alle sider lastet ned!")

asyncio.run(main())
