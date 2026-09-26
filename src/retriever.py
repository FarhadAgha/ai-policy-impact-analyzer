"""
retriever.py

Stores embedded chunks in a local Chroma vector database and
retrieves the most semantically relevant chunks for a given query.
This is the "R" in RAG — everything the LLM sees later comes
through here, not the raw document.
"""

import chromadb
from src.embeddings import embed_texts


def build_vector_store(chunks: list[dict], collection_name: str = "policy_doc"):
    """
    Store embedded chunks in a fresh in-memory Chroma collection.

    Args:
        chunks: output of embeddings.embed_chunks() — each chunk
                must already have an "embedding" key.
        collection_name: name for this document's collection.

    Returns:
        A Chroma collection object, ready to be queried.
    """
    client = chromadb.Client()
    # Ensure no stale collection from a previous run interferes.
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass

    collection = client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )
    collection.add(
        ids=[str(chunk["chunk_id"]) for chunk in chunks],
        embeddings=[chunk["embedding"] for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[
            {
                "page_start": chunk["page_start"],
                "page_end": chunk["page_end"],
                "chunk_id": chunk["chunk_id"],
            }
            for chunk in chunks
        ],
    )

    return collection


def retrieve_relevant_chunks(query: str, collection, top_k: int = 5) -> list[dict]:
    """
    Find the top_k chunks most semantically similar to the query.

    Args:
        query: the user's question or a system-generated question
               (e.g. "what does this policy say about transparency?")
        collection: a Chroma collection from build_vector_store()
        top_k: how many chunks to retrieve

    Returns:
        A list of dicts like:
        [
            {
                "text": "...",
                "page_start": 12,
                "page_end": 12,
                "chunk_id": 34,
                "similarity_score": 0.82
            },
            ...
        ]
        Ordered from most to least relevant.
    """
    query_embedding = embed_texts([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    retrieved = []
    for i in range(len(results["ids"][0])):
        # Chroma returns "distance" (lower = more similar);
        # convert to an intuitive 0-1 similarity score.
        distance = results["distances"][0][i]
        similarity_score = 1 - distance

        retrieved.append({
            "text": results["documents"][0][i],
            "page_start": results["metadatas"][0][i]["page_start"],
            "page_end": results["metadatas"][0][i]["page_end"],
            "chunk_id": results["metadatas"][0][i]["chunk_id"],
            "similarity_score": round(similarity_score, 3),
        })

    return retrieved