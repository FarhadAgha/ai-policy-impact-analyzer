"""
pdf_processor.py

Extracts text from a PDF, keeping track of which page each
piece of text came from. This page-tagging is what makes
citations possible later in the pipeline.
"""

import fitz  # this is PyMuPDF's import name


def extract_text_by_page(pdf_path: str) -> list[dict]:
    """
    Extract text from a PDF, one entry per page.

    Args:
        pdf_path: path to the PDF file on disk.

    Returns:
        A list of dicts, one per page, like:
        [
            {"page_number": 1, "text": "..."},
            {"page_number": 2, "text": "..."},
            ...
        ]
        Pages with no extractable text (e.g. pure scanned
        images) are still included, with text as an empty string,
        so page numbering stays accurate downstream.
    """
    doc = fitz.open(pdf_path)
    pages = []

    for page_index in range(len(doc)):
        page = doc[page_index]
        raw_text = page.get_text()
        cleaned_text = _clean_text(raw_text)

        pages.append({
            "page_number": page_index + 1,  # human-readable, 1-indexed
            "text": cleaned_text
        })

    doc.close()
    return pages


def _clean_text(text: str) -> str:
    """
    Light cleanup: collapse excessive whitespace/line breaks
    that PDF extraction often introduces, without altering
    the actual words.
    """
    lines = [line.strip() for line in text.split("\n")]
    lines = [line for line in lines if line]  # drop empty lines
    return " ".join(lines)


def get_document_metadata(pdf_path: str) -> dict:
    """
    Pull whatever basic metadata the PDF itself exposes
    (title, author, etc.) — often incomplete or missing,
    which is expected and fine; we don't invent what's not there.
    """
    doc = fitz.open(pdf_path)
    metadata = doc.metadata or {}
    doc.close()

    return {
        "title": metadata.get("title") or None,
        "author": metadata.get("author") or None,
        "page_count": len(fitz.open(pdf_path)),
    }