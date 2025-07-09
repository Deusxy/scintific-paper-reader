import fitz  # PyMuPDF

def extract_text(pdf_file):
    """Extract text from uploaded PDF file."""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text
