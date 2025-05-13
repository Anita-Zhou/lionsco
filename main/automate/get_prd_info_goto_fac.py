import asyncio
import json
from playwright.async_api import async_playwright

COOKIE_FILE = "1688_cookies.json"

async def get_fixed_info(page, field):
    try:
        if field == "商家名字":
            return await page.eval_on_selector(
                "#pc_card_baseinfo > div > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)",
                "el => el.textContent.trim()"
            )
    except Exception as e:
        print(f"Error getting {field}:", e)
        return ""

async def extract_info_with_cookies(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        context = await browser.new_context()

        # 加载 cookies
        with open(COOKIE_FILE, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        await context.add_cookies(cookies)

        page = await context.new_page()
        await page.goto(url)
        print("自动加载 Cookies 进入页面：", url)
        await page.wait_for_load_state('networkidle')
        print("页面加载完成")

        # 1. Get the image with ind="1" and class="detail-gallery-img"
        image_elem = await page.query_selector('img.detail-gallery-img[ind="1"]')
        image_url = await image_elem.get_attribute('src') if image_elem else None
        print("Image URL:", image_url)

        # 2. Get the product title text
        title_elem = await page.query_selector('div.title-text')
        title_text = await title_elem.inner_text() if title_elem else None
        print("Title:", title_text)

        # 3. Find the tab and click it — but wait for new page (tab) to open
        credit_tab = await page.query_selector('li.creditdetail')
        if credit_tab:
            # Wait for popup triggered by the click
            async with context.expect_page() as new_page_info:
                await credit_tab.click()
            new_page = await new_page_info.value
            await new_page.wait_for_load_state('networkidle')
            await new_page.wait_for_timeout(500)  # Wait to be sure everything loads

            factory_url = new_page.url
            print("Factory URL (new tab):", factory_url)
        else:
            print("Credit detail tab not found.")

        await context.close()
        await browser.close()

if __name__ == "__main__":
    url = input("请输入一个网页链接: ").strip()
    asyncio.run(extract_info_with_cookies(url))
