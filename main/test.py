import time
import os
import re
import requests
import zipfile
import platform
import pyautogui
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 设置 Chrome 的选项
def setup_chrome_with_plugin(plugin_path):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_extension(plugin_path)  # 加载插件路径
    service = Service('/path/to/chromedriver')  # 替换为你的 ChromeDriver 路径
    return webdriver.Chrome(service=service, options=options)

# # 初始化 ChromeOptions
# options = webdriver.ChromeOptions()

# # # 设置用户数据目录路径
# # user_data_dir = "/Users/<用户名>/Library/Application\ Support/Google/Chrome"  # 替换为你的实际路径
# # options.add_argument(f"user-data-dir={user_data_dir}")

# # 启动 WebDriver 并加载用户配置
# driver = webdriver.Chrome(options=options)

# driver.get("https://www.amazon.com/gp/bestsellers")  # Amazon Best Sellers 页面

# for i in range(3):
#     time.sleep(60)
#     print(str(i+1) + " minutes passed.")

# # Given a button's XPath, click on it
# def click_button(this_xpath):
#     wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'el-loading-mask')))
#     print("Loading mask is gone")
#     button = wait.until(EC.element_to_be_clickable((By.XPATH, this_xpath)))
#     print("button is clickable")
#     try:
#         button.click()
#         time.sleep(10)
#     except Exception as e:
#         print("An error occurred:", e)

# def navigate_and_extract(curr_xpath):
#     """
#     递归遍历导航栏并提取文本
#     :param curr_xpath: 当前类目的 XPath
#     """
#     try:
#         # 点击当前类目
#         element = wait.until(EC.element_to_be_clickable((By.XPATH, curr_xpath)))
#         element.click()
        
#         # 提取当前类目的文本
#         category_name = element.text
#         print(f"当前类目: {category_name}")
        
#         # 构造下一级类目的 XPath
#         next_xpath_base = curr_xpath.rsplit('/', 2)[0]  # 去掉最后两层
#         last_div = int(curr_xpath.split('/')[-2].replace('div[', '').replace(']', ''))
#         next_xpath = f"{next_xpath_base}/div[{last_div + 1}]/div[1]/a"
        
#         # 尝试访问下一级类目
#         navigate_and_extract(next_xpath)
    
#     except (NoSuchElementException, TimeoutException):
#         # 如果找不到下一级类目，说明到达最深层级
#         print("到达最深层级")
#         return


# # 开始遍历，从一级类目开始
# start_xpath = "/html/body/div[1]/div[1]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[2]/div[9]/a"
# navigate_and_extract(start_xpath)

# # 关闭浏览器
# driver.quit()

import pickle
import time
import download
from download import click_button
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# 初始化 ChromeOptions
options = webdriver.ChromeOptions()

# 是否在下载时包含五点描述，产品属性，和子类目
download_option = [1,0,0]

# 启动 WebDriver 并加载用户配置
driver = webdriver.Chrome(options=options)

driver.get("https://www.amazon.com/gp/bestsellers")  # Amazon Best Sellers 页面

for i in range(2):
    time.sleep(75)
    print(str(i+1) + " minutes passed.")

wait = WebDriverWait(driver, 10)

# download.download_review(wait)

# Given a button's XPath, click on it
def click_button(this_xpath):
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'el-loading-mask')))
    print("Loading mask is gone")
    button = wait.until(EC.element_to_be_clickable((By.XPATH, this_xpath)))
    print("button is clickable")
    try:
        button.click()
        time.sleep(3)
    except Exception as e:
        print("An error occurred:", e)

# # 点击分页显示
# click_button('//*[@id="sorftime"]/div/div/section/main/div[1]/div[1]/div[2]/div/div/span[1]/button')

# # 点击产品列表
# click_button('//*[@id="sorftime"]/div/div/section/main/div[3]/div[3]/div[3]/div/div[18]')

# # 点击下载按钮
# click_button('//*[@id="sorftime"]/div/div/section/main/div[3]/div[3]/div[5]/div[17]/div[1]/div[1]/div[3]/span[1]/button')

# 下载选项，是否包含五点描述，产品属性，和子类目
for i in range(len(download_option)):
    if (download_option[i] == 1):
        option_box = '/html/body/div[15]/div/div[2]/div/div[1]/div[4]/div/label[' + str(i+1) + ']'
        print(option_box)
        time.sleep(10)
        click_button(option_box)

# Export button
click_button('/html/body/div[15]/div/div[2]/div/div[1]/div[8]/span/button')


    #    checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, )))
    #     print("checkbox " + str(i+1) + " is detected.")
    #     try:
    #         checkbox.click()
    #         print("checkbox " + str(i+1) + " is clicked")
    #     except Exception as e:
    #         print("An error occurred:", e)
