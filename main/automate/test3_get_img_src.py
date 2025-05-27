import asyncio
import pandas as pd
from playwright.async_api import async_playwright

CONSUMER_COUNT = 5  # Number of parallel browser tasks

async def get_amazon_image(page, asin):
    url = f"https://www.amazon.com/dp/{asin}/?th=1"
    try:
        await page.goto(url, timeout=60000)
        await page.wait_for_selector("#landingImage", timeout=15000)
        return await page.get_attribute("#landingImage", "src")
    except Exception as e:
        print(f"Failed to fetch image for ASIN {asin}: {e}")
        return None

def extract_asins_from_csv(file_path, column_name="ASIN"):
    try:
        df = pd.read_csv(file_path, skiprows=1, encoding='gb18030')
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in CSV.")
        return df, df[column_name].dropna().astype(str).tolist()
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None, []

async def consumer(queue, result_dict, context):
    page = await context.new_page()
    while True:
        asin = await queue.get()
        if asin is None:
            break
        img_src = await get_amazon_image(page, asin)
        result_dict[asin] = img_src
        queue.task_done()
    await page.close()

async def main():
    file_path = input("请输入你要提取的文件: ").strip()
    df, asins = extract_asins_from_csv(file_path)
    if not asins:
        print("未找到任何ASIN。")
        return

    queue = asyncio.Queue()
    for asin in asins:
        await queue.put(asin)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/90.0.4430.212 Safari/537.36"
        ))

        result_dict = {}
        consumers = [asyncio.create_task(consumer(queue, result_dict, context)) for _ in range(CONSUMER_COUNT)]

        await queue.join()
        for _ in range(CONSUMER_COUNT):
            await queue.put(None)
        await asyncio.gather(*consumers)
        await browser.close()

    # Insert image URLs into the original dataframe
    asin_col_index = df.columns.get_loc("ASIN")
    df.insert(asin_col_index + 1, "ImageURL", df["ASIN"].map(result_dict))

    # Save to new CSV
    output_path = file_path.replace(".csv", "_with_images.csv")
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"已保存结果至: {output_path}")

if __name__ == "__main__":
    asyncio.run(main())
