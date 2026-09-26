"""
prompts.py

Prompt templates for the LLM analysis layer. Kept separate from
analyzer.py so the exact wording of our evidence rules is easy
to review, audit, and tune independently of the orchestration logic.
"""

SYSTEM_PROMPT = """You are an AI policy analysis assistant. You help \
researchers understand AI policy documents by analyzing retrieved \
excerpts from those documents.

STRICT RULES YOU MUST FOLLOW:
1. Only use information from the provided excerpts below. Never use \
outside knowledge about laws, regulations, or policies.
2. Every factual claim you make must be traceable to a specific excerpt. \
Reference the page number(s) given with that excerpt.
3. If the excerpts do not contain enough information to answer the \
question, say exactly: "I could not find sufficient evidence in the \
uploaded document to answer this question." Do not guess or fill gaps \
with general knowledge.
4. Never state whether the policy is "good" or "bad." Describe what it \
says and its possible implications, using hedged language like \
"may," "could," "potential."
5. Clearly distinguish between what the document explicitly states and \
any analytical inference you're drawing from it. Label inferences as \
such.
6. Keep any direct wording you borrow from the excerpts short — \
paraphrase in your own words rather than quoting at length.
"""


def build_qa_prompt(question: str, retrieved_chunks: list[dict]) -> str:
    """
    Build the user-turn prompt for answering a question using
    only the retrieved evidence chunks.
    """
    evidence_block = _format_evidence(retrieved_chunks)

    return f"""Question: {question}

Retrieved excerpts from the policy document:

{evidence_block}

Answer the question using only the excerpts above. For each claim, \
note which page(s) it comes from. If the excerpts don't answer the \
question, say so explicitly rather than guessing."""


def build_section_prompt(section_question: str, retrieved_chunks: list[dict]) -> str:
    """
    Same structure as build_qa_prompt, used for the automated
    dashboard sections (Overview, Requirements, etc.) rather than
    a user-typed question.
    """
    return build_qa_prompt(section_question, retrieved_chunks)


def _format_evidence(chunks: list[dict]) -> str:
    """Format retrieved chunks into a numbered evidence block for the prompt."""
    lines = []
    for i, chunk in enumerate(chunks, start=1):
        page_ref = (
            f"Page {chunk['page_start']}"
            if chunk['page_start'] == chunk['page_end']
            else f"Pages {chunk['page_start']}-{chunk['page_end']}"
        )
        lines.append(f"[Excerpt {i} — {page_ref}]\n{chunk['text']}\n")
    return "\n".join(lines)