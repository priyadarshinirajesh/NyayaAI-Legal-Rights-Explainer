# run_demo.py
import os
import sys
import time
from pathlib import Path
from googletrans import Translator

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
print("Working dir:", ROOT)

# Project imports
from src.ingestion.extract_text import process_all
from src.ingestion.chunker import ingest_all
from src.embeddings.embed import compute_and_save
from src.embeddings.build_faiss import build_index
from src.rag import retriever, generator
from src.rag.safe_context import safe_combine_passages

translator = Translator()


def detect_language(text):
    try:
        return translator.detect(text).lang
    except:
        return "en"


def translate_text(text, dest="en"):
    try:
        return translator.translate(text, dest=dest).text
    except:
        return text


def main():
    RAW = Path("data/raw_docs")
    if not any(RAW.iterdir()):
        print("❗ Put PDFs/Text files inside data/raw_docs/")
        sys.exit(0)

    print("📄 Extracting...")
    process_all()

    print("📦 Chunking...")
    ingest_all()

    print("🧠 Embeddings...")
    compute_and_save()

    print("🔍 Building FAISS...")
    build_index()

    print("\n✔ Ready! Ask any question.\n")

    while True:
        q = input("Your question: ").strip()
        if not q:
            break

        start = time.time()

        lang = detect_language(q)
        print(f"[info] Language: {lang}")
        q_en = translate_text(q, "en") if lang != "en" else q

        # RETRIEVAL
        t0 = time.time()
        passages = retriever.retrieve(q_en, top_k=6)
        t_retrieval = time.time() - t0
        print(f"[timing] Retrieval: {t_retrieval:.2f}s")

        # BUILD CLEAN CONTEXT
        context_str = safe_combine_passages(passages, max_chars=3000)

        # GENERATION
        t1 = time.time()
        answer = generator.generate_answer(q_en, context_str)
        t_generation = time.time() - t1

        # TRANSLATE BACK
        if lang != "en":
            answer = translate_text(answer, lang)

        total = time.time() - start

        print("\n========== NYAYAAI FINAL ANSWER ==========\n")
        print(answer)
        print("\n⏱ Timing:")
        print(f"- Retrieval: {t_retrieval:.2f}s")
        print(f"- Generation: {t_generation:.2f}s")
        print(f"- Total: {total:.2f}s")
        print("\n==========================================\n")


if __name__ == "__main__":
    main()
