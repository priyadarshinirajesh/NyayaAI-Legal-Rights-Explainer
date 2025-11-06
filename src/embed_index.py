import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import pickle
import os

MODEL = "paraphrase-multilingual-mpnet-base-v2"

def build_index():
    os.makedirs("models", exist_ok=True)
    df = pd.read_csv("data/legal_kb.csv")
    model = SentenceTransformer(MODEL)
    embeddings = model.encode(df["plain_text_en"].tolist(), convert_to_numpy=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings).astype("float32"))
    faiss.write_index(index, "models/legal_index.faiss")
    with open("models/legal_meta.pkl", "wb") as f:
        pickle.dump(df.to_dict(orient="list"), f)
    print("✅ FAISS index built successfully!")

if __name__ == "__main__":
    build_index()
