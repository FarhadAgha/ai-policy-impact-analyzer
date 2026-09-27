AI Policy Impact Analyzer

A RAG-based tool that analyzes AI policy PDFs and produces a structured, evidence-based impact analysis — every claim cited to a specific page in the source document.

Live Demo:- https://ai-policy-impact-analyzer-fsnhbmqek87kujekjieb2b.streamlit.app/ 

What it does

Upload an AI policy/regulation PDF and get:

An automated dashboard: Overview, Key Requirements, Stakeholder Impact, Policy Dimensions, Benefits, Concerns, Trade-offs, Implementation Challenges
A Q&A feature to ask specific questions about the document
Page-level citations and expandable evidence on every claim
Neutral, hedged language — the tool never judges a policy as "good" or "bad"

Built to demonstrate responsible LLM use on a governance problem: grounding answers in retrieved text, separating fact from inference, and saying "not found" instead of guessing.

Architecture
PDF → page-tagged text extraction → chunking (overlapping, page-tracked)
→ embeddings (sentence-transformers) → ChromaDB vector store
→ semantic retrieval (top-k) → LLM (Groq, evidence-only prompting) → cited answer

The dashboard and Q&A share this same pipeline — the dashboard just runs a fixed set of questions automatically on upload.

Tech stack

Python · Streamlit · PyMuPDF · sentence-transformers · ChromaDB · Groq API (openai/gpt-oss-120b)

Example

Q: What does this policy say about transparency requirements? The regulation requires providers to enable detection and disclosure of AI-generated content, particularly when published for public interest, unless human editorial review has been applied (Pages 120-122). It maintains a list of AI systems subject to additional transparency measures under Article 50 (Pages 412-413).

(Tested against the EU AI Act, 459 pages.)

Limitations
No guarantee against LLM hallucination, despite evidence-only prompting
No OCR — scanned/image-only PDFs won't extract
Runs on Groq's free-tier API — subject to daily token limits
Hosted on Streamlit Community Cloud's free tier — cold starts after inactivity
Not legal advice; does not assess legal compliance or effectiveness
Future improvements

Formal retrieval evaluation (Precision@K/Recall@K) · policy comparison (two documents side by side) · OCR support · FastAPI + React frontend on the same Python RAG core

Project structure
      ai-policy-impact-analyzer/
          ├── app.py
          ├── src/
          │   ├── pdf_processor.py      # PDF → page-tagged text
          │   ├── chunker.py            # text → overlapping chunks
          │   ├── embeddings.py         # chunks → vectors
          │   ├── retriever.py          # vector store + semantic search
          │   ├── analyzer.py           # RAG orchestration + LLM calls
          │   ├── citations.py          # evidence formatting
          │   ├── prompts.py            # LLM prompt templates
          │   └── dashboard_sections.py # dashboard question definitions
          ├── tests/
          └── data/sample_policies/

Ethical note

The system prompt forbids declaring a policy "good" or "bad," requires hedged language for impacts, and requires the model to say when it can't find supporting evidence rather than guess. Intended to support human research, not replace it — verify important claims against the original document.

Author

Syed Farhad — Final-year BS Computer Science, University of Balochistan (AI & Data Science) 
LinkedIn:- https://www.linkedin.com/in/syed-farhad-computer-science/
