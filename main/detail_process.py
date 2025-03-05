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

this_name = 'TEST'

# Example implementations of previous functions using pandas
def cal_average(df, column_name):
    # Temporarily drop rows where this column is 0
    valid_values = df[column_name][df[column_name] != 0]  
    # Calculate mean only using valid values
    return valid_values.mean() if not valid_values.empty else 0

def cal_median(df, column_name):
    # Temporarily drop rows where this column is 0
    valid_values = df[column_name][df[column_name] != 0]  
    return valid_values.median() if valid_values.empty else 0

def cal_last_x_percent(df, column_name, x=25):
    # Temporarily drop rows where this column is 0
    valid_values = df[column_name][df[column_name] != 0]  
    if valid_values.empty:
        return 0
    sorted_values = valid_values.sort_values(ascending=False)
    n = max(1, int(len(sorted_values) * (x / 100)))
    return sorted_values.tail(n).mean() if n > 0 else 0

def count_keyword(df, column_name, keyword):
    return df[column_name].astype(str).str.lower().eq(str(keyword).lower()).count()

def count_new_product(df, column_name, days):
    # Temporarily drop rows where this column is 0
    valid_df = df[df[column_name] != 0]  
    return (valid_df[column_name] < days).sum() if not valid_df.empty else 0

def sum_top_x(df, column_name, x=10):
    return df[column_name].nlargest(x).sum() if not df[column_name].empty else 0

def count_unique(df, column_name):
    return df[column_name].nunique()

def create_avg_fba(df):
    # Convert columns to numeric, forcing non-numeric values to NaN
    df['FBA费用($)'] = pd.to_numeric(df['FBA费用($)'], errors='coerce')
    df['实际价格($)'] = pd.to_numeric(df['实际价格($)'], errors='coerce')
    # Calculate the ratio, handling NaN by replacing them with 0
    df['FBA费用占比'] = (df['FBA费用($)'] / df['实际价格($)']).fillna(0)
    # Replace infinity values (from division by zero) with 0
    df['FBA费用占比'] = df['FBA费用占比'].replace([float('inf'), -float('inf')], 0)

# Process the raw-data file
def process_file(file_path):
    """Process a single raw data file using pandas."""
    # Load specific sheets from the Excel file
    # Assume header row is row 3
    product_df = pd.read_excel(file_path, sheet_name="产品", header=2) 
    # # DEBUG
    # # Print all column names to check for typos or formatting issues
    # print("Column Names:", product_df.columns.tolist())

    # # DEBUG
    # # Identify rows where "Listing月销量" is not numeric
    # non_numeric_rows = product_df[~product_df["Listing月销量"].astype(str).str.replace('.', '', regex=False).str.isdigit()]
    # # Print the problematic rows
    # print("Rows with non-numeric 'Listing月销量':")
    # print(non_numeric_rows)

    cols = ['Listing月销量', 'Listing月销额($)', '实际价格($)', '上架时长(天）']

    for col in cols:
        if col in product_df.columns:
            # Convert to numeric, replacing non-numeric values with 0
            product_df[col] = pd.to_numeric(product_df[col], errors='coerce').fillna(0)
        else:
            print(f"Warning: Column '{col}' not found in DataFrame")

        # Drop rows with value smaller than 10
        product_df = product_df[product_df['Listing月销量'] >= 10]

    # TODO: Change this filter every time
    # Filter to keep rows where "产品名称" or "五点描述" contains "round" (case-insensitive)
    product_df = product_df[
        product_df["产品名称"].astype(str).str.lower().str.contains("round") |
        product_df["五点描述"].astype(str).str.lower().str.contains("round")
    ].dropna(subset=["产品名称", "五点描述"], how="all")  # Drop rows where both are NaN

    create_avg_fba(product_df)
    # DEBUG
    # Print all column names to check for typos or formatting issues
    print("Column Names:", product_df.columns.tolist())

    # You can now use these functions with column names instead of Excel coordinates
    # Example usage (you'll need to map your Excel columns to DataFrame column names):
    results = {
        'avg_sales': cal_average(product_df, 'Listing月销额($)'), 
        'median_sales': cal_median(product_df, 'Listing月销额($)'), 
        'total_prdcts': count_unique(product_df, 'ASIN'),    
        'mkt_barrier' : sum_top_x(product_df, 'Listing月销额($)', 10),
        'last25_sales': cal_last_x_percent(product_df, 'Listing月销额($)', 25),
        'unique_brands': count_unique(product_df, '品牌'),
        'unique_sellers': count_unique(product_df, '店铺'),
        'num_amz': count_keyword(product_df, 'BBX卖家属性', '亚马逊自营'),
        'avg_days': cal_average(product_df, '上架时长(天）'),
        'new_prdcts': count_new_product(product_df, '上架时长(天）', 181),
        'avg_price': cal_average(product_df, '实际价格($)'),
        'avg_num_sales': cal_average(product_df, 'Listing月销量'),
        'avg_reviews': cal_average(product_df, '评价数量'),
        'amz_share': (product_df.loc[product_df['BBX卖家属性'] == '亚马逊自营', 'Listing月销额($)'].sum())/(product_df['Listing月销额($)'].sum()),
        'new_share': (product_df.loc[product_df['上架时长(天）'] < 181, 'Listing月销额($)'].sum())/(product_df['Listing月销额($)'].sum()),
        'avg_fba': cal_average(product_df, 'FBA费用占比')
    }
    
    return results

def save_result(results):
    """Save the processed results to a new Excel file based on the template."""
    # DEBUG
    print("save_result")
    # Create a copy of the template
    new_file_name = f"{this_name}_template.xlsx"
    new_file_path = os.path.join(RESULT_DIR, new_file_name)
    shutil.copyfile(TEMPLATE_FILE, new_file_path)

    # Load the copied template
    template_wb = load_workbook(new_file_path)
    template_sheet = template_wb.active  # Assumes writing to the first sheet

    # Copy specific cells from raw to template
    template_sheet[在售产品数] = results['total_prdcts']
    template_sheet[买家垄断系数] = results['mkt_barrier']
    template_sheet[月均销额] = results['avg_sales']
    template_sheet[AMZ自营占比] = results['num_amz'] / results['total_prdcts']
    template_sheet[平均上架天数] = results['avg_days']
    template_sheet[新品占比] = str(results['new_prdcts']) + "个, " + str(results['new_prdcts'] / results['total_prdcts'])
    template_sheet[月搜索量]
    template_sheet[后25销额] = results['last25_sales']
    template_sheet[在售商家数] = results['unique_sellers']
    template_sheet[平均价格] = results['avg_price']
    template_sheet[月均销量] = results['avg_num_sales']
    template_sheet[中位销额] = results['median_sales']
    template_sheet[AMZ自营额] = results['amz_share']
    template_sheet[平均评价数量] = results['avg_reviews']
    template_sheet[新品市场份额] = results['new_share']
    template_sheet[退货率]
    template_sheet[平均FBA占比] = results['avg_fba']
    template_sheet[品牌数] = results['unique_brands']
    
    # percentage2 = calculate_percentage("H", cal_sheet)
    # template_sheet["F16"] = percentage2

    # Create a new sheet for filtered data
    extra_sheet = template_wb.create_sheet(title="Filtered Raw Data")  # Create a second sheet



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
        if file_name.endswith("产品看板导出.xlsx"):
            file_path = os.path.join(RAW_DIR, file_name)
            print(f"Processing file: {file_name}")
            results = process_file(file_path)
            # Do something with results, like write to template
            save_result(results)

if __name__ == "__main__":
    main()