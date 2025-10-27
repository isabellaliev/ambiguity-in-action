# scripts/ocr_extractor.py
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import logging
from pathlib import Path
from typing import Optional, List
import re

# Configure paths for Windows installations
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
POPPLER_PATH = r'C:\Program Files\poppler-25.07.0\Library\bin'

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OCRExtractor:
    """
    OCR-only extractor for image-based PDFs.
    Use this when your regular PDF extractor fails!
    """
    
    def __init__(self, pdf_folder: str = "data/raw", output_folder: str = "data/raw"):
        self.pdf_folder = Path(pdf_folder)
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True)
        
        # Create temp folder for OCR images
        self.temp_folder = Path("data/temp_ocr")
        self.temp_folder.mkdir(exist_ok=True)
    
    def ocr_pdf(self, pdf_filename: str, output_filename: Optional[str] = None) -> str:
        """
        Extract text from image-based PDF using OCR.
        
        Args:
            pdf_filename: Name of the PDF file
            output_filename: Optional name for output .txt file
            
        Returns:
            Extracted text content
        """
        pdf_path = self.pdf_folder / pdf_filename
        
        if not pdf_path.exists():
            logger.error(f"PDF file not found: {pdf_path}")
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        try:
            # Convert PDF to images
            logger.info(f"Converting {pdf_filename} to images (DPI=300)...")
            logger.info(f"Using poppler path: {POPPLER_PATH}")
            
            # Verify poppler path exists
            if not Path(POPPLER_PATH).exists():
                logger.error(f"Poppler path does not exist: {POPPLER_PATH}")
                raise FileNotFoundError(f"Poppler path not found: {POPPLER_PATH}")
            
            images = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)
            
            full_text = ""
            total_pages = len(images)
            logger.info(f"Starting OCR on {total_pages} pages...")
            
            for page_num, image in enumerate(images, 1):
                try:
                    logger.info(f"OCR processing page {page_num}/{total_pages}...")
                    
                    # Optional: Save image for debugging
                    # temp_image_path = self.temp_folder / f"{pdf_filename}_page_{page_num}.png"
                    # image.save(temp_image_path)
                    
                    # Perform OCR with Spanish language support
                    page_text = pytesseract.image_to_string(
                        image, 
                        lang='spa',  # Spanish - change to 'spa+eng' for bilingual
                        config='--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789áéíóúñÁÉÍÓÚÑüÜ.,;:!?()[]{}""«»-_/\\ \n\t'
                    )
                    
                    if page_text.strip():
                        full_text += page_text + "\n\n"
                        word_count = len(page_text.split())
                        logger.info(f"  Page {page_num}: {word_count} words extracted")
                    else:
                        logger.warning(f" Page {page_num}: no text found")
                    
                except Exception as e:
                    logger.warning(f" Error on page {page_num}: {str(e)}")
                    continue
            
            # Clean the extracted text
            cleaned_text = self._clean_ocr_text(full_text)
            
            # Save result
            if not output_filename:
                output_filename = pdf_filename.replace('.pdf', '_ocr.txt')
            
            output_path = self.output_folder / output_filename
            with open(output_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(cleaned_text)
            
            word_count = len(cleaned_text.split())
            logger.info(f" OCR completed! {word_count} words saved to {output_path}")
            
            return cleaned_text
            
        except Exception as e:
            logger.error(f"OCR failed for {pdf_filename}: {str(e)}")
            raise
    
    def _clean_ocr_text(self, text: str) -> str:
        """
        Clean OCR text specifically (more aggressive than regular PDF cleaning).
        """
        if not text.strip():
            return text
        
        logger.info("Cleaning OCR text...")
        
        # Fix common OCR errors in Spanish legal documents
        text = re.sub(r'\bARTlCULO\b', 'ARTÍCULO', text, flags=re.IGNORECASE)  # l instead of I
        text = re.sub(r'\bARTICULO\b', 'ARTÍCULO', text, flags=re.IGNORECASE)  # Missing accent
        text = re.sub(r'\bDECRETO\s+N[úu]mero\b', 'DECRETO Número', text, flags=re.IGNORECASE)
        text = re.sub(r'\bPARAGRAFO\b', 'PARÁGRAFO', text, flags=re.IGNORECASE)
        text = re.sub(r'\bCAPITULO\b', 'CAPÍTULO', text, flags=re.IGNORECASE)
        
        # Fix OCR spacing issues
        text = re.sub(r'([.!?])\s*([A-ZÁÉÍÓÚÑ])', r'\1\n\2', text)  # New line after sentence
        text = re.sub(r'([.!?])\s*(\d+\.)', r'\1\n\2', text)  # New line before numbered items
        
        # Structure legal documents better
        text = re.sub(r'\b(ARTÍCULO|PARÁGRAFO|CAPÍTULO|TÍTULO)\s+(\d+)', r'\n\n\1 \2', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(CONSIDERANDO|DECRETA|DISPONE):', r'\n\n\1:', text, flags=re.IGNORECASE)
        
        # Fix punctuation spacing
        text = re.sub(r'\s+([.,:;!?])', r'\1', text)  # Remove space before punctuation
        text = re.sub(r'([.,:;!?])([A-Za-záéíóúñÁÉÍÓÚÑ])', r'\1 \2', text)  # Add space after
        
        # Clean whitespace
        text = re.sub(r'\n{4,}', '\n\n', text)  # Max 2 newlines
        text = re.sub(r'[ \t]+', ' ', text)     # Normalize spaces
        text = re.sub(r' +\n', '\n', text)      # Remove trailing spaces
        text = re.sub(r'\n +', '\n', text)      # Remove leading spaces
        
        text = text.strip()
        
        logger.info(f"OCR text cleaning completed. {len(text)} characters.")
        return text
    
    def ocr_specific_files(self, filenames: List[str]):
        """
        OCR specific files by name.
        """
        results = {}
        
        for filename in filenames:
            try:
                print(f"\n Starting OCR for: {filename}")
                text = self.ocr_pdf(filename)
                results[filename] = {'status': 'success', 'words': len(text.split())}
                print(f" Success: {results[filename]['words']} words extracted")
                
                # Show preview
                preview = text[:200].replace('\n\n', ' | ').replace('\n', ' ')
                print(f" Preview: {preview}...")
                
            except Exception as e:
                results[filename] = {'status': 'failed', 'error': str(e)}
                print(f" Failed: {str(e)}")
        
        return results

def ocr_failed_pdfs():
    """
    Function to OCR PDFs that failed with regular extraction
    """
    ocr = OCRExtractor()
    
    print(" OCR Extractor for Image-based PDFs")
    print("=" * 45)
    
    # List all PDFs
    pdf_files = list(Path("data/raw").glob("*.pdf"))
    
    if not pdf_files:
        print(" No PDF files found in data/raw/")
        return
    
    print(f" Available PDF files:")
    for i, pdf in enumerate(pdf_files, 1):
        print(f"  {i}. {pdf.name}")
    
    # Let user choose which ones need OCR
    print(f"\n Which PDFs need OCR? (Enter numbers separated by commas, or 'all')")
    choice = input("Your choice: ").strip()
    
    if choice.lower() == 'all':
        selected_files = [pdf.name for pdf in pdf_files]
    else:
        try:
            indices = [int(x.strip()) - 1 for x in choice.split(',')]
            selected_files = [pdf_files[i].name for i in indices if 0 <= i < len(pdf_files)]
        except:
            print(" Invalid input. Please try again.")
            return
    
    if not selected_files:
        print(" No files selected.")
        return
    
    print(f"\n Will OCR {len(selected_files)} files:")
    for filename in selected_files:
        print(f"  - {filename}")
    
    # Process selected files
    results = ocr.ocr_specific_files(selected_files)
    
    # Summary
    successful = [f for f, r in results.items() if r['status'] == 'success']
    failed = [f for f, r in results.items() if r['status'] == 'failed']
    
    print(f"\n OCR Results:")
    print(f" Successful: {len(successful)}")
    print(f" Failed: {len(failed)}")

if __name__ == "__main__":
    ocr_failed_pdfs()