
if __name__ == "__main__":
    url = input("请输入一个网页链接: ").strip()
    asyncio.run(scrape_company_info(url))