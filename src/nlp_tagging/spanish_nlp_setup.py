# Basic Spanish NLP Setup for ambiguity-in-action
# Phase 1, Part 3: Load spaCy, create POS tagger, and extract lemmatized versions

import spacy
import os
import json
from pathlib import Path

def load_and_test_spacy_model():
    """
    Load the Spanish spaCy model and test it with a simple sentence.
    Think of this like loading a Spanish dictionary and grammar book into memory.
    """
    print("Loading Spanish spaCy model...")
    
    try:
        # Load the Spanish model we downloaded
        nlp = spacy.load("es_core_news_lg")
        print("Spanish model loaded successfully!")
        
        # Test with a simple Spanish sentence
        test_sentence = "El gobierno debe implementar nuevas políticas públicas."
        doc = nlp(test_sentence)
        
        print(f"\nTesting with: '{test_sentence}'")
        print("Word analysis:")
        for token in doc:
            print(f"  '{token.text}' -> POS: {token.pos_}, Lemma: '{token.lemma_}'")
        
        return nlp
        
    except OSError:
        print("Error: Spanish model not found!")
        print("Please run: python -m spacy download es_core_news_lg")
        return None

def create_pos_tagging_function(nlp):
    """
    Create a function that takes text and returns POS tags for each word.
    POS = Part of Speech (like noun, verb, adjective)
    """
    def analyze_pos_tags(text):
        """
        Analyze a text and return detailed information about each word.
        
        Args:
            text (str): The Spanish text to analyze
            
        Returns:
            list: List of dictionaries with word information
        """
        # Process the text with spaCy
        doc = nlp(text)
        
        # Create a list to store our analysis
        word_analysis = []
        
        for token in doc:
            # Skip punctuation and spaces for cleaner output
            if not token.is_punct and not token.is_space:
                word_info = {
                    'text': token.text,           # The original word
                    'lemma': token.lemma_,        # Root form of the word
                    'pos': token.pos_,            # Part of speech (NOUN, VERB, etc.)
                    'tag': token.tag_,            # More detailed grammatical tag
                    'is_alpha': token.is_alpha,   # Is it a real word (not number/punctuation)?
                    'is_stop': token.is_stop      # Is it a common word like "el", "de", "y"?
                }
                word_analysis.append(word_info)
        
        return word_analysis
    
    return analyze_pos_tags

def extract_and_save_lemmatized_versions(nlp, input_folder="data/processed", output_folder="data/lemmatized"):
    """
    Take our cleaned decree texts, extract lemmatized versions, and save them.
    Lemmatization = converting words to their base form (like "corrían" -> "correr")
    """
    # Create output folder if it doesn't exist
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    # Check if input folder exists and show the actual path being checked
    print(f"Looking for files in: {os.path.abspath(input_folder)}")
    
    if not os.path.exists(input_folder):
        print(f"Input folder '{input_folder}' not found!")
        print("Make sure you've run the data loader and cleaning steps first.")
        print("Current working directory:", os.getcwd())
        return
    
    # Find all .txt files in the input folder
    txt_files = list(Path(input_folder).glob("*.txt"))
    
    if not txt_files:
        print(f"No .txt files found in '{input_folder}'")
        # Let's see what files ARE there
        all_files = list(Path(input_folder).glob("*"))
        print("Files found in folder:")
        for file in all_files:
            print(f"  {file.name}")
        return
    
    # Filter out metadata files
    decree_files = [f for f in txt_files if 'metadata' not in f.name.lower()]
    
    print(f"Found {len(txt_files)} total .txt files")
    print(f"Processing {len(decree_files)} decree files (skipping metadata files)")
    
    if not decree_files:
        print("No decree files to process after filtering!")
        return
    
    # Process each file
    lemmatized_results = {}
    
    for file_path in decree_files:
        print(f"Processing: {file_path.name}")
        
        try:
            # Read the text file
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Process with spaCy
            doc = nlp(text)
            
            # Extract lemmatized text
            lemmatized_words = []
            original_words = []
            
            for token in doc:
                if not token.is_punct and not token.is_space:
                    original_words.append(token.text)
                    lemmatized_words.append(token.lemma_)
            
            # Save lemmatized version as text file
            lemmatized_text = " ".join(lemmatized_words)
            output_file = Path(output_folder) / f"lemmatized_{file_path.name}"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(lemmatized_text)
            
            # Store results for summary
            lemmatized_results[file_path.name] = {
                'original_words': len(original_words),
                'unique_original': len(set(original_words)),
                'unique_lemmatized': len(set(lemmatized_words)),
                'reduction_percentage': round((1 - len(set(lemmatized_words))/len(set(original_words))) * 100, 2)
            }
            
            print(f"  Saved: {output_file.name}")
            
        except Exception as e:
            print(f"  Error processing {file_path.name}: {e}")
    
    # Save summary statistics
    summary_file = Path(output_folder) / "lemmatization_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(lemmatized_results, f, indent=2, ensure_ascii=False)
    
    print(f"\nSummary saved to: {summary_file}")
    return lemmatized_results

