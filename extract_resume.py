import fitz  # type: ignore # PyMuPDF

def extract_text_from_pdf(pdf_bytes):
    """
    Extracts text from a PDF byte stream.
    """
    if not pdf_bytes:
        raise ValueError("PDF byte stream is empty.")
    
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text
