🇮🇳 NyayaAI – AI-Powered Legal Rights Explainer for Indian Citizens
✨ Multilingual • Offline • RAG-based • Local LLM • Open-Source

NyayaAI is an AI assistant that helps Indian citizens—especially rural and underprivileged communities—understand their legal rights in simple, easy-to-understand language.

It works on your local system using a local Llama 3.1 model, a FAISS semantic search index, and multilingual translation, making it powerful, private, and flexible.

⭐ Key Features
🔍 Retrieval-Augmented Generation (RAG)

NyayaAI performs:

PDF → Text extraction

Sentence-level chunking

Embedding generation using all-MiniLM-L6-v2

Fast semantic search using FAISS

Context-based LLM answering

🧠 Local LLM (Offline)

Powered by:

Meta-Llama-3.1-8B-Instruct-GGUF

Run through llama.cpp (llama_cpp_python), fully offline and CPU-friendly.

🌍 Multilingual Support

NyayaAI automatically detects and supports questions in:

Hindi

Tamil

Telugu

Malayalam

Kannada

Bengali

Marathi

Gujarati

Punjabi

English

…and any other Googletrans-supported language

Workflow:

Detect language

Translate to English

Run RAG + LLM

Translate response back

📘 Simple, Understandable Responses

Every answer includes:

Direct explanation (3–5 sentences)

Clear steps to follow

Relevant laws/sources

📑 Document-Agnostic

Just drop PDFs or text files into:

data/raw_docs/


NyayaAI processes everything automatically.

📁 Folder Structure
NyayaAI-Legal-Rights-Explainer/
│
├── run_demo.py
│
├── models/
│   └── llm/
│       └── llama.gguf       # Meta-Llama-3.1-8B-Instruct-GGUF (renamed)
│
├── data/
│   ├── raw_docs/            # PDF documents you provide
│   ├── raw_text/            # Extracted text
│   ├── embeddings/          # Embedding vector files
│   ├── index/               # FAISS index
│   └── legal.db             # Chunk database
│
├── src/
│   ├── ingestion/
│   │   ├── extract_text.py
│   │   └── chunker.py
│   │
│   ├── embeddings/
│   │   ├── embed.py
│   │   └── build_faiss.py
│   │
│   ├── rag/
│   │   ├── retriever.py
│   │   └── generator.py
│   │
│   └── llm/
│       └── local_llm.py

🛠️ Installation Guide
1️⃣ Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate       # Windows

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Download the Llama model

Download:

Meta-Llama-3.1-8B-Instruct-GGUF

Rename it to:

llama.gguf


Place it in:

models/llm/

4️⃣ Add your legal PDFs

Place them inside:

data/raw_docs/

▶️ Running NyayaAI

Run this command:

python run_demo.py


NyayaAI will:

✔ Extract PDFs
✔ Chunk text
✔ Compute embeddings
✔ Build FAISS index
✔ Load local LLM
✔ Ask you for questions

You will see:

✔ Ready! Ask any legal question (any language)

🧪 Example Questions (Try These!)
Widow Pension

विधवा पेंशन कैसे मिलेगी?

What is the eligibility for IGNWPS?

Tamil: நான் விதவைத் தொகைக்கு தகுதி உள்ளவரா?

Domestic Violence

What support is available under the Domestic Violence Act?

Property

What documents do I need to buy land?

I want to buy a property. What steps should I take?

Crime / FIR

FIR कैसे दर्ज करें?

Steps to file an FIR?

Children / POCSO

What rights do minors have under the POCSO Act?

🧱 How NyayaAI Works (Architecture)
USER QUESTION (Any language)
        ↓
Language Detection (googletrans)
        ↓
Translate → English
        ↓
RAG Retrieval (FAISS + MiniLM embeddings)
        ↓
Build LLM Prompt (Context + Question)
        ↓
Local LLM (llama.cpp) Generates Answer
        ↓
Clean Output
        ↓
Translate Back → User’s Language
        ↓
FINAL RESPONSE


🌟 Future Enhancements

Add IndicTrans2 for offline translation

Add a FastAPI backend

Add a mobile-friendly UI (Flutter / React Native)

Add speech-to-text + text-to-speech

State-wise legal modules

Offline OCR for scanned PDFs

#👏 Acknowledgments

Meta AI (Llama 3.1)

SentenceTransformers

FAISS

Googletrans

PyMuPDF

Python open-source community