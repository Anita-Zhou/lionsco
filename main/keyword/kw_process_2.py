import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter
from collections import Counter

# Directory paths
RAW_DIR = "../../raw/keyword"
RESULT_DIR = "../../result/keyword"

# Prompt user whether they want top 400 data
dir_name = input(f"请输入你想要处理的文件夹名称 (注：请先将需要处理的文件合并在一个文件夹中): ").strip()
input_folder = f"{RAW_DIR}/{dir_name}"
output_file = os.path.join(RESULT_DIR, dir_name + "_combined.xlsx")

'''
Count the frequency of each word in the given column
'''
def count_word_freq(df, col_name):
    all_words = []
    for phrase in df[col_name].dropna():
        words = phrase.strip().split()
        all_words.extend(words)
    return Counter(all_words)

'''
Highlight essential keywords in the Excel file
'''
def hlt_essential_kw(msk,filename):
    # Open the saved file using openpyxl
    wb = load_workbook(filename)
    ws = wb[asin]

    # Map column names to Excel column indexes
    header = [cell.value for cell in ws[1]]
    col_index = {name: idx + 1 for idx, name in enumerate(header)}

    # Define the purple
    purple_fill = PatternFill(start_color="E4DFEC", end_color="E4DFEC", fill_type="solid")

    # Loop through DataFrame rows and corresponding Excel rows
    for i, highlight in enumerate(msk, start=2):  # Start from the second row (first row is header)
        if highlight:
            # Color the '关键词' column in the Excel sheet
            ws.cell(row=i, column=col_index["关键词"]).fill = purple_fill

    # Save changes
    wb.save(filename)


'''
Highlight niche keywords in the Excel file
'''
def hlt_niche_kw(niches, filename):
    # Open the saved file using openpyxl
    wb = load_workbook(filename)
    ws = wb[asin]

    # Map column names to Excel column indexes
    header = [cell.value for cell in ws[1]]
    col_index = {name: idx + 1 for idx, name in enumerate(header)}

    # Define green fill
    green_fill = PatternFill(start_color="CCFF99", end_color="CCFF99", fill_type="solid")

    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        keyword_cell = row[col_index["关键词"] - 1]
        flow_cell = row[col_index["流量占比(%)"] - 1]

        words = str(keyword_cell.value or "").strip().split()
        flow = float(flow_cell.value or 0)

        if any(word in niches for word in words) and flow > 1:
            keyword_cell.fill = green_fill

    wb.save(filename)
    print(f"Highlighted niche keywords in {filename}.")


'''
Highlight niche keywords in the Excel file
'''
def hlt_big_kw(niches, filename):
    # Open the saved file using openpyxl
    wb = load_workbook(filename)
    ws = wb[asin]

    # Map column names to Excel column indexes
    header = [cell.value for cell in ws[1]]
    col_index = {name: idx + 1 for idx, name in enumerate(header)}

    # Define green fill
    green_fill = PatternFill(start_color="CCFF99", end_color="CCFF99", fill_type="solid")

    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        keyword_cell = row[col_index["关键词"] - 1]
        flow_cell = row[col_index["流量占比(%)"] - 1]

        words = str(keyword_cell.value or "").strip().split()
        flow = float(flow_cell.value or 0)

        if any(word in niches for word in words) and flow > 1:
            keyword_cell.fill = green_fill

    wb.save(filename)
    print(f"Highlighted niche keywords in {filename}.")

'''
Post-process the Excel file
'''
def post_process(filename):
    #=====================
    #   Post-processing
    #=====================
    print(f"Post-processing file: {filename}")
    wb = load_workbook(filename)
    for sheetname in wb.sheetnames:
    
        ws = wb[sheetname]

        # Set row height of new first row (was originally third)
        ws.row_dimensions[1].height = 30

        # Fill background color for new header row
        fill = PatternFill(start_color="B8CCE4", end_color="B8CCE4", fill_type="solid")
        for cell in ws[1]:
            cell.fill = fill
        
        # Set each column's width to 13 characters
        for col_idx in range(1, ws.max_column + 1):
            col_letter = get_column_letter(col_idx)
            ws.column_dimensions[col_letter].width = 13

        # Save the styled workbook
        wb.save(filename)
        print(f"Styled Excel saved to: {filename}")
        print("=====================================")
        print("                 END                 ")
        print("=====================================")

# # Initialize an Excel writer
# writer = pd.ExcelWriter(output_file, engine='openpyxl')

# Loop through all Excel files in the folder
for filename in os.listdir(input_folder): 
    if filename.startswith("~$"):
        continue
    if filename.endswith(".xlsx") and "_反查关键词" in filename:
        print("=====================================")
        print("                 START               ")
        print("=====================================")

        # Initialize an Excel writer
        filepath = os.path.join(input_folder, filename)
        out = os.path.join(RESULT_DIR, filename)
        print("Output file: ", out)
        writer = pd.ExcelWriter(out, engine='openpyxl')
        print(f"{filepath}")

        # Extract ASIN from filename (assumes format: <date>_<ASIN>_反查出单词列表.xlsx)
        try:
            asin = filename.split("_")[1]
            print(f"Processing file: {asin}")
        except IndexError:
            print(f"Skipping {filename}: ASIN not found in filename.")
            continue

        # Read the '产品' sheet
        try:
            df = pd.read_excel(filepath, sheet_name="产品", header=2)
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            continue

        # ====================
        #      Do process  
        # ====================
        # Replace all NA with 0
        df.replace("--", 0, inplace=True)

        # Create "序号" column starting from 1
        df.sort_values(by="月搜索量", ascending=False, inplace=True)
        df.insert(0, "序号", range(1, len(df) + 1))

        # Extract 自然流量占比 from 贡献流量
        df['自然流量占比'] = df['贡献流量'].str.extract(r':(\d+(?:\.\d+)?)%').fillna(0).astype(float)
        mask = (
            df["出单词来源"].str.contains("热搜关键词", na=False) &
            (df["月搜索量"].astype(float) > 5000) &
            (df["流量占比(%)"].astype(float) > 1)
        )
        # print("Mask: ")
        # print(mask)

        # Filter out unnecessary columns
        required_columns = [
            "序号", "关键词", "出单词来源", "月排名", "月搜索量", "周搜索排名变化", "旺季",
            "曝光形式",	"流量占比(%)",	"点击垄断性(%)", "转化垄断性(%)", "自然流量占比"]
        # Ensure only existing columns are selected (avoid errors if some columns are missing)
        available_columns = [col for col in required_columns if col in df.columns]
        df = df[available_columns]  

        # Print the word frequency
        word_freq = count_word_freq(df, "关键词")
        freq_df = pd.DataFrame(word_freq.items(), columns=["word", "count"]).sort_values(by="count", ascending=False)
        top_words = set(freq_df["word"].head(10))
        all_words = set(freq_df["word"])
        niche_words = all_words - top_words
        print(f"Top 10 frequent words: {freq_df.head(10)}")
        freq_df.to_excel(writer, sheet_name="词频", index=False)

        # Write to the output Excel file with ASIN as the sheet name
        df.to_excel(writer, sheet_name=asin, index=False)

        # Save the final combined file
        writer.close()
        print(f"Processed file saved to: {out}")
        # print(f"Combined file saved to: {output_file}")

        # ================================
        #   Post-process the Excel file
        # ================================
        hlt_niche_kw(niche_words, out)
        hlt_essential_kw(mask, out)
        post_process(out)

