"""
analyzer.py

Orchestrates the retrieve-then-generate loop: takes a question,
retrieves relevant evidence chunks, sends them to the LLM with
strict grounding rules, and returns a structured, cited answer.
"""
from groq import RateLimitError
import os
from groq import Groq
from dotenv import load_dotenv

from src.retriever import retrieve_relevant_chunks
from src.prompts import SYSTEM_PROMPT, build_qa_prompt

load_dotenv()

_client = None


def _get_api_key():
    """
    Reads the API key from Streamlit secrets (used on Streamlit Cloud)
    if available, otherwise falls back to a local .env file.
    """
    try:
        import streamlit as st
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return os.getenv("GROQ_API_KEY")


def _get_client():
    global _client
    if _client is None:
        api_key = _get_api_key()
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found. Set it in your .env file locally, "
                "or in Streamlit Cloud's Secrets settings when deployed."
            )
        _client = Groq(api_key=api_key)
    return _client


def answer_question(
    question: str,
    collection,
    top_k: int = 3,
    model: str = "openai/gpt-oss-20b",
) -> dict:
    """
    Answer a question about the policy document using RAG.

    Args:
        question: the question to answer
        collection: a Chroma collection from retriever.build_vector_store()
        top_k: how many chunks to retrieve as evidence
        model: which Groq model to use

    Returns:
        {
            "question": "...",
            "answer": "...",
            "evidence": [ {text, page_start, page_end, similarity_score}, ... ]
        }
    """
    retrieved_chunks = retrieve_relevant_chunks(question, collection, top_k=top_k)

    client = _get_client()
    prompt = build_qa_prompt(question, retrieved_chunks)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        answer_text = response.choices[0].message.content
    except RateLimitError:
        answer_text = (
            "⚠️ The analysis service has hit its daily usage limit. "
            "Please try again later, or contact the developer to increase capacity."
        )

    return {
        "question": question,
        "answer": answer_text,
        "evidence": retrieved_chunks,
    }