import asyncio
from playwright.async_api import async_playwright
import pandas as pd

async def get_amazon_image(asin):
    url = f"https://www.amazon.com/dp/{asin}/?th=1"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/90.0.4430.212 Safari/537.36"
        ))
        page = await context.new_page()
        await page.goto(url)

        # Wait for the landing image to appear
        await page.wait_for_selector("#landingImage")

        # Extract the src attribute of the main image
        img_src = await page.get_attribute("#landingImage", "src")
        print(f"ASIN: {asin}")
        print(f"Image URL: {img_src}")

        await browser.close()

def extract_asins_from_csv(file_path, column_name="ASIN"):
    try:
        df = pd.read_csv(file_path, skiprows=1, encoding='gb18030')
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in CSV.")
        asins = df[column_name].dropna().astype(str).tolist()
        return asins
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []

if __name__ == "__main__":
    # Example usage of extract_urls_from_csv
    file_path = input("请输入你要提取的文件: ").strip()
    # Extract URLs from CSV
    asins = extract_asins_from_csv(file_path)

    # TEST：Print extracted URLs
    print("提取到的链接列表：")
    for asin in asins:
        print(asin)
        asyncio.run(get_amazon_image(asin))


    
    

# # Example
# asin = "B0CTS8VQ85"
# asyncio.run(get_amazon_image(asin))
