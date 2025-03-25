import pandas as pd
from playwright.sync_api import sync_playwright

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

if __name__ == "__main__":
    test()