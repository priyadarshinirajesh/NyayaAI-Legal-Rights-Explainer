# NyayaAI — Offline RAG Demo (Laptop-only)

This is a minimal offline RAG demo you can run on your laptop.
It uses SentenceTransformers + FAISS for retrieval and a small template-based generator so you can test the full pipeline without heavy LLMs.

Image you uploaded (screenshot): /mnt/data/7bdfb2f0-1552-4d9f-96c8-b716d26892eb.png

## Quick start

1. Create virtualenv and install:
'''
python -m venv .venv
source .venv/bin/activate 
pip install -r requirements.txt
'''

2. Prepare data:
- Put PDFs or .txt in `data/raw_docs/`
- Or run demo script to auto-generate sample docs.

3. Run demo:
'''
python demo/run_demo.py
'''

4. Answer questions:
- The demo will prompt for a question; type something like:
  `How do I apply for widow pension?`

## What the demo does
- Text extraction (from .txt / PDFs)
- Chunking into bite-sized chunks (stored in SQLite)
- Embeddings (SentenceTransformers)
- FAISS vector index
- Retrieval + simple answer generator that uses retrieved chunks and produces a short plain-language answer with citations

## Notes
- This demo is intentionally dependency-light so you can run offline on a typical laptop.
- Later you can swap the generator with a local LLaMA GGUF model (instructions in README).