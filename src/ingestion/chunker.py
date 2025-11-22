# src/ingestion/chunker.py
import sqlite3
from pathlib import Path
import re

RAW_TEXT_DIR = Path("data/raw_text")
DB_PATH = Path("data/legal.db")
CHUNK_SENTENCES = 6


def create_tables(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        state TEXT,
        language TEXT,
        topic TEXT,
        chunk_text TEXT
    );
    """)
    conn.commit()


def chunk_text(text, sentences_per_chunk=CHUNK_SENTENCES):
    # Basic sentence split
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    chunks = []
    for i in range(0, len(sentences), sentences_per_chunk):
        chunk = " ".join(sentences[i:i + sentences_per_chunk]).strip()
        if chunk:
            chunks.append(chunk)
    return chunks


def ingest_all(default_state="UNKNOWN", default_lang="en", default_topic="general"):
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    cur = conn.cursor()

    # ------------------ FIX: clear old chunks ------------------
    cur.execute("DELETE FROM chunks;")
    conn.commit()
    print("Old chunks cleared.")

    # ------------------ Insert new chunks ------------------
    for txt in RAW_TEXT_DIR.glob("*.txt"):
        src = txt.name
        text = txt.read_text(encoding="utf-8")
        chunks = chunk_text(text)

        for c in chunks:
            cur.execute(
                "INSERT INTO chunks (source, state, language, topic, chunk_text) VALUES (?,?,?,?,?)",
                (src, default_state, default_lang, default_topic, c)
            )

    conn.commit()
    conn.close()
    print("Ingested chunks into", DB_PATH)
