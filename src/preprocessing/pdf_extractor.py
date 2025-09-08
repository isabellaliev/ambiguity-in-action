#Required libs
import # PDF EXTRACTOR BREAKDOWN - Part by Part Explanation

# ============================================================================
# PART 1: IMPORTS AND SETUP
# ============================================================================

import PyPDF2          # Library to read PDF files
import logging         # For tracking what the program is doing (like a diary)
from pathlib import Path    # Modern way to work with file paths
from typing import Optional # For type hints (makes code clearer)

# Set up logging - this creates a "diary" of what your program does
logging.basicConfig(
    level=logging.INFO,  # Show INFO level messages and above
    format='%(asctime)s - %(levelname)s - %(message)s'  # Format: time - level - message
)
logger = logging.getLogger(__name__)  # Create our logger

# EXPLANATION:
# - PyPDF2: Reads PDF files and extracts text from them
# - logging: Instead of using print(), we use logging to track what happens
# - Path: Better than strings for file paths (works on Windows, Mac, Linux)
# - Optional: Tells Python "this parameter might be None"

# ============================================================================
# PART 2: CLASS DEFINITION AND CONSTRUCTOR
# ============================================================================

class PDFExtractor:
    """
    Simple PDF text extractor for Colombian decree documents.
    """
    
    def __init__(self, pdf_folder: str = "data/raw", output_folder: str = "data/raw"):
        # Convert string paths to Path objects
        self.pdf_folder = Path(pdf_folder)      # Where to find PDF files
        self.output_folder = Path(output_folder) # Where to save .txt files
        
        # Create the output folder if it doesn't exist
        self.output_folder.mkdir(exist_ok=True)

# EXPLANATION:
# - __init__ is the "constructor" - runs when you create a PDFExtractor object
# - self.pdf_folder: stores where your PDFs are
# - self.output_folder: stores where to save extracted text
# - mkdir(exist_ok=True): creates folder if needed, doesn't crash if it exists
# - Default values: if you don't specify folders, uses "data/raw"

# EXAMPLE USAGE:
# extractor = PDFExtractor()  # Uses default folders
# extractor = PDFExtractor("my_pdfs", "my_texts")  # Custom folders

# ============================================================================
# PART 3: MAIN EXTRACTION FUNCTION
# ============================================================================

def extract_text_from_pdf(self, pdf_filename: str, output_filename: Optional[str] = None) -> str:
    """
    Extract text from a single PDF file.
    
    Args:
        pdf_filename: Name of the PDF file (like "decreto.pdf")
        output_filename: What to name the .txt file (optional)
        
    Returns:
        The extracted text as a string
    """
    # Build the full path to the PDF file
    pdf_path = self.pdf_folder / pdf_filename
    
    # Check if file exists before trying to open it
    if not pdf_path.exists():
        logger.error(f"PDF file not found: {pdf_path}")
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

# EXPLANATION:
# - pdf_path = self.pdf_folder / pdf_filename: combines folder + filename
# - pdf_path.exists(): checks if file is really there
# - raise FileNotFoundError: stops the program with an error message if file missing
# - Optional[str]: means output_filename can be a string OR None

# ============================================================================
# PART 4: OPENING AND READING THE PDF
# ============================================================================

    try:
        # Open PDF file in binary read mode ('rb')
        with open(pdf_path, 'rb') as pdf_file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Initialize empty string to collect all text
            full_text = ""
            
            # Get total number of pages
            total_pages = len(pdf_reader.pages)
            logger.info(f"Extracting text from {total_pages} pages...")

# EXPLANATION:
# - 'rb': read binary mode (PDFs are binary files, not text files)
# - with open(): automatically closes file when done (good practice)
# - PyPDF2.PdfReader(): creates an object that can read the PDF
# - pdf_reader.pages: list of all pages in the PDF
# - len(pdf_reader.pages): counts how many pages

# ============================================================================
# PART 5: EXTRACTING TEXT FROM EACH PAGE
# ============================================================================

            # Loop through each page
            for page_num, page in enumerate(pdf_reader.pages, 1):
                try:
                    # Extract text from this page
                    page_text = page.extract_text()
                    
                    # Add page text to our full text (with spacing)
                    full_text += page_text + "\n\n"
                    
                    # Log progress
                    logger.info(f"Processed page {page_num}/{total_pages}")
                    
                except Exception as e:
                    # If this page fails, log warning but continue
                    logger.warning(f"Error extracting page {page_num}: {str(e)}")
                    continue

# EXPLANATION:
# - enumerate(pdf_reader.pages, 1): gives us (page_number, page_object) starting from 1
# - page.extract_text(): gets all text from this page
# - full_text += page_text + "\n\n": adds page text + two newlines for spacing
# - try/except: if one page fails, we skip it and continue with others

