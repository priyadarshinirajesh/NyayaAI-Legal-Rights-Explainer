# 📘 NyayaAI – Legal Rights Assistant (RAG + Voice + Multilingual)

**NyayaAI** is an intelligent legal rights assistant designed specifically for India. It helps users understand their legal rights by answering questions through text or voice input in any Indian language, providing clear guidance based on real legal documents.

## 🎯 Key Features

- **🎤 Voice & Text Input**: Ask questions using voice (Whisper transcription) or text
- **🌐 Multilingual Support**: Works with Hindi, Tamil, Telugu, Bengali, Marathi, Malayalam, and other Indian languages
- **🔍 RAG-based Answers**: Uses Retrieval Augmented Generation with FAISS vector search
- **💻 Local Inference**: Runs on CPU without needing GPUs or API keys
- **📚 Document Processing**: Automatically processes PDFs and text documents
- **💬 Chat Interface**: Clean Streamlit-based conversational UI
- **🚀 Offline Capable**: Works offline after initial setup

## 🏗️ Technical Stack

| Component | Technology |
|-----------|------------|
| **LLM** | Llama (GGUF format) via llama-cpp-python |
| **Speech-to-Text** | OpenAI Whisper (Small model) |
| **Translation** | Google Translate API |
| **Text-to-Speech** | Edge-TTS (Optional) |
| **Vector Database** | FAISS |
| **Embeddings** | Sentence Transformers (all-MiniLM-L6-v2) |
| **PDF Processing** | PyMuPDF (fitz) |
| **Frontend** | Streamlit |
| **Database** | SQLite |

## 📂 Project Structure

```
NyayaAI-Legal-Rights-Explainer/
│
├── app.py                          # Main Streamlit application
├── run_demo.py                     # CLI demo for testing
├── README.md                       # Documentation
├── requirements.txt                # Python dependencies
│
├── data/
│   ├── raw_docs/                   # Place your PDFs and documents here
│   ├── raw_text/                   # Extracted text (auto-generated)
│   ├── embeddings/                 # Vector embeddings (auto-generated)
│   ├── index/                      # FAISS index (auto-generated)
│   └── legal.db                    # SQLite database (auto-generated)
│
├── models/
│   └── llm/
│       └── llama_meta_Q4_K_M.gguf # Your GGUF model file
│
└── src/
    ├── nyayaai_core.py             # Core translation and RAG orchestration
    ├── db/
    │   └── db_schema.py            # Database schema utilities
    ├── embeddings/
    │   ├── embed.py                # Generate embeddings
    │   └── build_faiss.py          # Build FAISS index
    ├── ingestion/
    │   ├── extract_text.py         # PDF/text extraction
    │   ├── chunker.py              # Document chunking
    │   └── clean_text.py           # Text cleaning utilities
    ├── llm/
    │   └── local_llm.py            # Local LLM wrapper
    ├── rag/
    │   ├── retriever.py            # FAISS-based retrieval
    │   ├── generator.py            # Answer generation
    │   └── safe_context.py         # Context management
    └── utils/
        ├── audio_tools.py          # Audio recording utilities
        ├── text_utils.py           # Text processing utilities
        └── tts_tools.py            # Text-to-speech (optional)
```

## 🛠️ Installation Guide

### System Requirements

**Minimum:**
- Windows 10 / macOS / Linux
- RAM: 8 GB
- CPU: Any modern processor
- Storage: 10 GB free space

**Recommended:**
- RAM: 16 GB
- CPU: Intel i5/i7 or AMD Ryzen
- Storage: 20 GB free space

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/NyayaAI-Legal-Rights-Explainer.git
cd NyayaAI-Legal-Rights-Explainer
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
py -3.11 -m venv myenv

# Activate it
# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate
```

### Step 3: Install Dependencies

Install:

```bash
pip install -r requirements.txt
```

### Step 4: Install FFmpeg (Required for Audio)

**Windows:**
1. Download from: https://www.gyan.dev/ffmpeg/builds/
2. Extract `ffmpeg-gpl-essentials.zip`
3. Add the `bin` folder to your PATH
4. Verify: `ffmpeg -version`

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

### Step 5: Download GGUF Model

Download a Llama GGUF model (recommended: 3B or 8B quantized):

**Option 1: Llama 3.1 3B (Recommended for most users)**
```bash
# Download from Hugging Face
wget https://huggingface.co/MaziyarPanahi/Meta-Llama-3.1-3B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-3B-Instruct.Q4_K_M.gguf

# Move to correct location
mkdir -p models/llm
mv Meta-Llama-3.1-3B-Instruct.Q4_K_M.gguf models/llm/llama_meta_Q4_K_M.gguf
```

**Option 2: Manual Download**
1. Visit: https://huggingface.co/models?search=gguf
2. Download any Q4_K_M or Q5_K_M quantized model
3. Place in `models/llm/` folder
4. Rename to `llama_meta_Q4_K_M.gguf`

### Step 6: Prepare Legal Documents

Add your legal documents to `data/raw_docs/`:

```bash
# Create directory if it doesn't exist
mkdir -p data/raw_docs

