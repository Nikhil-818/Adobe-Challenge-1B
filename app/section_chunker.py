"""
Module for chunking PDFs into titled sections using heuristics.
"""

import re


def chunk_sections(pages, doc_name):
    sections = []
    for page in pages:
        paragraphs = page["text"].split("\n\n")
        for para in paragraphs:
            if is_potential_heading(para):
                sections.append({
                    "document": doc_name,
                    "section_title": para.strip(),
                    "section_text": para.strip(),
                    "page_number": page["page_number"]
                })
    return sections


def is_potential_heading(text):
    # Example: match ALL CAPS or numbered headings
    return bool(re.match(r"^(?:(?:[A-Z][A-Z\s]+)|(?:\\d+\\.\\s))", text.strip()))