# ============================================================================
# PART 6: CLEANING AND SAVING THE TEXT
# ============================================================================

            # Clean up the extracted text
            full_text = self._clean_extracted_text(full_text)
            
            # Create output filename if not provided
            if not output_filename:
                output_filename = pdf_filename.replace('.pdf', '.txt')
            
            # Save to .txt file
            output_path = self.output_folder / output_filename
            with open(output_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(full_text)
            
            # Log success info
            logger.info(f"Text saved to: {output_path}")
            logger.info(f"Extracted {len(full_text.split())} words total")
            
            return full_text

# EXPLANATION:
# - self._clean_extracted_text(): calls our cleaning function (see below)
# - replace('.pdf', '.txt'): changes "decreto.pdf" to "decreto.txt"
# - encoding='utf-8': saves with proper encoding for Spanish accents
# - len(full_text.split()): counts words by splitting on spaces

# ============================================================================
# PART 7: TEXT CLEANING FUNCTION
# ============================================================================

def _clean_extracted_text(self, text: str) -> str:
    """
    Clean text extracted from PDF to improve readability.
    """
    import re  # Regular expressions for pattern matching
    
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)  # Max 2 newlines
    text = re.sub(r'[ \t]+', ' ', text)     # Normalize spaces and tabs
    
    # Fix common PDF extraction issues
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Add spaces between joined words
    text = re.sub(r'(\d)([A-Za-z])', r'\1 \2', text)  # Space between numbers and letters
    text = re.sub(r'([A-Za-z])(\d)', r'\1 \2', text)  # Space between letters and numbers

# EXPLANATION OF REGEX PATTERNS:
# - r'\n{3,}': 3 or more newlines
# - r'[ \t]+': one or more spaces or tabs
# - r'([a-z])([A-Z])': lowercase letter followed by uppercase letter
# - r'\1 \2': replace with first group + space + second group
# - The underscore before _clean_extracted_text means it's "private" (internal use)

# EXAMPLE OF WHAT IT FIXES:
# Before: "palabraSIGUIENTE123texto"
# After:  "palabra SIGUIENTE 123 texto"

# ============================================================================
# PART 8: BATCH PROCESSING FUNCTION
# ============================================================================

def extract_all_pdfs(self):
    """
    Extract text from all PDF files in the pdf_folder.
    """
    # Find all PDF files in the folder
    pdf_files = list(self.pdf_folder.glob("*.pdf"))
    
    if not pdf_files:
        logger.warning("No PDF files found in the specified folder")
        return
    
    logger.info(f"Found {len(pdf_files)} PDF files to process")
    
    # Process each PDF file
    for pdf_file in pdf_files:
        try:
            logger.info(f"Processing: {pdf_file.name}")
            self.extract_text_from_pdf(pdf_file.name)
            logger.info(f"Successfully processed: {pdf_file.name}")
        except Exception as e:
            logger.error(f"Failed to process {pdf_file.name}: {str(e)}")
            continue

# EXPLANATION:
# - .glob("*.pdf"): finds all files ending with .pdf
# - list(): converts the results to a list
# - pdf_file.name: just the filename, not the full path
# - try/except: if one file fails, continue with the others

# ============================================================================
# PART 9: SPECIFIC FUNCTION FOR DECRETO 1194
# ============================================================================

def extract_decreto_1194():
    """
    Specific function to extract Decreto 1194 de 1989
    """
    extractor = PDFExtractor()
    
    # Try different possible filenames (people name files differently)
    possible_names = [
        "decreto_1194_1989.pdf",
        "Decreto_1194_1989.pdf", 
        "decreto-1194-1989.pdf",
        "1194.pdf"
    ]
    
    # Try each possible name
    for filename in possible_names:
        try:
            text = extractor.extract_text_from_pdf(filename, "decreto_1194_1989.txt")
            print(f"✅ Successfully extracted: {filename}")
            print(f"📄 First 200 characters:")
            print(text[:200] + "...")  # Show first 200 characters
            return text
        except FileNotFoundError:
            continue  # Try the next filename
    
    # If none worked, show what files are available
    print("❌ Could not find Decreto 1194 PDF file")
    print("📁 Available PDF files:")
    pdf_files = list(Path("data/raw").glob("*.pdf"))
    for pdf in pdf_files:
        print(f"   - {pdf.name}")

# EXPLANATION:
# - Tries multiple common naming patterns
# - text[:200]: gets first 200 characters (slice notation)
# - if all filenames fail, shows what PDF files are actually there
# - return text: gives back the extracted text to whoever called this function

# ============================================================================
# PART 10: RUNNING THE PROGRAM
# ============================================================================

if __name__ == "__main__":
    print("🔧 PDF Text Extractor for Colombian Decrees")
    print("=" * 50)
    
    # Try to extract Decreto 1194
    extract_decreto_1194()

# EXPLANATION:
# - if __name__ == "__main__": only runs when you execute this file directly
# - Doesn't run when you import this file into another program
# - "=" * 50: creates a line of 50 equal signs for formatting