# Add your documents (PDFs, TXT files)
cp /path/to/your/documents/*.pdf data/raw_docs/
```

Example documents to include:
- Indian Penal Code
- Domestic Violence Act
- Consumer Protection Act
- Labour Laws
- RTI Act
- Fundamental Rights
- Any legal PDFs or text files

## 🚀 Running the Application

### Option 1: Streamlit Web Interface (Recommended)

```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Run Streamlit app
streamlit run app.py
```

Open browser at: http://localhost:8501

### Option 2: Command Line Demo

```bash
python run_demo.py
```

## 💡 Usage Guide

### Using the Web Interface

1. **Text Input**: Type your question in the text box
2. **Voice Input**: Click the 🎤 microphone button and speak
3. **Language**: Ask in any Indian language - it will auto-detect
4. **Response**: Get structured legal guidance with relevant laws cited

### Example Questions

**English:**
- "What are my rights if my employer doesn't pay salary?"
- "How can I file an RTI application?"
- "What is the procedure for divorce in India?"

**Hindi (हिंदी):**
- "घरेलू हिंसा के खिलाफ मेरे क्या अधिकार हैं?"
- "किरायेदार के रूप में मेरे क्या अधिकार हैं?"

## 🔧 How It Works

### Pipeline Architecture

```
User Query (Any Language)
    ↓
Language Detection (Googletrans)
    ↓
Translation to English
    ↓
Embedding Generation (Sentence Transformers)
    ↓
FAISS Vector Search (Top K passages)
    ↓
Context Building (SQLite + Chunked Documents)
    ↓
LLM Generation (Llama GGUF)
    ↓
Translation Back to User Language
    ↓
Structured Response
```

### Backend Processing Flow

1. **Document Ingestion** (`src/ingestion/`)
   - Extract text from PDFs using PyMuPDF
   - Clean and normalize text
   - Chunk into 6-sentence segments
   - Store in SQLite database

2. **Embedding Generation** (`src/embeddings/`)
   - Generate embeddings using all-MiniLM-L6-v2
   - Build FAISS index for similarity search
   - Store embeddings as numpy arrays

3. **RAG Pipeline** (`src/rag/`)
   - Retrieve relevant chunks using FAISS
   - Build context from top passages
   - Generate answer using local LLM
   - Format and clean response

4. **Translation** (`src/nyayaai_core.py`)
   - Detect input language
   - Translate query to English
   - Process in English
   - Translate response back

## 🐛 Troubleshooting

### Common Issues and Solutions

| Problem | Solution |
|---------|----------|
| **"No module named X"** | Activate venv: `.venv\Scripts\activate` |
| **FFmpeg not found** | Ensure `ffmpeg -version` works in terminal |
| **Whisper too slow** | Use `"tiny"` or `"base"` model instead of `"small"` |
| **Out of memory** | Use smaller GGUF model (Q3_K_M instead of Q4_K_M) |
| **No chunks found** | Ensure documents exist in `data/raw_docs/` |
| **LLM not generating** | Check model path in `src/llm/local_llm.py` |
| **Translation failing** | Check internet connection (Google Translate needs it) |

### Performance Optimization

**For Faster Processing:**
```python
# In src/llm/local_llm.py
n_threads=8,  # Increase based on CPU cores
n_batch=64,   # Increase for faster batch processing

# In app.py
model = whisper.load_model("tiny")  # Use smaller model
```

**For Better Quality:**
```python
# In src/rag/retriever.py
top_k=8  # Retrieve more passages

# In src/rag/generator.py
max_tokens=600  # Longer responses
```

## 🌐 Language Support

### Fully Supported Languages
- English (en)
- Hindi (हिंदी - hi)

### Voice Input Support
Whisper supports 100+ languages including all major Indian languages.

## 📊 Database Schema

The SQLite database (`data/legal.db`) contains:

```sql
CREATE TABLE chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,        -- Source filename
    chunk_text TEXT     -- Chunked text content
);
```

## 🚢 Deployment Options

### Local Deployment
- Run directly with Python
- Package as executable using PyInstaller

### Cloud Deployment

**Streamlit Cloud (Easiest):**
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy (Note: Large models may hit limits)

**Docker:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

**Other Platforms:**
- Render.com (needs paid plan for persistent storage)
- Railway.app
- Google Cloud Run
- AWS EC2

## 🔒 Privacy & Security

- **100% Local Processing**: No data sent to external servers (except translations)
- **No API Keys Required**: Uses local models
- **Data Privacy**: Your documents stay on your machine
- **Offline Mode**: Works without internet (except translations)

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

### Areas for Contribution
- Add more language support
- Improve PDF extraction
- Optimize chunking strategy
- Add more legal documents
- Enhance UI/UX
- Add unit tests


- **v1.0.0** - Initial release with basic RAG pipeline
- **v1.1.0** - Added voice input support
- **v1.2.0** - Multilingual support added
- **v1.3.0** - Improved chunking and retrieval

---

**Built with ❤️ for accessible legal information in India**