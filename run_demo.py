# demo/run_demo.py
"""
End-to-end demo that runs the pipeline and accepts a query from the user.
This demo is intentionally light: instead of a heavy LLM it uses a template-based
generator so you can run it offline immediately.

Steps performed:
1. Create demo data (if data/raw_docs is empty)
2. Extract text -> data/raw_text
3. Chunk into SQLite (data/legal.db)
4. Compute embeddings -> data/embeddings
5. Build FAISS index -> data/index
6. Prompt user for a query -> run retrieve -> generate answer -> print
"""
import os
from pathlib import Path
import sys
print("Working dir:", Path.cwd())

# helper imports (local)
from src.ingestion import extract_text, chunker
from src.embeddings import embed, build_faiss
from src.rag import retriever, generator
from pathlib import Path

DATA_RAW = Path("data/raw_docs")
DATA_RAW.mkdir(parents=True, exist_ok=True)
DATA_RAW_TEXT = Path("data/raw_text")
DATA_RAW_TEXT.mkdir(parents=True, exist_ok=True)
# 1. If data/raw_docs is empty, create small sample text files
if not any(DATA_RAW.iterdir()):
    print("❗ No documents found in data/raw_docs/")
    print("Please place your legal PDFs or text files inside data/raw_docs/ and run again.")
    sys.exit(0)

# 2. Extract text (if PDFs present) or copy text files
print("Running text extraction/copy...")
from src.ingestion.extract_text import process_all
process_all()

# 3. Chunk into SQLite
print("Running chunker...")
from src.ingestion.chunker import ingest_all
ingest_all()

# 4. Compute embeddings
print("Computing embeddings...")
from src.embeddings.embed import compute_and_save
compute_and_save()

# 5. Build FAISS index
print("Building FAISS index...")
from src.embeddings.build_faiss import build_index
build_index()

# 6. Accept a query and run retrieve + generate
print("\nReady. Type a question like: 'How do I apply for widow pension?'\n")
query = input("Your question: ").strip()
if not query:
    print("No query given. Exiting.")
    sys.exit(0)

results = retriever.retrieve(query, top_k=4)
print("\nTop retrieved passages (source — score):")
for r in results:
    print(f" - {r['source']} (score: {r['score']:.3f})")
    print("   ", r['text'][:200].replace("\n"," ") + "...\n")

answer = generator.generate_answer(query, results)
print("\n--- NyayaAI (demo) answer ---")
print(answer)
print("\nWhat to do next:")
for i, s in enumerate(answer["steps"], start=1):
    print(f"{i}. {s}")
print("\nSources:")
for s in answer["sources"]:
    print("- ", s)

