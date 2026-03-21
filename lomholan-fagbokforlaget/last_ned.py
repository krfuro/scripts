import asyncio
import os
import httpx
from playwright.async_api import async_playwright

NAMESPACE = "65758e40-59ac-4e2b-8b7b-3d44e37b5114"
FILER = [
    "organisasjon-og-ledelse",
    "okonomistyring",
    "markedsforingsledelse",
]
DOWNLOAD_DIR = "lomholan_filer"
HEADERS = {
    "referer": "https://lomholan.fagbokforlaget.no/",
    "user-agent": "Mozilla/5.0"
}

async def main():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    asset_ids = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        async def handle_request(request):
            url = request.url
            if f"api.edtech.fagbokforlaget.no/assets/{NAMESPACE}/" in url:
                fil_id = url.split("/")[-1]
                if fil_id not in asset_ids:
                    print(f"  Fant asset-ID: {fil_id}")
                    asset_ids.add(fil_id)

        page.on("request", handle_request)

        for fag in FILER:
            for kap in range(1, 20):
                url = f"https://lomholan.fagbokforlaget.no/k/{fag}?contentType=all&paths={fag}/kapittel-{kap}"
                print(f"\nSkanner: {fag} / kapittel-{kap}")
                try:
                    await page.goto(url, wait_until="networkidle", timeout=20000)
                    await page.wait_for_timeout(1500)
                    await page.evaluate("document.querySelector('fbf-vue-cookie-modal')?.remove()")
                    buttons = await page.query_selector_all(".c-card-file__download-button")
                    if buttons:
                        print(f"  Fant {len(buttons)} fil(er)")
                        for btn in buttons:
                            await btn.click(timeout=5000)
                            await page.wait_for_timeout(1500)
                except Exception as e:
                    print(f"  Feil: {e}")

        await browser.close()

    print(f"\nFant totalt {len(asset_ids)} filer. Starter nedlasting...")

    async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True) as client:
        for fil_id in asset_ids:
            api_url = f"https://api.edtech.fagbokforlaget.no/assets/{NAMESPACE}/{fil_id}"
            try:
                r = await client.get(api_url)
                data = r.json()
                filnavn = data.get("filename", fil_id)
                download_url = data.get("url")
                if not download_url:
                    print(f"  Ingen URL for {filnavn}")
                    continue
                print(f"Laster ned: {filnavn}")
                fil = await client.get(download_url)
                filepath = os.path.join(DOWNLOAD_DIR, filnavn)
                with open(filepath, "wb") as f:
                    f.write(fil.content)
                print(f"  Lagret: {filepath}")
            except Exception as e:
                print(f"  Feil ved {fil_id}: {e}")

    print(f"\nFerdig! Filer lagret i '{DOWNLOAD_DIR}/'")

asyncio.run(main())
