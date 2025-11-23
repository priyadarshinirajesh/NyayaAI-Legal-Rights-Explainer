#app.py

import streamlit as st
from pathlib import Path
import time
import sys

ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT))

from src.nyayaai_core import rag_answer, detect_language, translate
from src.rag.retriever import retrieve
from src.rag.generator import generate_answer

# ------------------------------------
# 🧠 CACHE THE BACKEND INITIALIZATION
# ------------------------------------
@st.cache_resource
def init_backend():
    print("=== NyayaAI BACKEND STARTED ===")

    from src.ingestion.extract_text import process_all
    from src.ingestion.chunker import ingest_all
    from src.embeddings.embed import compute_and_save
    from src.embeddings.build_faiss import build_index

    RAW = Path("data/raw_docs")
    if not any(RAW.iterdir()):
        print("❗ No raw docs found.")
        return

    print("Extracting...")
    process_all()

    print("Chunking...")
    ingest_all()

    print("Embedding...")
    compute_and_save()

    print("Building index...")
    build_index()

    print("=== BACKEND READY ===")


# initialize backend ONCE
init_backend()

# ------------------------------------
# Streamlit UI
# ------------------------------------
st.set_page_config(page_title="NyayaAI", layout="wide")

st.title("⚖️ NyayaAI – Legal Rights Assistant")
st.write("Ask any legal question in any language and get simple, clear guidance.")

query = st.text_input("📝 Your Question")

if st.button("Ask NyayaAI"):
    if not query.strip():
        st.warning("Please type a question.")
        st.stop()

    with st.spinner("NyayaAI is thinking..."):

        # detect and translate
        lang = detect_language(query)
        q_en = translate(query, "en") if lang != "en" else query

        # retrieve
        start = time.time()
        passages = retrieve(q_en, top_k=6)
        retrieval_time = time.time() - start

        # debug print in terminal
        print("[DEBUG] Retrieved passages:", len(passages))

        # answer
        start = time.time()
        answer = generate_answer(q_en, passages)
        gen_time = time.time() - start

        # translate back
        if lang != "en":
            answer = translate(answer, lang)

    # ---------------------
    # SHOW ANSWER ONLY
    # ---------------------
    st.subheader("📜 NyayaAI Answer")
    st.markdown(answer)

    # ---------------------
    # BACKEND LOGGING ONLY
    # ---------------------
    print("\n===== BACKEND SUMMARY =====")
    print("Query:", q_en)
    print("Answer:", answer)
    print("\nPassages:")
    for p in passages:
        print("-", p["source"])
    print("\nTiming:")
    print(f"Retrieval: {retrieval_time:.2f}s")
    print(f"Generation: {gen_time:.2f}s")
    print("===========================\n")
