# src/preprocessing/data_loader.py
import os
import logging
from pathlib import Path
import re
from typing import Dict, List, Tuple
import pandas as pd

# Set up logging to track preprocessing steps
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DecreeDataLoader:
    """
    Data loader for Colombian decree texts.
    Handles loading, cleaning, and basic preprocessing of legal documents.
    """
    
    def __init__(self, raw_data_path: str = "data/raw", processed_data_path: str = "data/processed"):
        self.raw_path = Path(raw_data_path)
        self.processed_path = Path(processed_data_path)
        self.processed_path.mkdir(exist_ok=True)
        
        # Create backup directory for raw texts
        self.backup_path = Path("data/backup")
        self.backup_path.mkdir(exist_ok=True)
        
    def load_decree_text(self, filename: str) -> str:
        """
        Load a single decree text file.
        
        Args:
            filename: Name of the text file
            
        Returns:
            Raw text content of the decree
        """
        file_path = self.raw_path / filename
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                logger.info(f"Successfully loaded {filename}")
                return text
        except FileNotFoundError:
            logger.error(f"File not found: {filename}")
            raise
        except UnicodeDecodeError:
            # Try different encodings if UTF-8 fails
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    text = file.read()
                    logger.warning(f"Loaded {filename} with latin-1 encoding")
                    return text
            except:
                logger.error(f"Could not decode {filename}")
                raise
    
    def clean_text(self, text: str) -> str:
        """
        Clean text by removing special characters and normalizing whitespace.
        Preserves Spanish accents and legal formatting.
        
        Args:
            text: Raw decree text
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace but preserve paragraph structure
        text = re.sub(r'\n{3,}', '\n\n', text)  # Max 2 newlines
        text = re.sub(r'[ \t]+', ' ', text)     # Normalize spaces/tabs
        
        # Remove special characters but keep legal punctuation
        # Keep: letters, numbers, accents, basic punctuation, Spanish chars
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\(\)\-\"\'\ñÑáéíóúÁÉÍÓÚüÜ]', ' ', text)
        
        # Clean up multiple spaces created by character removal
        text = re.sub(r'\s+', ' ', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        logger.info("Text cleaning completed")
        return text
    
    def extract_metadata(self, text: str, filename: str) -> Dict:
        """
        Extract basic metadata from decree text.
        
        Args:
            text: Decree text content
            filename: Original filename
            
        Returns:
            Dictionary with metadata
        """
        metadata = {
            'filename': filename,
            'word_count': len(text.split()),
            'char_count': len(text),
            'paragraph_count': len(text.split('\n\n'))
        }
        
        # Try to extract decree number and date from text
        decreto_pattern = r'DECRETO\s+(?:NÚMERO\s+)?(\d+)\s+DE\s+(\d{4})'
        ley_pattern = r'LEY\s+(\d+)\s+DE\s+(\d{4})'
        
        decreto_match = re.search(decreto_pattern, text, re.IGNORECASE)
        ley_match = re.search(ley_pattern, text, re.IGNORECASE)
        
        if decreto_match:
            metadata['document_type'] = 'DECRETO'
            metadata['number'] = decreto_match.group(1)
            metadata['year'] = decreto_match.group(2)
        elif ley_match:
            metadata['document_type'] = 'LEY'
            metadata['number'] = ley_match.group(1)
            metadata['year'] = ley_match.group(2)
        else:
            metadata['document_type'] = 'UNKNOWN'
            metadata['number'] = None
            metadata['year'] = None
        
        return metadata
    
    def save_processed_text(self, text: str, metadata: Dict, output_filename: str = None):
        """
        Save processed text and create backup of original.
        
        Args:
            text: Processed text
            metadata: Document metadata
            output_filename: Optional custom output filename
        """
        if not output_filename:
            base_name = metadata['filename'].replace('.txt', '')
            output_filename = f"{base_name}_processed.txt"
        
        # Save processed text
        processed_file = self.processed_path / output_filename
        with open(processed_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        # Save metadata
        metadata_file = self.processed_path / f"{output_filename.replace('.txt', '_metadata.txt')}"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            for key, value in metadata.items():
                f.write(f"{key}: {value}\n")
        
        logger.info(f"Processed text saved as {output_filename}")
        logger.info(f"Metadata saved for {output_filename}")
    
    def process_all_decrees(self) -> List[Dict]:
        """
        Process all decree files in the raw data directory.
        
        Returns:
            List of metadata dictionaries for all processed files
        """
        all_metadata = []
        txt_files = list(self.raw_path.glob("*.txt"))
        
        if not txt_files:
            logger.warning("No .txt files found in raw data directory")
            return all_metadata
        
        for txt_file in txt_files:
            try:
                # Load original text
                original_text = self.load_decree_text(txt_file.name)
                
                # Create backup
                backup_file = self.backup_path / txt_file.name
                with open(backup_file, 'w', encoding='utf-8') as f:
                    f.write(original_text)
                
                # Clean text
                cleaned_text = self.clean_text(original_text)
                
                # Extract metadata
                metadata = self.extract_metadata(cleaned_text, txt_file.name)
                
                # Save processed version
                self.save_processed_text(cleaned_text, metadata)
                
                all_metadata.append(metadata)
                
            except Exception as e:
                logger.error(f"Error processing {txt_file.name}: {str(e)}")
                continue
        
        # Save summary metadata
        self.save_processing_summary(all_metadata)
        
        return all_metadata
    
    def save_processing_summary(self, all_metadata: List[Dict]):
        """Save a summary of all processed files."""
        df = pd.DataFrame(all_metadata)
        summary_file = self.processed_path / "processing_summary.csv"
        df.to_csv(summary_file, index=False)
        logger.info(f"Processing summary saved to {summary_file}")

# Example usage and testing
if __name__ == "__main__":
    # Initialize the data loader
    loader = DecreeDataLoader()
    
    # Process all decree files
    print("Starting decree processing...")
    metadata = loader.process_all_decrees()
    
    print(f"\nProcessed {len(metadata)} decree files:")
    for meta in metadata:
        print(f"- {meta['filename']}: {meta['word_count']} words, {meta['document_type']} {meta['number']} de {meta['year']}")