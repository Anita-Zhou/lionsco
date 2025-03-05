import os
import shutil
import pandas as pd
from openpyxl import load_workbook
import statistics

# Directory paths
RAW_DIR = "../raw"
RESULT_DIR = "../result"
TEMPLATE_FILE = "../template3.xlsx"

产品名 = 'A3'
类目链接 = 'D3'
在售产品数 = 'F3'
买家垄断系数 = 'F4'
月均销额 = 'F5'
AMZ自营占比 = 'F6'
平均上架天数 = 'F7'
新品占比 = 'F8'
月搜索量 = 'F9'
后25销额 = 'F10'
在售商家数 = 'F11'
平均价格 = 'H3'
月均销量 = 'H4'
中位销额 = 'H5'
AMZ自营额 = 'H6'
平均评价数量 = 'H7'
新品市场份额 = 'H8'
退货率 = 'H9'
平均FBA占比 = 'H10'
品牌数 = 'H11'

this_name = 'test placemat'

def process_file(file_path):
    """Process a single raw data file using pandas."""

    # Load specific sheets from the Excel file
    product_df = pd.read_excel(file_path, sheet_name="产品", header=3)  # Assuming row 1 is header
    # cal_df = pd.read_excel(file_path, sheet_name="产品详情", header=1)  # Assuming row 1 is header
    
    # Filter out products where "Listing月销量" < 10 in the product_df
    product_df = product_df[product_df["Listing月销量"] >= 10]

    # Create a copy of the template
    new_file_name = f"{this_name}_template.xlsx"
    new_file_path = os.path.join(RESULT_DIR, new_file_name)
    shutil.copyfile(TEMPLATE_FILE, new_file_path)

    # Load the copied template
    template_wb = load_workbook(new_file_path)
    template_sheet = template_wb.active  # Assumes writing to the first sheet

    # Read Excel file into a DataFrame, skipping header row
    df = pd.read_excel(file_path, header=3)  # header=1 assumes row 1 is header

    
    # Example implementations of previous functions using pandas
    def cal_average(column_name):
        return df[column_name].mean() if not df[column_name].empty else 0
    
    def cal_median(column_name):
        return df[column_name].median() if not df[column_name].empty else 0
    
    def cal_last_x_percent(column_name, x=25):
        if df[column_name].empty:
            return 0
        sorted_values = df[column_name].dropna().sort_values(ascending=False)
        n = max(1, int(len(sorted_values) * (x / 100)))
        return sorted_values.tail(n).mean() if n > 0 else 0
    
    def count_keyword(column_name, keyword):
        return df[column_name].astype(str).str.lower().eq(str(keyword).lower()).sum()
    
    def count_new_product(column_name, days):
        return df[column_name].lt(days).sum()
    
    def sum_top_x(column_name, x=10):
        return df[column_name].nlargest(x).sum() if not df[column_name].empty else 0
    
    def count_unique(column_name):
        return df[column_name].nunique()
    
    # You can now use these functions with column names instead of Excel coordinates
    # Example usage (you'll need to map your Excel columns to DataFrame column names):
    results = {
        'avg_sales': cal_average('Listing月销额($)'),  # Replace 'Price' with actual column name
        'median_sales': cal_median('Listing月销额($)'),    # Replace 'Sales' with actual column name
        # Add more calculations as needed
    }
    
    return results

def save_result(results):
    # Create a copy of the template
    new_file_name = f"{this_name}_template.xlsx"
    new_file_path = os.path.join(RESULT_DIR, new_file_name)
    shutil.copyfile(TEMPLATE_FILE, new_file_path)

    # Load the copied template
    template_wb = load_workbook(new_file_path)
    template_sheet = template_wb.active  # Assumes writing to the first sheet


    # Copy specific cells from raw to template
    template_sheet[月均销额]=results['avg_sales']
    template_sheet[中位销额]=results['median_sales']
    
    # percentage2 = calculate_percentage("H", cal_sheet)
    # template_sheet["F16"] = percentage2

    # Save the modified template
    template_wb.save(new_file_path)
    print(f"Processed and saved: {new_file_path}")

def main():
    """Main function to iterate through raw files and process them."""
    for file_name in os.listdir(RAW_DIR):
        # DEBUG 
        print("file name: " + file_name)
        if file_name.startswith("~$"):
            continue
        if file_name.endswith("产品列表.xlsx"):
            file_path = os.path.join(RAW_DIR, file_name)
            print(f"Processing file: {file_name}")
            results = process_file(file_path)
            # Do something with results, like write to template

if __name__ == "__main__":
    main()