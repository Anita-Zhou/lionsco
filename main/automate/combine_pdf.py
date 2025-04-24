from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader("./FBA18WNBD9V8_BoxLabels.pdf")
writer = PdfWriter()

for page in reader.pages:
    for _ in range(4):  # repeat 4 times
        writer.add_page(page)

with open("output_repeated.pdf", "wb") as f:
    writer.write(f)