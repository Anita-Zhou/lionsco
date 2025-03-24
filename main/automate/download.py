import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# # 加载插件
# options = webdriver.ChromeOptions()
# plugin_path = "/path/to/your/extension"  # 替换为插件文件夹路径
# options.add_argument(f"load-extension={plugin_path}")
# # 是否在下载时包含五点描述，产品属性，和子类目
# download_option = [1,0,0]

# wait = WebDriverWait(driver, 10)

# Given a button's XPath, wait, and then click on it
def safe_click_button(this_wait, this_xpath):
    this_wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'el-loading-mask')))
    # DEBUG
    print("Loading mask is gone")
    button = this_wait.until(EC.element_to_be_clickable((By.XPATH, this_xpath)))
    # DEBUG
    print("Button is clickable")
    try:
        button.click()
        print("button clicked")
        time.sleep(1)
    except Exception as e:
        print("An error occurred:", e)

# Given a button's XPath, click on it
def click_button(this_driver, this_xpath):
    try:
        this_driver.find_element(By.XPATH, this_xpath).click()
        # DEBUG
        print("button clicked")
        time.sleep(1)
    except Exception as e:
        print("An error occurred:", e)

def download_review(this_wait, this_driver, this_options):
    # 点击分页显示
    safe_click_button(this_wait, '//*[@id="sorftime"]/div/div/section/main/div[1]/div[1]/div[2]/div/div/span[1]/button')

    # 点击产品列表
    safe_click_button(this_wait, '//*[@id="sorftime"]/div/div/section/main/div[3]/div[3]/div[3]/div/div[18]')
    
    time.sleep(10)
    # 点击下载按钮
    click_button(this_driver, '//*[@id="sorftime"]/div/div/section/main/div[3]/div[3]/div[5]/div[17]/div[1]/div[1]/div[3]/span[1]/button')

    time.sleep(5)
    # 下载选项，是否包含五点描述，产品属性，和子类目
    for i in range(len(this_options)):
        if (this_options[i] == 1):
            option_box = '/html/body/div[15]/div/div[2]/div/div[1]/div[4]/div/label[' + str(i+1) + ']'
            print(option_box)
            click_button(this_driver, option_box)


    # Export button
    click_button(this_driver, '/html/body/div[15]/div/div[2]/div/div[1]/div[8]/span/button')

