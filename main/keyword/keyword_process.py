import os
import pandas as pd

# Directory paths
RAW_DIR = "../../raw/keyword"
RESULT_DIR = "../../result/keyword"

# Initialize an Excel writer
writer = pd.ExcelWriter(RESULT_DIR, engine='openpyxl')
# Prompt user whether they want top 400 data
dir_name = input(f"请输入你想要处理的文件夹名称 (注：请先将需要处理的文件合并在一个文件夹中): ").strip()
input_folder = f"{RAW_DIR}/{dir_name}"

# Loop through all Excel files in the folder
for filename in os.listdir(input_folder): 
    if filename.endswith(".xlsx") and "_反查出单词列表" in filename:
        filepath = os.path.join(input_folder, filename)
        
        # Extract ASIN from filename (assumes format: <date>_<ASIN>_反查出单词列表.xlsx)
        try:
            asin = filename.split("_")[1]
        except IndexError:
            print(f"Skipping {filename}: ASIN not found in filename.")
            continue

        # Read the '产品' sheet
        try:
            df = pd.read_excel(filepath, sheet_name="产品")
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            continue

        # ---- Do process (currently left blank) ----
        # For example: df = df[df["some_column"] > 0]
        # ------------------------------------------

        # Write to the output Excel file with ASIN as the sheet name
        df.to_excel(writer, sheet_name=asin, index=False)

def process_keyword(dataframe):
    
    #do things
    return

# Save the final combined file
writer.save()
print(f"Combined file saved to: {output_file}")
