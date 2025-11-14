#!/usr/bin/env python3
"""
Setup script for NyayaAI project
"""

import os
import sys
from pathlib import Path
import subprocess
import json
import requests
from tqdm import tqdm

def setup_directories():
    """Create necessary directories"""
    print("Setting up project directories...")
    
    directories = [
        "data/raw_documents",
        "data/processed/chunks",
        "data/processed/metadata",
        "data/processed/extracted_text",
        "data/knowledge_base",
        "data/indexes/faiss",
        "data/indexes/bm25",
        "models",
        "logs"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created {dir_path}")

def install_requirements():
    """Install Python requirements"""
    print("\nInstalling Python packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✓ Packages installed")

def download_models():
    """Download required models"""
    print("\nDownloading models...")
    
    # Download spaCy model
    print("Downloading spaCy English model...")
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    
    print("✓ Models downloaded")

def create_sample_data():
    """Create sample knowledge base"""
    print("\nCreating sample knowledge base...")
    
    # Sample FAQs
    faqs = [
        {
            "id": 1,
            "question": "How to apply for widow pension?",
            "answer": "Visit Tehsildar office with husband's death certificate, Aadhaar card, and bank passbook. Fill form and submit.",
            "category": "pension",
            "tags": ["widow", "pension", "application"]
        },
        {
            "id": 2,
            "question": "What to do if facing domestic violence?",
            "answer": "Call Women Helpline 181 immediately. File complaint at police station. Get protection order from court.",
            "category": "domestic_violence",
            "tags": ["violence", "women", "help"]
        },
        {
            "id": 3,
            "question": "How much compensation for land acquisition?",
            "answer": "Market value plus 100% solatium. Additional benefits for rehabilitation. Can object within 60 days.",
            "category": "land",
            "tags": ["land", "compensation", "acquisition"]
        }
    ]
    
    # Save FAQs
    faq_path = Path("data/knowledge_base/faqs.json")
    with open(faq_path, 'w') as f:
        json.dump(faqs, f, indent=2)
    print(f"✓ Created {faq_path}")
    
    # Sample helplines
    helplines = {
        "emergency": {
            "police": "100",
            "women": "181",
            "child": "1098",
            "ambulance": "108"
        },
        "legal": {
            "legal_aid": "15100",
            "consumer": "14404",
            "rtd": "155300"
        }
    }
    
    helpline_path = Path("data/knowledge_base/helplines.json")
    with open(helpline_path, 'w') as f:
        json.dump(helplines, f, indent=2)
    print(f"✓ Created {helpline_path}")

def create_env_file():
    """Create .env file template"""
    print("\nCreating .env file...")
    
    env_content = """
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_KEY=your-api-key-here

# SMS Configuration (Optional)
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=+911234567890

# Database
DATABASE_URL=sqlite:///data/nyayaai.db
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=INFO
"""
    
    env_path = Path(".env")
    if not env_path.exists():
        with open(env_path, 'w') as f:
            f.write(env_content.strip())
        print("✓ Created .env file")
    else:
        print("✓ .env file already exists")

def main():
    """Main setup function"""
    print("=" * 50)
    print("NyayaAI Project Setup")
    print("=" * 50)
    
    # Run setup steps
    setup_directories()
    install_requirements()
    download_models()
    create_sample_data()
    create_env_file()
    
    print("\n" + "=" * 50)
    print("✅ Setup Complete!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Add PDF documents to data/raw_documents/")
    print("2. Run: python scripts/build_indexes.py")
    print("3. Run: python run.py")

if __name__ == "__main__":
    main()