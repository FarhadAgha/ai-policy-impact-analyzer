"""
embeddings.py

Converts text chunks into vector embeddings using a local
sentence-transformer model. These embeddings are what make
semantic (meaning-based) search possible in retriever.py.
"""

from sentence_transformers import SentenceTransformer

# Loaded once and reused — loading the model is the slow part,
# so we don't want to reload it for every chunk.
_model = None


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Turn a list of text strings into a list of embedding vectors.

    Args:
        texts: list of strings (e.g. chunk["text"] values)

    Returns:
        A list of vectors (each a list of floats), same length
        and order as the input texts.
    """
    model = _get_model()
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings.tolist()


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    Take chunker.py's chunk dicts and attach an "embedding" field
    to each one, ready for storage in the vector database.

    Args:
        chunks: output of chunker.chunk_pages()

    Returns:
        The same list of chunk dicts, each with an added
        "embedding" key.
    """
    texts = [chunk["text"] for chunk in chunks]
    vectors = embed_texts(texts)

    for chunk, vector in zip(chunks, vectors):
        chunk["embedding"] = vector

    return chunks