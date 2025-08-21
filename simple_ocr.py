from pdf2image import convert_from_path
import pytesseract
import os

# Set up Tesseract path and language data folder
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:/tessdata"

# Creating clean folders for this test
os.makedirs("decreto-test/images", exist_ok=True)
os.makedirs("decreto-test/text", exist_ok=True)

images = convert_from_path((r"C:\Users\isabe\Documents\GitHub\ambiguity-in-action\data\Decreto 3398 - 965.pdf"),
    poppler_path=r"C:\Program Files\poppler-25.07.0\Library\bin",
    first_page=1,
    last_page=1
)

# Save image and extract text
for i, image in enumerate(images):
    image_path = f"decreto-test/images/page_{i+1}.png"
    text_path = f"decreto-test/text/page_{i+1}.txt"

    image.save(image_path, "PNG")
    text = pytesseract.image_to_string(image, lang="spa")

    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)

print(text[:500])