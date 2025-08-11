import re
import fitz  # PyMuPDF


def _clean_block_text(txt: str) -> str:
    """Normalize block text: fix hyphenation, collapse spaces, keep paragraph breaks."""
    if not txt:
        return ""
    # Normalize NBSP and weird spaces
    txt = txt.replace("\xa0", " ")
    # Join hyphenated line breaks: word-\nword -> wordword
    txt = re.sub(r"(\w)-\n(\w)", r"\1\2", txt)
    # Replace newlines within paragraphs with spaces, but keep empty-line paragraph breaks
    # First collapse 3+ newlines to 2
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    # Replace single newlines between non-empty chars with a space
    txt = re.sub(r"([^\n])\n([^\n])", r"\1 \2", txt)
    # Collapse multiple spaces
    txt = re.sub(r"[ \t]{2,}", " ", txt)
    return txt.strip()


def extract_text(pdf_file):
    """Extract reasonably clean text from a PDF, skipping headers/footers and captions.

    Heuristics:
    - Skip top/bottom 10% of page height (likely headers/footers)
    - Filter out common caption starters (Figure, Table, Eq.)
    - Fix hyphenation and preserve paragraph breaks
    """
    # Read bytes once; some uploaders have non-seekable streams
    pdf_bytes = pdf_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page_texts = []

    for page in doc:
        height = page.rect.height
        top_cut = 0.10 * height
        bot_cut = 0.90 * height

        # Use block extraction for positions
        blocks = page.get_text("blocks") or []

        # Sort blocks by y, then x
        blocks.sort(key=lambda b: (b[1], b[0]))

        parts = []
        for b in blocks:
            # blocks tuple: (x0, y0, x1, y1, text, block_no, block_type, ...)
            if len(b) < 5:
                continue
            x0, y0, x1, y1, btxt = b[:5]

            # Skip likely headers/footers
            if y1 <= top_cut or y0 >= bot_cut:
                continue

            # Heuristic skip captions/refs
            low = (btxt or "").strip().lower()
            if low.startswith((
                "figure ", "figure:", "fig ", "fig.", "fig:",
                "table ", "table:", "tab ", "tab.", "tab:",
                "equation", "eq ", "eq.", "eq:",
                "supplementary", "appendix", "reference", "references"
            )):
                continue

            cleaned = _clean_block_text(btxt)
            if cleaned:
                parts.append(cleaned)

        # Join blocks with double newline to encourage paragraph separation
        page_text = "\n\n".join(parts).strip()
        if page_text:
            page_texts.append(page_text)

    doc.close()
    return "\n\n".join(page_texts)
