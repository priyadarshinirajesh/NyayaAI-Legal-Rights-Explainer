# src/embeddings/build_faiss.py
import numpy as np
import faiss
from pathlib import Path

EMB_PATH = Path("data/embeddings/chunk_embeddings.npy")
OUT_DIR = Path("data/index")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def build_index():
    emb = np.load(EMB_PATH)
    # normalize to use cosine similarity via inner product
    faiss.normalize_L2(emb)
    d = emb.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(emb)
    faiss.write_index(index, str(OUT_DIR / "faiss.index"))
    print("FAISS index saved to", OUT_DIR / "faiss.index")

if __name__ == "__main__":
    build_index()

