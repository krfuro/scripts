"""
Last ned alle sider fra boken via nettleseren.
Kjør dette MENS boken er åpen i Chrome og du er innlogget.
"""
import asyncio
from playwright.async_api import async_playwright
import os

UNI = "2b3a0141e43b00b97dffb1bc8ece628b"
BASE = "https://angerman.no/wp-content/uploads/blafiler/full/maskiner-maskinkjoring-utg-11"
TOTAL_SIDER = 324

async def main():
    print("Starter nedlasting av boksider...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto(f"{BASE}/10/")
        print("⏳ Laster boken...")
        await page.wait_for_timeout(3000)

        for i in range(1, TOTAL_SIDER + 1):
            num = f"{i:04d}"

            svg_url = f"{BASE}/files/assets/common/page-vectorlayers/{num}.svg?uni={UNI}"
            r = await page.request.get(svg_url)
            if r.ok:
                with open(f"side{num}.svg", "wb") as f:
                    f.write(await r.body())

            jpg_url = f"{BASE}/files/assets/common/page-html5-substrates/page{num}_1.jpg?uni={UNI}"
            r = await page.request.get(jpg_url)
            if r.ok:
                with open(f"page{num}_1.jpg", "wb") as f:
                    f.write(await r.body())

            print(f"✓ Side {i}/{TOTAL_SIDER}")

        await browser.close()
    print("✅ Alle sider lastet ned!")

asyncio.run(main())
