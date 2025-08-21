import os
import pdfplumber

# Define reusable function
def extract_text(pdf_path, output_txt_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(full_text)

# Create cleaned folder in project root
os.makedirs("../cleaned", exist_ok=True)

# Extract from Decreto
with pdfplumber.open(r"C:\Users\isabe\Documents\GitHub\ambiguity-in-action\data\Decreto 3398 - 965.pdf") as pdf:
    Dec3398_text = ""
    for page in pdf.pages:
        Dec3398_text += page.extract_text() + "\n"

with open("../cleaned/Dec3398_text.txt", "w", encoding="utf-8") as f:
    f.write(Dec3398_text)

# Extract from Ley48
with pdfplumber.open(r"C:\Users\isabe\Documents\GitHub\ambiguity-in-action\data\Ley 48 - 1968.pdf") as pdf:
    Ley48_text = ""
    for page in pdf.pages:
        Ley48_text += page.extract_text() + "\n"

with open("../cleaned/Ley48_text.txt", "w", encoding="utf-8") as f:
    f.write(Ley48_text)
