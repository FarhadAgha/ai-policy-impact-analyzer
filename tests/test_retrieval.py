import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pdf_processor import extract_text_by_page
from src.chunker import chunk_pages

pdf_path = "data/sample_policies/TA-9-2024-0138_EN.pdf"

pages = extract_text_by_page(pdf_path)
chunks = chunk_pages(pages)

print(f"Created {len(chunks)} chunks from {len(pages)} pages")
print("\n--- First chunk ---")
print(f"Pages {chunks[0]['page_start']}-{chunks[0]['page_end']}, {chunks[0]['word_count']} words")
print(chunks[0]["text"][:300])

print("\n--- A middle chunk ---")
mid = len(chunks) // 2
print(f"Pages {chunks[mid]['page_start']}-{chunks[mid]['page_end']}, {chunks[mid]['word_count']} words")
print(chunks[mid]["text"][:300])

from src.embeddings import embed_chunks

print("\n--- Embedding chunks (this may take a minute on first run, downloading the model) ---")
embedded_chunks = embed_chunks(chunks[:5])  # just first 5 for a quick test

print(f"Embedded {len(embedded_chunks)} chunks")
print(f"Embedding vector length: {len(embedded_chunks[0]['embedding'])}")
print(f"First 5 values of first chunk's embedding: {embedded_chunks[0]['embedding'][:5]}")