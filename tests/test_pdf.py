import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pdf_processor import extract_text_by_page, get_document_metadata

pdf_path = "data/sample_policies/YOUR_FILE_NAME.pdf"  # update this
pdf_path = "data/sample_policies/TA-9-2024-0138_EN.pdf"

pages = extract_text_by_page(pdf_path)
print(f"Extracted {len(pages)} pages")
print("\n--- First page preview ---")
print(pages[0]["text"][:500])

metadata = get_document_metadata(pdf_path)
print("\n--- Metadata ---")
print(metadata)