# src/rag/retriever.py
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import sqlite3
from pathlib import Path

DB_PATH = Path("data/legal.db")
EMB_DIR = Path("data/embeddings")
INDEX_PATH = Path("data/index/faiss.index")

MODEL_NAME = "all-MiniLM-L6-v2"

# load embedding model once
_model = SentenceTransformer(MODEL_NAME)
_index = None
_chunk_ids = None

def _load_index():
    global _index, _chunk_ids
    if _index is None:
        _index = faiss.read_index(str(INDEX_PATH))
        _chunk_ids = np.load(EMB_DIR / "chunk_ids.npy")
    return _index, _chunk_ids

def retrieve(query, top_k=4):
    idx, chunk_ids = _load_index()
    q_emb = _model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(q_emb)
    D, I = idx.search(q_emb, top_k)
    ids = [int(chunk_ids[i]) for i in I[0]]
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    results = []
    for cid, score in zip(ids, D[0]):
        row = cur.execute("SELECT id, source, chunk_text FROM chunks WHERE id=?", (cid,)).fetchone()
        if row:
            results.append({"id": row[0], "source": row[1], "text": row[2], "score": float(score)})
    conn.close()
    return results

