import numpy as np
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import torch
from config.settings import settings
from config.logging_config import log

class EmbeddingGenerator:
    """Generate embeddings for text using various models"""
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        log.info(f"Loading embedding model {self.model_name} on {self.device}")
        self.model = SentenceTransformer(self.model_name)
        self.model.to(self.device)
        
        # Get embedding dimension
        self.dimension = self.model.get_sentence_embedding_dimension()
        log.info(f"Embedding dimension: {self.dimension}")
    
    def encode_texts(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """Encode multiple texts to embeddings"""
        if not texts:
            return np.array([])
        
        log.info(f"Encoding {len(texts)} texts")
        
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True  # For cosine similarity
        )
        
        return embeddings
    
    def encode_single(self, text: str) -> np.ndarray:
        """Encode a single text"""
        return self.encode_texts([text])[0]
    
    def encode_with_metadata(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Encode documents with metadata preservation"""
        texts = [doc.get('text', doc.get('content', '')) for doc in documents]
        embeddings = self.encode_texts(texts)
        
        return {
            'embeddings': embeddings,
            'metadata': [doc.get('metadata', {}) for doc in documents],
            'texts': texts,
            'dimension': self.dimension
        }