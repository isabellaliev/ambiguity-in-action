# debug_poppler.py
import os
from pathlib import Path
from pdf2image import convert_from_path

def test_poppler_paths():
    """Test different possible poppler paths"""
    
    possible_paths = [
        r'C:\Program Files\poppler-25.07.0\Library\bin',
        r'C:\Program Files\poppler-25.07.0\bin',
        r'C:\Program Files\poppler-25.07.0',
        r'C:\Program Files\poppler-25.07.0\Library',
        # Add more if needed
    ]
    
    print(" Testing poppler paths...")
    
    for path in possible_paths:
        print(f"\n Testing: {path}")
        
        if not Path(path).exists():
            print(" Path doesn't exist")
            continue
            
        print(" Path exists!")
        
        # List files in the directory
        try:
            files = list(Path(path).glob("*.exe"))
            print(f" Found {len(files)} .exe files:")
            for file in files[:5]:  # Show first 5
                print(f"   - {file.name}")
            
            # Look for key files
            key_files = ['pdftoppm.exe', 'pdfinfo.exe', 'pdftocairo.exe']
            found_files = [f for f in key_files if (Path(path) / f).exists()]
            
            if found_files:
                print(f" Found key poppler files: {found_files}")
                return path  # This looks like the right path
            else:
                print("  No key poppler files found here")
                
        except Exception as e:
            print(f" Error reading directory: {e}")
    
    return None

def test_pdf_conversion(poppler_path=None):
    """Test actual PDF conversion"""
    
    print(f"\n Testing PDF conversion...")
    
    pdf_path = Path("data/raw/Decreto 1194 - 1989.pdf")
    
    if not pdf_path.exists():
        print(f" Test PDF not found: {pdf_path}")
        return
    
    try:
        if poppler_path:
            print(f"Using poppler path: {poppler_path}")
            images = convert_from_path(pdf_path, dpi=150, poppler_path=poppler_path, first_page=1, last_page=1)
        else:
            print("Trying without poppler_path (using PATH)")
            images = convert_from_path(pdf_path, dpi=150, first_page=1, last_page=1)
            
        print(f" SUCCESS! Converted 1 page. Image size: {images[0].size}")
        return True
        
    except Exception as e:
        print(f" FAILED: {e}")
        return False

def check_path_environment():
    """Check if poppler is in PATH"""
    print("\n Checking PATH environment...")
    
    path_env = os.environ.get('PATH', '')
    poppler_in_path = any('poppler' in p.lower() for p in path_env.split(';'))
    
    if poppler_in_path:
        print(" Found 'poppler' in PATH")
        poppler_paths = [p for p in path_env.split(';') if 'poppler' in p.lower()]
        for p in poppler_paths:
            print(f"   - {p}")
    else:
        print(" No 'poppler' found in PATH")

if __name__ == "__main__":
    print(" Poppler Diagnostic Tool")
    print("=" * 40)
    
    # Test 1: Check PATH
    check_path_environment()
    
    # Test 2: Find correct poppler path
    correct_path = test_poppler_paths()
    
    # Test 3: Try PDF conversion
    if correct_path:
        print(f"\n Using discovered path: {correct_path}")
        success = test_pdf_conversion(correct_path)
    else:
        print(f"\n No poppler path found, trying without path...")
        success = test_pdf_conversion()
    
    if success:
        print(f"\n POPPLER IS WORKING!")
        if correct_path:
            print(f" Use this path in your OCR script:")
            print(f"POPPLER_PATH = r'{correct_path}'")
    else:
        print(f"\n Still having issues...")