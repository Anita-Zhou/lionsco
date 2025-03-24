import pickle
import time
import os
import download
from download import click_button
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Get the absolute path to the Chrome extension folder
BASE_DIR = "./"  # Gets the 'main' folder path
EXTENSION_PATH = os.path.join(BASE_DIR, "../aadiiicebnjmjmibjengdohedcfeekeg/1.3.9.4_0")

# Set up Chrome options and load the extension
options = webdriver.ChromeOptions()
options.add_argument(f"--load-extension={EXTENSION_PATH}")

# 是否在下载时包含五点描述，产品属性，和子类目
download_option = [1,0,0]

# 启动 WebDriver 并加载用户配置
driver = webdriver.Chrome(options=options)

driver.get("https://www.amazon.com/gp/bestsellers")  # Amazon Best Sellers 页面

for i in range(7):
    time.sleep(10)
    print(str((i+1) * 10) + " secs passed.")

wait = WebDriverWait(driver, 10)

download.download_review(wait, driver, download_option)