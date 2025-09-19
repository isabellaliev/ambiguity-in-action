# pdf extractor (tried with pdf2 and sucked - remember to always use pdfplumber!!)
import pdfplumber
import logging
from pathlib import Path
from typing import Optional

# setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFExtractor:
    """
    PDF text extractor for Colombian decree documents using pdfplumber.
    Much better for text extraction than PyPDF2!
    """
    
    def __init__(self, pdf_folder: str = "data/raw", output_folder: str = "data/raw"):
        self.pdf_folder = Path(pdf_folder)
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True)
    
    def extract_text_from_pdf(self, pdf_filename: str, output_filename: Optional[str] = None) -> str:
        """
        Extract text from a single PDF file using pdfplumber.
        
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
            # open PDF with pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                full_text = ""
                total_pages = len(pdf.pages)
                logger.info(f"Extracting text from {total_pages} pages using pdfplumber...")
                
                for page_num, page in enumerate(pdf.pages, 1):
                    try:
                        # extract text from page
                        page_text = page.extract_text()
                        
                        if page_text:  # Only add if we got text
                            full_text += page_text + "\n\n"
                            word_count = len(page_text.split())
                            logger.info(f"Page {page_num}/{total_pages}: extracted {word_count} words")
                        else:
                            logger.warning(f"Page {page_num}/{total_pages}: no text extracted")
                            
                    except Exception as e:
                        logger.warning(f"Error extracting page {page_num}: {str(e)}")
                        continue
                
                # clean up the extracted text
                full_text = self._clean_extracted_text(full_text)
                
                # save to .txt file
                if not output_filename:
                    output_filename = pdf_filename.replace('.pdf', '.txt')
                
                output_path = self.output_folder / output_filename
                with open(output_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(full_text)
                
                word_count = len(full_text.split())
                char_count = len(full_text)
                
                logger.info(f"Text saved to: {output_path}")
                logger.info(f"Total extracted: {word_count} words, {char_count} characters")
                
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
        
        if not text.strip():
            logger.warning("Text is empty after extraction!")
            return text
        
        # remove excessive whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)  # max 2 newlines
        text = re.sub(r'[ \t]+', ' ', text)     # normalize spaces
        
        # fix common PDF extraction issues
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Add spaces between joined words
        text = re.sub(r'(\d)([A-Za-z])', r'\1 \2', text)  # Space between numbers and letters
        text = re.sub(r'([A-Za-z])(\d)', r'\1 \2', text)  # Space between letters and numbers
        
        # remove page numbers and headers/footers (basic patterns)
        text = re.sub(r'\n\d+\n', '\n', text)  # Remove standalone page numbers
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)  # Remove spaced page numbers
        
        # fix Spanish text issues
        text = re.sub(r'([a-záéíóúñ])([AÁÉÍÓÚÑ])', r'\1 \2', text)  # Space before capitals
        
        # clean up extra spaces
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        logger.info(f"Text cleaning completed. Final length: {len(text)} characters")
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

def process_all_colombian_decrees():
    """
    Process all Colombian decree PDFs in the data/raw folder with detailed output
    """
    extractor = PDFExtractor()
    
    # Get all PDF files
    pdf_files = list(Path("data/raw").glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in data/raw/")
        return
    
    print(f"Found {len(pdf_files)} PDF files:")
    for pdf in pdf_files:
        print(f"   - {pdf.name}")
    
    print("\n Starting extraction with pdfplumber...")
    
    successful_extractions = 0
    
    for pdf_file in pdf_files:
        try:
            print(f"\n Processing: {pdf_file.name}")
            
            # create a clean output filename
            output_name = pdf_file.name.replace('.pdf', '.txt')
            output_name = output_name.replace(' - ', '_').replace(' ', '_')
            
            text = extractor.extract_text_from_pdf(pdf_file.name, output_name)
            
            # check extraction results
            word_count = len(text.split())
            char_count = len(text)
            
            if word_count > 0:
                print(f" Success! Extracted {word_count} words, {char_count} characters")
                print(f" Saved as: {output_name}")
                
                # Show first 150 characters for verification
                preview = text[:150].replace('\n', ' ')
                print(f" Preview: {preview}...")
                successful_extractions += 1
            else:
                print(f"  WARNING: No text extracted from {pdf_file.name}")
                print(f"  This might be an image-based PDF requiring OCR")
                
        except Exception as e:
            print(f" Failed to process {pdf_file.name}: {str(e)}")
            continue
    
    print(f"\n Processing complete!")
    print(f" Successfully processed: {successful_extractions}/{len(pdf_files)} files")
    
    if successful_extractions < len(pdf_files):
        print(f"\n Tip: Files that failed might be:")
        print(f"   - Image-based PDFs (need OCR)")
        print(f"   - Corrupted files")
        print(f"   - Password protected")

# Simple usage example for specific decreto
def extract_decreto_1194():
    """
    Specific function to extract Decreto 1194 de 1989 with pdfplumber
    """
    extractor = PDFExtractor()
    
    # Try different possible filenames
    possible_names = [
        "Decreto 1194 - 1989.pdf",  # Your actual filename!
        "decreto_1194_1989.pdf",
        "Decreto_1194_1989.pdf", 
        "decreto-1194-1989.pdf",
        "1194.pdf"
    ]
    
    for filename in possible_names:
        try:
            text = extractor.extract_text_from_pdf(filename, "decreto_1194_1989.txt")
            print(f" Successfully extracted: {filename}")
            print(f" Extracted {len(text.split())} words")
            if text.strip():
                print(f" First 200 characters:")
                print(text[:200] + "...")
            return text
        except FileNotFoundError:
            continue
    
    print(" Could not find Decreto 1194 PDF file")
    print(" Available PDF files:")
    pdf_files = list(Path("data/raw").glob("*.pdf"))
    for pdf in pdf_files:
        print(f"   - {pdf.name}")

if __name__ == "__main__":
    print(" PDF Text Extractor for Colombian Decrees (using pdfplumber)")
    print("=" * 65)
    
    # Process ALL PDFs
    process_all_colombian_decrees()