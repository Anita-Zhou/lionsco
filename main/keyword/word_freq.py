import pandas as pd
from collections import Counter
import spacy

def count_word_freq(df, col_name):
    all_words = []
    for phrase in df[col_name].dropna():
        words = phrase.strip().split()
        all_words.extend(words)
    return Counter(all_words)

def process_excel(input_file):
    # Load the Excel file
    df_all = pd.read_excel(input_file, header=None)

    # Ask the user for the title row and column
    title_row = int(input("标题是从上至下数第几行 (请输入数字): ")) - 1
    col_to_process = str(input("你要处理的数据列是哪一列（请输入数字，或输入数据列的标题）: ").strip())

    # Reload the file with correct header row
    df = pd.read_excel(input_file, header=title_row)

    # If column index is given instead of name, convert to name
    if col_to_process.isdigit():
        col_index = int(col_to_process) - 1
        col_name = df.columns[col_index]
    else:
        col_name = col_to_process

    # Count word frequencies
    word_freq = count_word_freq(df, col_name)

    # Save frequency to DataFrame
    freq_df = pd.DataFrame(word_freq.items(), columns=["word", "count"]).sort_values(by="count", ascending=False)

    # Print top 10 words
    print("Top 10 frequent words:")
    print(freq_df.head(10))

    # Save to new sheet in the same Excel file
    with pd.ExcelWriter(input_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        freq_df.to_excel(writer, sheet_name="词频", index=False)
    print("Word frequency saved to new sheet '词频'.")

# Example usage
# process_excel("your_file.xlsx")
if __name__ == "__main__":
    input_file = input("Enter the Excel file to process: ")
    process_excel(input_file)