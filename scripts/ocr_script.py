from pdf2image import convert_from_path
import pytesseract
import os

# Set up Tesseract path and language data folder
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
os.environ["TESSDATA_PREFIX"] = r"C:/tessdata"

#Creating output folders
os.makedirs("images", exist_ok=True)
os.makedirs("text", exist_ok=True)

#Converting PDF to Images
images = convert_from_path(
r"C:\Users\isabe\Documents\GitHub\ambiguity-in-action\data\Manual-de-Combate-1987 (Scanned).pdf",
    poppler_path=r"C:\Program Files\poppler-25.07.0\Library\bin"
)


#Run OCR on each image and save text
for i, image in enumerate(images):
    image_path = f"images/page_{i+1}.png"
    text_path = f"text/page_{i+1}.txt"

    image.save(image_path, "PNG")
    text = pytesseract.image_to_string(image, lang="spa")

    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)

print("ORC complete. Text files saved in /text folder.")