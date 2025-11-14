#!/usr/bin/env python3
"""
Build vector indexes for NyayaAI
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.document_processor import DocumentProcessor
from src.core.embeddings import EmbeddingGenerator
from src.core.indexer import VectorIndexer
from config.logging_config import log
from tqdm import tqdm
import json

def main():
    print("=" * 50)
    print("Building NyayaAI Indexes")
    print("=" * 50)
    
    # Initialize components
    processor = DocumentProcessor()
    embedder = EmbeddingGenerator()
    indexer = VectorIndexer()
    
    # Process documents
    print("\n1. Processing documents...")
    results = processor.process_all_documents()
    
    # Load all chunks
    print("\n2. Loading processed chunks...")
    all_chunks = []
    chunks_dir = Path("data/processed/chunks")
    
    for chunk_file in chunks_dir.glob("*.json"):
        with open(chunk_file, 'r',encoding="utf-8") as f:
            chunks = json.load(f)
            all_chunks.extend(chunks)
    
    print(f"Loaded {len(all_chunks)} chunks")
    
    # Generate embeddings
    print("\n3. Generating embeddings...")
    texts = [chunk['text'] for chunk in all_chunks]
    embeddings = embedder.encode_texts(texts)
    
    # Create indexes
    print("\n4. Building indexes...")
    
    # Main index
    indexer.create_faiss_index("main", embeddings, all_chunks)
    indexer.create_bm25_index("main", all_chunks)
    
    # Category indexes
    indexer.create_category_indexes(all_chunks, embeddings)
    
    print("\n✅ Indexes built successfully!")
    print(f"- Total documents processed: {len(results)}")
    print(f"- Total chunks indexed: {len(all_chunks)}")

if __name__ == "__main__":
    main()