import asyncio
from playwright.async_api import async_playwright
import pandas as pd

async def get_amazon_image(page, asin):
    url = f"https://www.amazon.com/dp/{asin}/?th=1"
    try:
        await page.goto(url, timeout=60000)
        await page.wait_for_selector("#landingImage", timeout=15000)
        img_src = await page.get_attribute("#landingImage", "src")
        print(f"ASIN: {asin}\nImage URL: {img_src}\n")
    except Exception as e:
        print(f"Failed to fetch image for ASIN {asin}: {e}")

def extract_asins_from_csv(file_path, column_name="ASIN"):
    try:
        df = pd.read_csv(file_path, skiprows=1, encoding='gb18030')
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in CSV.")
        return df[column_name].dropna().astype(str).tolist()
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []

async def main():
    file_path = input("请输入你要提取的文件: ").strip()
    asins = extract_asins_from_csv(file_path)

    print("提取到的ASIN列表：")
    for asin in asins:
        print(asin)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/90.0.4430.212 Safari/537.36"
        ))
        page = await context.new_page()

        for asin in asins:
            await get_amazon_image(page, asin)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
