from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from config.settings import settings
from config.logging_config import log
from src.core.embeddings import EmbeddingGenerator
from src.core.indexer import VectorIndexer

class HybridRetriever:
    """Advanced hybrid retrieval system"""
    
    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()
        self.indexer = VectorIndexer()
        self.reranker = None  # Optional reranker
    
    def retrieve(self,
                query: str,
                k: int = 5,
                category: Optional[str] = None,
                method: str = 'hybrid',
                weights: Dict[str, float] = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents
        
        Args:
            query: User query
            k: Number of documents to retrieve
            category: Document category filter
            method: 'dense', 'sparse', or 'hybrid'
            weights: Weights for combining scores
        """
        weights = weights or {'dense': 0.7, 'sparse': 0.3}
        
        results = []
        
        # Determine index name
        index_name = f"category_{category}" if category else "main"
        
        if method in ['dense', 'hybrid']:
            # Dense retrieval using embeddings
            query_embedding = self.embedding_generator.encode_single(query)
            dense_results = self.indexer.search_faiss(index_name, query_embedding, k * 2)
            results.extend(dense_results)
        
        if method in ['sparse', 'hybrid']:
            # Sparse retrieval using BM25
            sparse_results = self.indexer.search_bm25(index_name, query, k * 2)
            results.extend(sparse_results)
        
        if method == 'hybrid':
            # Combine and rerank results
            results = self._combine_results(
                dense_results,
                sparse_results,
                weights
            )
        
        # Deduplicate
        results = self._deduplicate_results(results)
        
        # Apply reranking if available
        if self.reranker:
            results = self._rerank_results(query, results)
        
        # Filter by threshold
        results = [r for r in results if r['score'] >= settings.SIMILARITY_THRESHOLD]
        
        return results[:k]
    
    def _combine_results(self,
                        dense_results: List[Dict],
                        sparse_results: List[Dict],
                        weights: Dict[str, float]) -> List[Dict[str, Any]]:
        """Combine results from different retrieval methods"""
        combined = {}
        
        # Process dense results
        for result in dense_results:
            key = result.get('chunk_id', result.get('text', '')[:50])
            if key not in combined:
                combined[key] = result.copy()
                combined[key]['dense_score'] = result['score']
                combined[key]['sparse_score'] = 0
        
        # Process sparse results
        for result in sparse_results:
            key = result.get('chunk_id', result.get('text', '')[:50])
            if key in combined:
                combined[key]['sparse_score'] = result['score']
            else:
                combined[key] = result.copy()
                combined[key]['dense_score'] = 0
                combined[key]['sparse_score'] = result['score']
        
        # Calculate combined scores
        for key, result in combined.items():
            result['combined_score'] = (
                weights['dense'] * result.get('dense_score', 0) +
                weights['sparse'] * result.get('sparse_score', 0)
            )
            result['score'] = result['combined_score']
        
        # Sort by combined score
        results = sorted(combined.values(), key=lambda x: x['score'], reverse=True)
        
        return results
    
    def _deduplicate_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate results"""
        seen = set()
        unique = []
        
        for result in results:
            # Create a key for deduplication
            key = result.get('chunk_id', result.get('text', '')[:100])
            
            if key not in seen:
                seen.add(key)
                unique.append(result)
        
        return unique
    
    def _rerank_results(self, query: str, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rerank results using a cross-encoder"""
        # This would use a cross-encoder model for reranking
        # For now, returning as-is
        return results
    
    def retrieve_with_context(self,
                             query: str,
                             context: Dict[str, Any],
                             k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve with user context"""
        # Extract relevant context
        user_state = context.get('state', '')
        user_category = context.get('category', '')
        user_language = context.get('language', 'en')
        
        # Modify query based on context
        enriched_query = f"{query} {user_state}"
        
        # Retrieve with category filter
        results = self.retrieve(
            enriched_query,
            k=k,
            category=user_category
        )
        
        # Add context relevance scoring
        for result in results:
            result['context_relevance'] = self._calculate_context_relevance(
                result, context
            )
        
        # Re-sort by context relevance
        results.sort(key=lambda x: x['context_relevance'], reverse=True)
        
        return results
    
    def _calculate_context_relevance(self,
                                    result: Dict[str, Any],
                                    context: Dict[str, Any]) -> float:
        """Calculate how relevant a result is to user context"""
        score = 1.0
        
        # Check state relevance
        if 'state' in context:
            if context['state'].lower() in result.get('text', '').lower():
                score *= 1.2
        
        # Check category match
        if 'category' in context:
            if context['category'] == result.get('metadata', {}).get('document_type'):
                score *= 1.3
        
        return score