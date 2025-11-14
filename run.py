#!/usr/bin/env python3
"""
Main entry point for NyayaAI
"""

import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="NyayaAI - Legal Rights Assistant")
    parser.add_argument(
        "--mode",
        choices=["web", "api", "cli", "setup", "index"],
        default="web",
        help="Mode to run the application"
    )
    parser.add_argument("--port", type=int, default=8000, help="Port for web/API server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host for web/API server")
    
    args = parser.parse_args()
    
    if args.mode == "setup":
        from scripts.setup_project import main as setup_main
        setup_main()
    
    elif args.mode == "index":
        from scripts.build_indexes import main as index_main
        index_main()
    
    elif args.mode == "web":
        import streamlit.web.cli as stcli
        sys.argv = ["streamlit", "run", "src/interfaces/streamlit_app.py",
                   "--server.port", str(args.port),
                   "--server.address", args.host]
        sys.exit(stcli.main())
    
    elif args.mode == "api":
        import uvicorn
        from src.interfaces.api_server import app
        uvicorn.run(app, host=args.host, port=args.port)
    
    elif args.mode == "cli":
        print("CLI mode - Interactive legal assistant")
        from src.core.retriever import HybridRetriever
        from src.nlp.query_processor import QueryProcessor
        from src.generation.response_generator import ResponseGenerator
        
        retriever = HybridRetriever()
        processor = QueryProcessor()
        generator = ResponseGenerator()
        
        while True:
            query = input("\nYour question (or 'exit'): ")
            if query.lower() == 'exit':
                break
            
            # Process query
            query_info = processor.process_query(query)
            docs = retriever.retrieve(query_info['expanded_query'])
            response = generator.generate_response(query_info, docs)
            
            print("\n" + "=" * 50)
            print("Answer:", response['answer'])
            print("\nSteps:")
            for i, step in enumerate(response['practical_steps'], 1):
                print(f"{i}. {step}")
            print("=" * 50)

if __name__ == "__main__":
    main()