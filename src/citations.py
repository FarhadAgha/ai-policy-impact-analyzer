"""
citations.py

Formats evidence chunks into consistent, display-ready citation
strings/objects used throughout the UI, so every part of the app
presents evidence the same way.
"""


def format_citation(chunk: dict) -> str:
    """
    Turn a single evidence chunk into a short citation label,
    e.g. "Page 12" or "Pages 205-207".
    """
    if chunk["page_start"] == chunk["page_end"]:
        return f"Page {chunk['page_start']}"
    return f"Pages {chunk['page_start']}-{chunk['page_end']}"


def format_evidence_list(evidence: list[dict]) -> list[dict]:
    """
    Take the raw evidence list from analyzer.answer_question() and
    return display-ready entries: citation label, excerpt preview,
    and confidence score.

    Returns:
        [
            {
                "citation": "Pages 412-413",
                "excerpt": "for amendments extending...",
                "confidence": 0.548
            },
            ...
        ]
    """
    formatted = []
    for chunk in evidence:
        formatted.append({
            "citation": format_citation(chunk),
            "excerpt": chunk["text"][:300] + ("..." if len(chunk["text"]) > 300 else ""),
            "confidence": chunk["similarity_score"],
        })
    return formatted


def no_evidence_message() -> str:
    """Standard message when no relevant evidence was found."""
    return "No supporting passage was identified."