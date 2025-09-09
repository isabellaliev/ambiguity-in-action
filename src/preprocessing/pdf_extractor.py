# scripts/pdf_extractor.py
import PyPDF2
import logging
from pathlib import Path
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFExtractor:
    """
    Simple PDF text extractor for Colombian decree documents.
    """
    
    def __init__(self, pdf_folder: str = "data/raw", output_folder: str = "data/raw"):
        self.pdf_folder = Path(pdf_folder)
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True)
    
    def extract_text_from_pdf(self, pdf_filename: str, output_filename: Optional[str] = None) -> str:
        """
        Extract text from a single PDF file.
        
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
            # Open and read PDF
            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                
                # Extract text from all pages
                full_text = ""
                total_pages = len(pdf_reader.pages)
                logger.info(f"Extracting text from {total_pages} pages...")
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    try:
                        page_text = page.extract_text()
                        full_text += page_text + "\n\n"
                        logger.info(f"Processed page {page_num}/{total_pages}")
                    except Exception as e:
                        logger.warning(f"Error extracting page {page_num}: {str(e)}")
                        continue
                
                # Clean up the extracted text
                full_text = self._clean_extracted_text(full_text)
                
                # Save to .txt file
                if not output_filename:
                    output_filename = pdf_filename.replace('.pdf', '.txt')
                
                output_path = self.output_folder / output_filename
                with open(output_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(full_text)
                
                logger.info(f"Text saved to: {output_path}")
                logger.info(f"Extracted {len(full_text.split())} words total")
                
                return full_text
                
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_filename}: {str(e)}")
            raise
    
    def _clean_extracted_text(self, text: str) -> str:
        """
        Clean text extracted from PDF to improve readability.
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        import re
        
        # Remove excessive whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)  # Max 2 newlines
        text = re.sub(r'[ \t]+', ' ', text)     # Normalize spaces
        
        # Fix common PDF extraction issues
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Add spaces between joined words
        text = re.sub(r'(\d)([A-Za-z])', r'\1 \2', text)  # Space between numbers and letters
        text = re.sub(r'([A-Za-z])(\d)', r'\1 \2', text)  # Space between letters and numbers
        
        # Remove page numbers and headers/footers (basic patterns)
        text = re.sub(r'\n\d+\n', '\n', text)  # Remove standalone page numbers
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)  # Remove spaced page numbers
        
        # Fix Spanish text issues
        text = re.sub(r'([a-záéíóúñ])([AÁÉÍÓÚÑ])', r'\1 \2', text)  # Space before capitals
        
        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def extract_all_pdfs(self):
        """
        Extract text from all PDF files in the pdf_folder.
        """
        pdf_files = list(self.pdf_folder.glob("*.pdf"))
        
        if not pdf_files:
            logger.warning("No PDF files found in the specified folder")
            return
        
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        for pdf_file in pdf_files:
            try:
                logger.info(f"Processing: {pdf_file.name}")
                self.extract_text_from_pdf(pdf_file.name)
                logger.info(f"Successfully processed: {pdf_file.name}")
            except Exception as e:
                logger.error(f"Failed to process {pdf_file.name}: {str(e)}")
                continue
        
        logger.info("PDF extraction completed!")

# Simple usage example
def extract_decreto_1194():
    """
    Specific function to extract Decreto 1194 de 1989
    """
    extractor = PDFExtractor()
    
    # Try different possible filenames
    possible_names = [
        "decreto_1194_1989.pdf",
        "Decreto_1194_1989.pdf", 
        "decreto-1194-1989.pdf",
        "1194.pdf"
    ]
    
    for filename in possible_names:
        try:
            text = extractor.extract_text_from_pdf(filename, "decreto_1194_1989.txt")
            print(f"✅ Successfully extracted: {filename}")
            print(f"📄 First 200 characters:")
            print(text[:200] + "...")
            return text
        except FileNotFoundError:
            continue
    
    print("❌ Could not find Decreto 1194 PDF file")
    print("📁 Available PDF files:")
    pdf_files = list(Path("data/raw").glob("*.pdf"))
    for pdf in pdf_files:
        print(f"   - {pdf.name}")

if __name__ == "__main__":
    print("🔧 PDF Text Extractor for Colombian Decrees")
    print("=" * 50)
    
    # Try to extract Decreto 1194
    extract_decreto_1194()