import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    RAW_DOCS_DIR = DATA_DIR / "raw_documents"
    PROCESSED_DIR = DATA_DIR / "processed"
    KB_DIR = DATA_DIR / "knowledge_base"
    INDEX_DIR = DATA_DIR / "indexes"
    MODEL_DIR = BASE_DIR / "models"
    LOG_DIR = BASE_DIR / "logs"
    
    # Create directories
    for dir_path in [RAW_DOCS_DIR, PROCESSED_DIR, KB_DIR, INDEX_DIR, MODEL_DIR, LOG_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # Model Configuration
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    INTENT_MODEL = "distilbert-base-uncased"
    TRANSLATION_MODEL = "Helsinki-NLP/opus-mt-en-hi"
    
    # Processing Configuration
    CHUNK_SIZE = 512
    CHUNK_OVERLAP = 64
    MAX_CHUNKS_PER_DOC = 100
    
    # Retrieval Configuration
    TOP_K_RETRIEVAL = 5
    SIMILARITY_THRESHOLD = 0.6
    USE_RERANKING = True
    
    # Language Configuration
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'hi': 'Hindi',
        'ta': 'Tamil',
        'te': 'Telugu',
        'bn': 'Bengali',
        'kn': 'Kannada',
        'ml': 'Malayalam'
    }
    DEFAULT_LANGUAGE = 'en'
    
    # API Configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    API_KEY = os.getenv("API_KEY", "your-api-key")
    
    # SMS Configuration
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
    
    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR}/nyayaai.db")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}"

settings = Settings()