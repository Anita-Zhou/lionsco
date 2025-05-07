import asyncio
from playwright.async_api import async_playwright

async def get_info_by_key(url, key_text):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_selector(".ability_key")

        # 拿到所有 .ability_key 元素
        keys = await page.query_selector_all(".ability_key")
        if not keys:
            print("⚠️ 未找到任何信息")
            await browser.close()
            return None
        print(f"找到 {len(keys)} 个信息项")
        print("keys...")
        print(keys)

        for key_el in keys:
            text = await key_el.text_content()
            if text.strip() == key_text:
                parent = await key_el.evaluate_handle("el => el.parentElement")
                value_el = await parent.query_selector(".ability_value")
                if value_el:
                    value = await value_el.text_content()
                    print(f"{key_text}: {value.strip()}")
                    return value.strip()

        print(f"未找到“{key_text}”对应的值")
        return None

# 示例用法
if __name__ == "__main__":
    url = "https://www.1688.com/factory/b2b-38940712729362b.html"
    asyncio.run(get_info_by_key(url, "员工总数"))
