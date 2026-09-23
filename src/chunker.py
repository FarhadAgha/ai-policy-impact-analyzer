"""
chunker.py

Splits page-tagged text into overlapping chunks suitable for
embedding and retrieval. Each chunk keeps track of which page(s)
it came from, so citations stay accurate downstream.
"""


def chunk_pages(pages: list[dict], chunk_size: int = 400, overlap: int = 50) -> list[dict]:
    """
    Turn page-tagged text into overlapping word-based chunks.

    Args:
        pages: output of pdf_processor.extract_text_by_page()
        chunk_size: target number of words per chunk
        overlap: number of words repeated between consecutive chunks

    Returns:
        A list of dicts like:
        [
            {
                "chunk_id": 0,
                "text": "...",
                "page_start": 1,
                "page_end": 2,
                "word_count": 400
            },
            ...
        ]
    """
    # Step 1: flatten all pages into one list of (word, page_number) pairs
    # so we can slide a window across the whole document while still
    # knowing which page every word came from.
    word_page_pairs = []
    for page in pages:
        words = page["text"].split()
        for word in words:
            word_page_pairs.append((word, page["page_number"]))

    chunks = []
    chunk_id = 0
    start = 0

    while start < len(word_page_pairs):
        end = min(start + chunk_size, len(word_page_pairs))
        window = word_page_pairs[start:end]

        if not window:
            break

        chunk_words = [w for w, _ in window]
        chunk_pages_covered = [p for _, p in window]

        chunks.append({
            "chunk_id": chunk_id,
            "text": " ".join(chunk_words),
            "page_start": chunk_pages_covered[0],
            "page_end": chunk_pages_covered[-1],
            "word_count": len(chunk_words)
        })

        chunk_id += 1
        # move the window forward, leaving `overlap` words behind
        start += (chunk_size - overlap)

    return chunks