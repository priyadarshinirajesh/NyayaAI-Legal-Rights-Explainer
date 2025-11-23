# src/ingestion/chunker.py
import sqlite3
import re
from pathlib import Path

RAW_TEXT_DIR = Path("data/raw_text")
DB_PATH = Path("data/legal.db")


def create_tables(conn):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        chunk_text TEXT
    );
    """)


def chunk_text(text, size=6):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [" ".join(sentences[i:i+size]).strip()
            for i in range(0, len(sentences), size)]


def ingest_all():
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    conn.execute("DELETE FROM chunks;")
    conn.commit()
    print("Old chunks cleared.")

    for txt in RAW_TEXT_DIR.glob("*.txt"):
        content = txt.read_text(encoding="utf-8")
        chunks = chunk_text(content)

        for c in chunks:
            conn.execute(
                "INSERT INTO chunks (source, chunk_text) VALUES (?, ?)",
                (txt.name, c)
            )

    conn.commit()
    conn.close()
    print("Ingested chunks.")
