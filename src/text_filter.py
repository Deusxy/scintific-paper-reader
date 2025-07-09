import re
import nltk
from nltk.tokenize import sent_tokenize

def ensure_nltk_data():
    """Ensure required NLTK data is downloaded."""
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        try:
            nltk.download('punkt_tab', quiet=True)
        except:
            # Fallback to older punkt if punkt_tab fails
            nltk.download('punkt', quiet=True)

def clean_text(text):
    """Clean and filter text to remove unwanted content."""
    lines = text.split('\n')
    filtered_lines = []
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines or very short lines
        if not line or len(line) < 30:
            continue
            
        # Skip common non-content patterns
        if any([
            line.lower().startswith(('figure', 'table', 'doi', 'reference', 'abstract', 'keywords')),
            line.lower().startswith(('fig.', 'tab.', 'eq.', 'appendix')),
            re.search(r'\[[^\]]+\]', line),  # square brackets [1], [23]
            re.search(r'\([^\)]{1,3}\)', line),  # short parentheses (1), (a)
            re.search(r'\{[^\}]+\}', line),  # curly brackets {formula}
            'http' in line.lower() or 'www' in line.lower(),  # URLs
            re.search(r'\d+(\.\d+){2,}', line),  # version numbers like 1.2.3
            re.search(r'^[A-Z\s]{10,}$', line),  # ALL CAPS headers
            re.search(r'^\d+\.\d+\s*$', line),  # standalone numbers
            re.search(r'^[^\w\s]*$', line),  # only special characters
            line.count('_') > 3,  # underscores (often formatting)
            line.count('*') > 2,  # asterisks (often formatting)
        ]):
            continue
            
        # Clean up the line
        line = re.sub(r'\s+', ' ', line)  # normalize whitespace
        line = re.sub(r'[^\w\s.,!?;:()-]', '', line)  # remove special chars
        
        if len(line) > 30:  # final length check
            filtered_lines.append(line)
    
    return " ".join(filtered_lines)

def split_sentences(text):
    """Split text into sentences using NLTK or fallback to regex."""
    try:
        ensure_nltk_data()
        sentences = sent_tokenize(text)
        # Filter out very short sentences
        return [sentence.strip() for sentence in sentences if len(sentence.strip()) > 10]
    except Exception as e:
        print(f"NLTK tokenization failed: {e}")
        # Fallback to simple regex-based sentence splitting
        import re
        sentences = re.split(r'[.!?]+\s+', text)
        # Clean and filter sentences
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10 and not sentence.endswith('.'):
                sentence += '.'
            if len(sentence) > 10:
                cleaned_sentences.append(sentence)
        return cleaned_sentences
