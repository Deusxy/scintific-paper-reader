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
        except Exception:
            nltk.download('punkt', quiet=True)


def is_unwanted_content(line: str, mode: str = "balanced") -> bool:
    """Check if a line contains unwanted content based on mode."""
    line_lower = line.lower()

    # URLs and web references
    if any(term in line_lower for term in ['http', 'www', '.com', '.org', '.edu', 'doi:']):
        return True

    # Obvious captions/sections
    figure_prefixes = [
        'figure', 'fig.', 'fig ', 'table', 'tab.', 'tab ', 'equation', 'eq.', 'eq ',
        'formula', 'theorem', 'lemma', 'corollary', 'proof', 'algorithm'
    ]
    if any(line_lower.startswith(prefix) for prefix in figure_prefixes):
        return True

    if any(line_lower.startswith(prefix) for prefix in [
        'abstract', 'keywords', 'introduction', 'conclusion', 'references', 'bibliography',
        'appendix', 'acknowledgment', 'author', 'copyright', 'page ', 'chapter',
        'section', 'subsection', 'footnote', 'endnote'
    ]):
        return True

    # Brackets and math only in strict mode
    if mode == 'strict' and any(ch in line for ch in ['(', ')', '[', ']', '{', '}']):
        return True

    math_symbols = ['=', '+', '-', '*', '/', '<', '>', '±', '≤', '≥', '∑', '∏', '∫', '∆', '∇', '∞', 'α', 'β', 'γ', 'δ', 'λ', 'μ', 'π', 'σ', 'θ']
    if mode == 'strict' and any(symbol in line for symbol in math_symbols):
        return True
    if mode == 'strict' and re.search(r'\d+\s*[+\-*/=]\s*\d+', line):
        return True

    # Lines with lots of numbers (tables)
    words = line.split()
    if words:
        number_words = sum(1 for w in words if re.search(r'\d', w))
        if mode == 'strict' and number_words / len(words) > 0.4:
            return True

    # Decorative/vertical separators
    if any(ind in line for ind in ['_____', '-----', '*****', '.....']):
        return True

    # Shouting headers
    if len(line) > 10 and line.isupper():
        return True

    # Very short fragments in strict mode
    if mode == 'strict' and len(words) < 5:
        return True

    # Punctuation noise in strict mode
    punct_count = sum(1 for ch in line if ch in '.,;:!?-_*#@$%^&')
    if mode == 'strict' and len(line) > 0 and punct_count / len(line) > 0.3:
        return True

    return False


def clean_text(text: str, mode: str = 'balanced') -> str:
    """Clean and filter text into paragraph-like content."""
    lines = text.split('\n')
    cleaned_lines = []

    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        if is_unwanted_content(line, mode=mode):
            continue

        line = re.sub(r'\s+', ' ', line)
        line = re.sub(r"[^\w\s\.,!?;:'-]", '', line)

        if mode == 'strict' and len(line) < 20:
            continue

        words = line.split()
        if mode == 'strict':
            if len(words) >= 5:
                cleaned_lines.append(line)
        else:
            if len(words) >= 3:
                cleaned_lines.append(line)

    return ' '.join(cleaned_lines)


def split_sentences(text: str, mode: str = 'balanced'):
    """Split text into sentences and filter them."""
    try:
        ensure_nltk_data()
        sentences = sent_tokenize(text)
    except Exception as e:
        print(f"NLTK tokenization failed: {e}")
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)

    cleaned_sentences = []
    for raw in sentences:
        sentence = raw.strip()
        if not sentence:
            continue

        if mode == 'strict' and len(sentence) < 25:
            continue

        if is_unwanted_content(sentence, mode=mode):
            continue

        words = sentence.split()
        if mode == 'strict' and len(words) < 6:
            continue

        sentence = re.sub(r'\s+', ' ', sentence)
        if not sentence.endswith(('.', '!', '?')):
            sentence += '.'

        if mode == 'strict':
            if len(sentence) >= 25 and len(words) >= 6:
                cleaned_sentences.append(sentence)
        else:
            if len(words) >= 4 and len(sentence) >= 15:
                cleaned_sentences.append(sentence)

    return cleaned_sentences


def analyze_text_quality(text: str, mode: str = 'balanced'):
    """Analyze counts for filtered vs readable lines."""
    lines = text.split('\n')
    total_lines = len([ln for ln in lines if ln.strip()])

    stats = {
        'total_lines': total_lines,
        'filtered_out': 0,
        'readable_lines': 0,
        'brackets_removed': 0,
        'formulas_removed': 0,
        'headers_removed': 0,
        'urls_removed': 0,
    }

    for raw in lines:
        line = raw.strip()
        if not line:
            continue

        if is_unwanted_content(line, mode=mode):
            stats['filtered_out'] += 1
            if any(ch in line for ch in ['(', ')', '[', ']', '{', '}']):
                stats['brackets_removed'] += 1
            if any(sym in line for sym in ['=', '+', '-', '*', '/', '<', '>']):
                stats['formulas_removed'] += 1
            if any(line.lower().startswith(prefix) for prefix in ['figure', 'table', 'abstract']):
                stats['headers_removed'] += 1
            if any(term in line.lower() for term in ['http', 'www', '.com']):
                stats['urls_removed'] += 1
        else:
            stats['readable_lines'] += 1

    stats['readable_percentage'] = (stats['readable_lines'] / total_lines) * 100 if total_lines else 0
    return stats
