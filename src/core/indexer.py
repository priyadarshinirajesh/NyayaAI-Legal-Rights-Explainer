import faiss
import pickle
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional
from rank_bm25 import BM25Okapi
from config.settings import settings
from config.logging_config import log

class VectorIndexer:
    """Multi-index system for efficient retrieval"""
    
    def __init__(self):
        self.faiss_dir = settings.INDEX_DIR / "faiss"
        self.bm25_dir = settings.INDEX_DIR / "bm25"
        self.faiss_dir.mkdir(parents=True, exist_ok=True)
        self.bm25_dir.mkdir(parents=True, exist_ok=True)
        
        self.indexes = {}
        self.metadata = {}
        self.bm25_indexes = {}
    
    def create_faiss_index(self, 
                          name: str, 
                          embeddings: np.ndarray,
                          documents: List[Dict[str, Any]],
                          use_gpu: bool = False) -> None:
        """Create and save a FAISS index"""
        log.info(f"Creating FAISS index '{name}' with {len(embeddings)} vectors")
        
        dimension = embeddings.shape[1]
        
        # Choose index type based on size
        if len(embeddings) < 10000:
            # Use flat index for small datasets
            index = faiss.IndexFlatIP(dimension)
        else:
            # Use IVF index for larger datasets
            nlist = int(np.sqrt(len(embeddings)))
            index = faiss.IndexIVFFlat(
                faiss.IndexFlatIP(dimension),
                dimension,
                nlist,
                faiss.METRIC_INNER_PRODUCT
            )
            index.train(embeddings)
        
        # Normalize for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Add to index
        index.add(embeddings)
        
        # Move to GPU if available
        if use_gpu and faiss.get_num_gpus() > 0:
            index = faiss.index_cpu_to_gpu(faiss.StandardGpuResources(), 0, index)
        
        # Save index
        index_path = self.faiss_dir / f"{name}.index"
        faiss.write_index(index, str(index_path))
        
        # Save metadata
        metadata_path = self.faiss_dir / f"{name}_metadata.pkl"
        with open(metadata_path, 'wb') as f:
            pickle.dump({
                'documents': documents,
                'dimension': dimension,
                'size': len(embeddings)
            }, f)
        
        log.info(f"Saved FAISS index to {index_path}")
    
    def create_bm25_index(self, name: str, documents: List[Dict[str, Any]]) -> None:
        """Create and save a BM25 index"""
        log.info(f"Creating BM25 index '{name}' with {len(documents)} documents")
        
        # Extract texts
        texts = [doc.get('text', doc.get('content', '')) for doc in documents]
        
        # Tokenize
        tokenized_texts = [text.lower().split() for text in texts]
        
        # Create BM25 index
        bm25 = BM25Okapi(tokenized_texts)
        
        # Save index
        index_path = self.bm25_dir / f"{name}.pkl"
        with open(index_path, 'wb') as f:
            pickle.dump({
                'bm25': bm25,
                'documents': documents,
                'tokenized': tokenized_texts
            }, f)
        
        log.info(f"Saved BM25 index to {index_path}")
    
    def load_faiss_index(self, name: str) -> Optional[Dict[str, Any]]:
        """Load a FAISS index"""
        index_path = self.faiss_dir / f"{name}.index"
        metadata_path = self.faiss_dir / f"{name}_metadata.pkl"
        
        if not index_path.exists() or not metadata_path.exists():
            log.warning(f"Index '{name}' not found")
            return None
        
        # Load index
        index = faiss.read_index(str(index_path))
        
        # Load metadata
        with open(metadata_path, 'rb') as f:
            metadata = pickle.load(f)
        
        return {
            'index': index,
            'metadata': metadata
        }
    
    def load_bm25_index(self, name: str) -> Optional[Dict[str, Any]]:
        """Load a BM25 index"""
        index_path = self.bm25_dir / f"{name}.pkl"
        
        if not index_path.exists():
            log.warning(f"BM25 index '{name}' not found")
            return None
        
        with open(index_path, 'rb') as f:
            return pickle.load(f)
    
    def search_faiss(self, 
                     index_name: str,
                     query_embedding: np.ndarray,
                     k: int = 5) -> List[Dict[str, Any]]:
        """Search in a FAISS index"""
        index_data = self.load_faiss_index(index_name)
        if not index_data:
            return []
        
        index = index_data['index']
        documents = index_data['metadata']['documents']
        
        # Normalize query
        query_embedding = query_embedding.reshape(1, -1)
        faiss.normalize_L2(query_embedding)
        
        # Search
        distances, indices = index.search(query_embedding, k)
        
        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if idx >= 0:  # Valid result
                result = documents[idx].copy()
                result['score'] = float(dist)
                result['rank'] = i + 1
                results.append(result)
        
        return results
    
    def search_bm25(self,
                   index_name: str,
                   query: str,
                   k: int = 5) -> List[Dict[str, Any]]:
        """Search in a BM25 index"""
        index_data = self.load_bm25_index(index_name)
        if not index_data:
            return []
        
        bm25 = index_data['bm25']
        documents = index_data['documents']
        
        # Tokenize query
        query_tokens = query.lower().split()
        
        # Get scores
        scores = bm25.get_scores(query_tokens)
        
        # Get top k
        top_indices = np.argsort(scores)[::-1][:k]
        
        results = []
        for i, idx in enumerate(top_indices):
            result = documents[idx].copy()
            result['score'] = float(scores[idx])
            result['rank'] = i + 1
            results.append(result)
        
        return results
    
    def create_category_indexes(self, documents: List[Dict[str, Any]], embeddings: np.ndarray):
        """Create separate indexes for different categories"""
        categories = {}
        
        # Group documents by category
        for i, doc in enumerate(documents):
            category = doc.get('metadata', {}).get('document_type', 'general')
            if category not in categories:
                categories[category] = {'docs': [], 'embeddings': []}
            
            categories[category]['docs'].append(doc)
            categories[category]['embeddings'].append(embeddings[i])
        
        # Create index for each category
        for category, data in categories.items():
            if data['docs']:
                category_embeddings = np.array(data['embeddings'])
                
                # Create FAISS index
                self.create_faiss_index(
                    f"category_{category}",
                    category_embeddings,
                    data['docs']
                )
                
                # Create BM25 index
                self.create_bm25_index(
                    f"category_{category}",
                    data['docs']
                )
                
                log.info(f"Created indexes for category '{category}' with {len(data['docs'])} documents")