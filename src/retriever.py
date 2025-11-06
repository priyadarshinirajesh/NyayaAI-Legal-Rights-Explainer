import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

class Retriever:
    def __init__(self):
        self.model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
        self.index = faiss.read_index("models/legal_index.faiss")
        with open("models/legal_meta.pkl", "rb") as f:
            self.meta = pickle.load(f)

    def retrieve(self, query, k=3):
        q_emb = self.model.encode([query])
        D, I = self.index.search(np.array(q_emb).astype('float32'), k)
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx >= 0:
                item = {k: self.meta[k][idx] for k in self.meta}
                results.append(item)
        return results
