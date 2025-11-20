# src/embeddings/embed.py
import sqlite3
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer

DB_PATH = Path("data/legal.db")
OUT_DIR = Path("data/embeddings")
OUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "all-MiniLM-L6-v2"  # small & works offline once downloaded

def load_chunks():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    rows = cur.execute("SELECT id, chunk_text FROM chunks ORDER BY id").fetchall()
    conn.close()
    ids = [r[0] for r in rows]
    texts = [r[1] for r in rows]
    return ids, texts

def compute_and_save():
    ids, texts = load_chunks()
    if not texts:
        print("No chunks found. Run chunker first.")
        return
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    np.save(OUT_DIR / "chunk_embeddings.npy", embeddings)
    np.save(OUT_DIR / "chunk_ids.npy", ids)
    print("Saved embeddings and ids to", OUT_DIR)

if __name__ == "__main__":
    compute_and_save()