def test_on_sample_decrees(nlp, pos_function, input_folder="data/processed", num_samples=3):
    """
    Test our NLP functions on 2-3 sample decrees to make sure everything works.
    """
    print(f"\nTesting NLP functions on sample decrees...")
    
    # Find available text files
    txt_files = list(Path(input_folder).glob("*.txt"))
    # Filter out metadata files
    decree_files = [f for f in txt_files if 'metadata' not in f.name.lower()]
    
    # Take up to num_samples files
    sample_files = decree_files[:num_samples]
    
    if not sample_files:
        print(f"No sample files found in '{input_folder}'")
        return
    
    for i, file_path in enumerate(sample_files, 1):
        print(f"\n--- Sample {i}: {file_path.name} ---")
        
        try:
            # Read first few lines for testing (not the whole document)
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # Take first 3 sentences or first 200 characters, whichever is shorter
                sample_text = " ".join(lines[:3])[:200]
            
            print(f"Sample text: {sample_text}...")
            
            # Test POS tagging
            pos_results = pos_function(sample_text)
            
            print("POS Analysis (first 10 words):")
            for word_info in pos_results[:10]:
                print(f"  {word_info['text']} -> {word_info['pos']} (lemma: {word_info['lemma']})")
            
            # Show some statistics
            total_words = len(pos_results)
            verbs = len([w for w in pos_results if w['pos'] == 'VERB'])
            nouns = len([w for w in pos_results if w['pos'] == 'NOUN'])
            
            print(f"Quick stats: {total_words} words, {verbs} verbs, {nouns} nouns")
            
        except Exception as e:
            print(f"Error testing {file_path.name}: {e}")

def main():
    """
    Main function that runs all our NLP setup steps.
    """
    print("Starting Basic Spanish NLP Setup...")
    print("=" * 50)
    
    # Step 1: Load and test spaCy Spanish model
    nlp = load_and_test_spacy_model()
    if nlp is None:
        return
    
    print("\n" + "=" * 50)
    
    # Step 2: Create basic POS tagging function
    print("Creating POS tagging function...")
    pos_function = create_pos_tagging_function(nlp)
    print("POS tagging function created!")
    
    print("\n" + "=" * 50)
    
    # Step 3: Extract and save lemmatized versions
    print("Extracting and saving lemmatized versions...")
    results = extract_and_save_lemmatized_versions(nlp)
    
    if results:
        print("\nLemmatization Results Summary:")
        for filename, stats in results.items():
            print(f"  {filename}:")
            print(f"    Original unique words: {stats['unique_original']}")
            print(f"    Lemmatized unique words: {stats['unique_lemmatized']}")
            print(f"    Vocabulary reduction: {stats['reduction_percentage']}%")
    
    print("\n" + "=" * 50)
    
    # Step 4: Test on sample decrees
    test_on_sample_decrees(nlp, pos_function)
    
    print("\nBasic Spanish NLP Setup Complete!")
    print("Next steps: Move on to Phase 2 - Core Analysis Development")

if __name__ == "__main__":
    main()