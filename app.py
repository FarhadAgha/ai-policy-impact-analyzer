"""
app.py

Streamlit UI for the AI Policy Impact Analyzer.
Handles ONLY presentation — all real logic lives in src/.
"""

import streamlit as st
import tempfile
import os

from src.pdf_processor import extract_text_by_page, get_document_metadata
from src.chunker import chunk_pages
from src.embeddings import embed_chunks
from src.retriever import build_vector_store
from src.analyzer import answer_question
from src.citations import format_evidence_list

st.set_page_config(page_title="AI Policy Impact Analyzer", layout="wide")

st.title("AI Policy Impact Analyzer")
st.caption(
    "This tool provides AI-assisted analysis for research and educational "
    "purposes. It does not provide legal advice or determine whether a "
    "policy is legally compliant, effective, or desirable. Users should "
    "verify important claims against the original policy document."
)

# --- Session state setup ---
if "collection" not in st.session_state:
    st.session_state.collection = None
if "doc_metadata" not in st.session_state:
    st.session_state.doc_metadata = None
if "num_chunks" not in st.session_state:
    st.session_state.num_chunks = None

# --- Upload & indexing ---
st.header("1. Upload a Policy Document")
uploaded_file = st.file_uploader("Upload a PDF policy document", type="pdf")

if uploaded_file is not None and st.session_state.collection is None:
    with st.spinner("Processing document — extracting text, chunking, and building the search index..."):
        # Save uploaded file to a temp path so pymupdf can open it
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        pages = extract_text_by_page(tmp_path)
        metadata = get_document_metadata(tmp_path)
        chunks = chunk_pages(pages)
        embedded_chunks = embed_chunks(chunks)
        collection = build_vector_store(embedded_chunks, collection_name="current_doc")

        st.session_state.collection = collection
        st.session_state.doc_metadata = metadata
        st.session_state.num_chunks = len(chunks)

        os.unlink(tmp_path)  # clean up temp file

    st.success(
        f"Document processed: {metadata.get('page_count')} pages, "
        f"{st.session_state.num_chunks} chunks indexed."
    )

if st.session_state.collection is not None:
    st.divider()
    st.header("2. Ask About This Policy")

    question = st.text_input(
        "Ask a question about the uploaded policy",
        placeholder="e.g. What does this policy require from AI developers?"
    )

    if question:
        with st.spinner("Retrieving evidence and generating answer..."):
            result = answer_question(question, st.session_state.collection)

        st.subheader("Answer")
        st.markdown(result["answer"])

        st.subheader("Evidence")
        citations = format_evidence_list(result["evidence"])
        for c in citations:
            with st.expander(f"{c['citation']} (relevance: {c['confidence']})"):
                st.write(c["excerpt"])