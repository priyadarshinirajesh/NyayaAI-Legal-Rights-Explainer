# app.py — NyayaAI with Speech + Text Chat
import streamlit as st
from pathlib import Path
import time
import sys
import whisper
import os

ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT))

from src.nyayaai_core import rag_answer, detect_language, translate
from src.rag.retriever import retrieve
from src.rag.generator import generate_answer
from src.utils.audio_tools import record_audio


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
st.write("Ask any legal question using voice 🎤 or text 💬.")


# ------------------------------------
# Chat history
# ------------------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []


# ------------------------------------
# Display chat messages
# ------------------------------------
for msg in st.session_state.chat:
    st.chat_message(msg["role"]).write(msg["text"])


# --------------------------------------------------
# INPUT AREA (Mic + Text Input)
# --------------------------------------------------
col1, col2 = st.columns([10, 1])

with col1:
    user_text = st.text_input(
        "text_box",
        placeholder="Type your legal question…",
        label_visibility="collapsed"
    )

with col2:
    st.write("")
    audio_file = record_audio()


# --------------------------------------------------
# HANDLE AUDIO → TEXT (Whisper SMALL)
# --------------------------------------------------
query = None

if audio_file:
    st.toast("🎙️ Processing voice…")
    model = whisper.load_model("small")   # FAST + ACCURATE FOR INDIAN LANGUAGES
    result = model.transcribe(audio_file, fp16=False)
    query = result["text"].strip()

    st.chat_message("user").write("🎤 " + query)
    st.session_state.chat.append({"role": "user", "text": query})

elif user_text.strip():
    query = user_text.strip()
    st.chat_message("user").write(query)
    st.session_state.chat.append({"role": "user", "text": query})


# --------------------------------------------------
# PROCESS QUERY
# --------------------------------------------------
if query:
    with st.spinner("NyayaAI is thinking..."):
        lang = detect_language(query)
        q_en = translate(query, "en") if lang != "en" else query

        passages = retrieve(q_en, top_k=6)
        answer_en = generate_answer(q_en, passages)

        answer = translate(answer_en, lang) if lang != "en" else answer_en

    st.chat_message("assistant").write(answer)
    st.session_state.chat.append({"role": "assistant", "text": answer})

    print("\n=== BACKEND LOG ===")
    print("QUERY:", q_en)
    print("ANSWER:", answer_en)
    print("====================\n")
