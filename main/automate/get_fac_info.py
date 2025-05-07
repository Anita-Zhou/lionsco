import asyncio
import pandas as pd
from playwright.async_api import async_playwright

# 固定字段的抓取方式
async def get_fixed_info(page, field):
    try:
        if field == "商家名字":
            return await page.eval_on_selector(
                "#pc_card_baseinfo > div > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)",
                "el => el.textContent.trim()"
            )
        elif field == "认证":
            certs_div = "#pc_card_baseinfo > div > div > div:nth-child(2) > div:nth-child(3) > div"
            await page.wait_for_selector(certs_div, timeout=10000)
            return await page.eval_on_selector_all(
                f"{certs_div} > div",
                "els => els.map(el => el.textContent.trim()).join(', ')"
            )
        elif field == "地点":
            return await page.eval_on_selector(
                "#pc_card_baseinfo > div > div > div:nth-child(2) > div:nth-child(4) > a > span:nth-child(2)",
                "el => el.textContent.trim()"
            )
    except:
        return ""
    return ""

# 模糊匹配字段的抓取方式
async def get_info_by_key_elements(page, key_text):
    try:
        keys = await page.query_selector_all(".ability_key")
        for key_el in keys:
            text = await key_el.text_content()
            if text and key_text in text.strip():
                parent = await key_el.evaluate_handle("el => el.parentElement")
                value_el = await parent.query_selector(".ability_value")
                if value_el:
                    value = await value_el.text_content()
                    return value.strip()
    except:
        return ""
    return ""

# 针对一个 URL 抓取所有列
async def scrape_row(url, fieldnames):
    result = {"URL": url}
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=30000)

            await page.wait_for_selector("#pc_card_exhibition", timeout=10000)
            await page.wait_for_selector("#pc_card_baseinfo", timeout=10000)

            for field in fieldnames:
                if field == "URL":
                    continue
                elif field in ["商家名字", "认证", "地点"]:
                    value = await get_fixed_info(page, field)
                else:
                    value = await get_info_by_key_elements(page, field)
                result[field] = value

            await browser.close()
    except Exception as e:
        print(f"抓取失败: {url}\n原因: {e}")
        for field in fieldnames:
            if field not in result:
                result[field] = ""
    return result

# 批量抓取协程
async def scrape_all(urls, fieldnames):
    return await asyncio.gather(*[scrape_row(url, fieldnames) for url in urls])

# 主函数：询问路径和标题行
def main_dynamic_fields():
    input_csv = input("请输入 CSV 文件路径）：").strip()
    if not input_csv:
        print("未输入文件路径，程序终止。")
        return

    try:
        header_input = input("请输入标题行的行号（例如第2行请输入 2）：").strip()
        header_idx = int(header_input) - 1
    except ValueError:
        print("标题行输入无效，程序终止。")
        return

    try:
        df = pd.read_csv(input_csv, header=header_idx)
    except Exception as e:
        print(f"无法读取 CSV 文件：{e}")
        return

    fieldnames = df.columns.tolist()
    if "URL" not in fieldnames:
        print("CSV 中未找到 'URL' 列")
        return

    urls = df["URL"].dropna().tolist()
    print(f"共 {len(urls)} 个链接，开始抓取中…")

    results = asyncio.run(scrape_all(urls, fieldnames))

    result_df = pd.DataFrame(results)
    output_csv = "供应商信息_结果.csv"
    result_df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"抓取完成，已保存为：{output_csv}")

if __name__ == "__main__":
    main_dynamic_fields()
