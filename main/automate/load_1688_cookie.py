import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

COOKIE_FILE = "1688_cookies.json"

async def login_and_save_cookies():
    user_data_dir = str(Path.home() / "AppData/Local/Google/Chrome/User Data")  # Windows路径
    profile = "Default"  # 或 "Profile 1"

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=f"{user_data_dir}/{profile}",
            headless=False,
            slow_mo=50
        )
        page = await context.new_page()
        await page.goto("https://detail.1688.com/")
        print("请手动完成登录 & 验证...")

        input("登录完成后按下回车保存 cookies：")

        cookies = await context.cookies()
        with open(COOKIE_FILE, "w", encoding="utf-8") as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)

        print(f"Cookies 已保存到 {COOKIE_FILE}")
        await context.close()

if __name__ == "__main__":
    asyncio.run(login_and_save_cookies())
