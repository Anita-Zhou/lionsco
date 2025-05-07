import asyncio
import csv
from playwright.async_api import async_playwright

def read_urls_from_excel(excel_path):
    wb = openpyxl.load_workbook(excel_path)
    ws = wb.active

    # 假设 "URL" 列在第一行标题中，找到它的列号
    header_idx = input("请输入一个标题行的索引: ").strip()
    header = [cell.value for cell in ws[header_idx]]  # +1 因为 openpyxl 是从1开始计数
    url_col_index = header.index("URL") + 1  # openpyxl 是从1开始计数

    urls = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        url = row[url_col_index - 1]
        if url:
            urls.append(url.strip())
    return urls

async def scrape_company_info(url, output_file="output.csv"):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        # 等待所需元素加载
        await page.wait_for_selector("#pc_card_exhibition")
        await page.wait_for_selector("#pc_card_baseinfo")

        # 4. 工厂名称
        factory_name = await page.eval_on_selector(
            "#pc_card_baseinfo > div > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)",
            "el => el.textContent.trim()"
        )

        # 1. 成立时间
        established = await page.eval_on_selector(
            "#pc_card_exhibition > div > div:nth-child(3) > div.ability_info > div:nth-child(1) > span.ability_value",
            "el => el.textContent.trim()"
        )

        # 2. 员工人数
        employees = await page.eval_on_selector(
            "#pc_card_exhibition > div > div:nth-child(3) > div.ability_info > div:nth-child(4) > span.ability_value",
            "el => el.textContent.trim()"
        )

        # 3. 资质/标签
        certs_div = "#pc_card_baseinfo > div > div > div:nth-child(2) > div:nth-child(3) > div"
        await page.wait_for_selector(certs_div)
        certs = await page.eval_on_selector_all(
            f"{certs_div} > div",
            "els => els.map(el => el.textContent.trim()).join(', ')"
        )

        await browser.close()

        # 写入 CSV
        with open(output_file, mode='w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["URL", "工厂名称", "成立时间", "员工人数", "资质/标签"])
            writer.writerow([url, factory_name, established, employees, certs])

        print(f"数据已保存到 {output_file}")

# 调用
if __name__ == "__main__":
    url = input("请输入一个网页链接: ").strip()
    asyncio.run(scrape_company_info(url))