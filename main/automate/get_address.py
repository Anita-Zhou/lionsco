import pickle
import time
import os
import shutil
import pandas as pd
from openpyxl import load_workbook
import statistics
import re
from playwright.sync_api import sync_playwright
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


ASIN = 'B0DNZ535C6'
product_site = f'https://www.amazon.com/dp/{ASIN}?th=1'
RAW_DIR = "../../raw/sale"


def get_merchant_site():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(product_site)

        # Wait for the element to be visible (optional but recommended)
        page.wait_for_selector("#sellerProfileTriggerId")

        # Extract href attribute
        merchant = page.get_attribute("#sellerProfileTriggerId", "href")
        print("Merchant link:", merchant)
        browser.close()
        return merchant

    
def get_merchant_address(merchant_site):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.amazon.com/sp?ie=UTF8&seller=AF9NNE4MR5EHT&asin=B07CYWKJRY&ref_=dp_merchant_link&isAmazonFulfilled=1")

        # Run JavaScript inside the browser
        content = page.evaluate("""() => {
            return document.querySelector("#page-section-detail-seller-info").innerText;
        }""")
        print(content)
        browser.close()
        return content

def process_file(file_path):
    """Process a single raw data file using pandas."""
    # Load specific sheets from the Excel file
    # Assume header row is row ?
    product_df = pd.read_excel(file_path, sheet_name="产品", header=5) 
    asins = product_df["ASIN"].unique()
    print(f"ASINs found: {asins}")
    # Do processing here
    for asin in asins:
        get_merchant_address(get_merchant_site())




'''
Execution starts here.
'''
def main():
    """Main function to iterate through raw files and process them."""
    # ============================
    # Step 1: Process Raw Files
    # ============================
    for file_name in os.listdir(RAW_DIR):
        # # DEBUG 
        # print("file name: " + file_name)
        if file_name.startswith("~$"):
            continue
        if file_name.endswith("产品看板导出.xlsx"):
            print("=====================================")
            print("                 START               ")
            print("=====================================")
            file_path = os.path.join(RAW_DIR, file_name)
            print(f"Processing file: {file_name}")
            # Prompt user for a keyword filter (optional)
            is_process = input("你要处理这个文件吗 (yes/no): ").strip()
            if is_process.lower() != "yes":
                print("Skipping...")
                continue
            process_file(file_path)
            print("=====================================\n")
    # get_merchant_address(get_merchant_site())

if __name__ == "__main__":
    main()
