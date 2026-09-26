"""
analyzer.py

Orchestrates the retrieve-then-generate loop: takes a question,
retrieves relevant evidence chunks, sends them to the LLM with
strict grounding rules, and returns a structured, cited answer.
"""

import os
from groq import Groq
from dotenv import load_dotenv

from src.retriever import retrieve_relevant_chunks
from src.prompts import SYSTEM_PROMPT, build_qa_prompt

load_dotenv()

_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found. Make sure it's set in your .env file."
            )
        _client = Groq(api_key=api_key)
    return _client


def answer_question(
    question: str,
    collection,
    top_k: int = 5,
    model: str = "openai/gpt-oss-120b",
) -> dict:
    """
    Answer a question about the policy document using RAG.
    """
    retrieved_chunks = retrieve_relevant_chunks(question, collection, top_k=top_k)

    client = _get_client()
    prompt = build_qa_prompt(question, retrieved_chunks)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    answer_text = response.choices[0].message.content

    return {
        "question": question,
        "answer": answer_text,
        "evidence": retrieved_chunks,
    }