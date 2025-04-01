import pandas as pd
from playwright.sync_api import sync_playwright
from collections import Counter
import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter
from collections import Counter

ASIN = 'B0DNZ535C6'
product_site = f'https://www.amazon.com/dp/{ASIN}?th=1'

def to_csv():
    # Load the Excel file
    excel_file = "./comments.xlsx"  # Replace with your file name
    df = pd.read_excel(excel_file)
    # Save as CSV
    csv_file = "./output.csv"  # Replace with your desired output file name
    df.to_csv(csv_file, index=False)
    print(f"Conversion complete. CSV saved as {csv_file}")


def test():
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

'''
Count the frequency of each word in the given column
'''
def count_word_freq(df, col_name):
    all_words = []
    for phrase in df[col_name].dropna():
        words = phrase.strip().split()
        all_words.extend(words)
    return Counter(all_words)

# Directory paths
RAW_DIR = "../../raw/keyword"
RESULT_DIR = "../../result/keyword"

# Prompt user whether they want top 400 data
dir_name = input(f"请输入你想要处理的文件夹名称 (注：请先将需要处理的文件合并在一个文件夹中): ").strip()
input_folder = f"{RAW_DIR}/{dir_name}"
output_file = os.path.join(RESULT_DIR, dir_name + "_combined.xlsx")

if __name__ == "__main__":
    # Loop through all Excel files in the folder
    for filename in os.listdir(input_folder): 
        if filename.startswith("~$"):
            continue
        if filename.endswith(".xlsx"):
            print("=====================================")
            print("                 START               ")
            print("=====================================")

            # Initialize an Excel writer
            filepath = os.path.join(input_folder, filename)
            out = os.path.join(RESULT_DIR, filename)
            print("Output file: ", out)
            writer = pd.ExcelWriter(out, engine='openpyxl')
            print(f"{filepath}")

            # Read the '产品' sheet
            try:
                df = pd.read_excel(filepath, sheet_name="产品", header=0)
            except Exception as e:
                print(f"Error reading file {filename}: {e}")
                continue
    
    # Print the word frequency
        word_freq = count_word_freq(df, "关键词")
        freq_df = pd.DataFrame(word_freq.items(), columns=["word", "count"]).sort_values(by="count", ascending=False)
        top_words = set(freq_df["word"].head(10))
        all_words = set(freq_df["word"])
        niche_words = all_words - top_words
        print(f"Top 10 frequent words: {freq_df.head(10)}")
        freq_df.to_excel(writer, sheet_name="词频", index=False)

        # Write to the output Excel file with ASIN as the sheet name
        df.to_excel(writer, index=False)

        # Save the final combined file
        writer.close()
        print(f"Processed file saved to: {out}")
