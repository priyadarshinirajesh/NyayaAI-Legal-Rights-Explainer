# app.py — NyayaAI Chatbot
import streamlit as st
from pathlib import Path
import time
import sys

ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT))

from src.nyayaai_core import rag_answer, detect_language, translate
from src.rag.retriever import retrieve
from src.rag.generator import generate_answer


# --------------------------------------------------
# Initialize backend once
# --------------------------------------------------
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

init_backend()


# --------------------------------------------------
# Streamlit Chat UI
# --------------------------------------------------
st.set_page_config(page_title="NyayaAI – Legal Assistant", layout="wide")

st.title("⚖️ NyayaAI – Legal Rights Assistant")
st.write("Ask any legal question in any language and get simple, clear guidance.")


# ------------------------------------
# Chat history setup
# ------------------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []   # [{"role": "user"/"assistant", "text": "..."}]


# ------------------------------------
# Show chat history
# ------------------------------------
for msg in st.session_state.chat:
    st.chat_message(msg["role"]).write(msg["text"])


# ------------------------------------
# Chat input — like ChatGPT
# ------------------------------------
query = st.chat_input("Type your legal question...")

if query:
    # Show user's message
    st.chat_message("user").write(query)
    st.session_state.chat.append({"role": "user", "text": query})

    # Process
    with st.spinner("NyayaAI is thinking..."):
        start_total = time.time()

        lang = detect_language(query)
        q_en = translate(query, "en") if lang != "en" else query

        # retrieve
        t0 = time.time()
        passages = retrieve(q_en, top_k=6)
        retrieval_time = time.time() - t0

        # generate answer
        t1 = time.time()
        answer_en = generate_answer(q_en, passages)
        generation_time = time.time() - t1

        # translate back
        answer = translate(answer_en, lang) if lang != "en" else answer_en

        total_time = time.time() - start_total

    # Show NyayaAI answer
    st.chat_message("assistant").write(answer)
    st.session_state.chat.append({"role": "assistant", "text": answer})

    # Backend log
    print("\n======== BACKEND LOG ========")
    print("Question:", q_en)
    print("Answer:", answer_en)
    print("Retrieved:", len(passages))
    print("Retrieval:", retrieval_time)
    print("Generation:", generation_time)
    print("Total:", total_time)
    print("=============================\n")