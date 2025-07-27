"""
Module for parsing PDF files and extracting page-wise text.
"""

import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path):
    pages = []
    with fitz.open(pdf_path) as doc:
        for i, page in enumerate(doc, start=1):
            text = page.get_text()
            pages.append({
                "page_number": i,
                "text": text
            })
    return pages
