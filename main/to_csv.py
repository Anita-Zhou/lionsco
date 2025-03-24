import pandas as pd

# Load the Excel file
excel_file = "./comments.xlsx"  # Replace with your file name
df = pd.read_excel(excel_file)



# Save as CSV
csv_file = "./output.csv"  # Replace with your desired output file name
df.to_csv(csv_file, index=False)

print(f"Conversion complete. CSV saved as {csv_file}")
