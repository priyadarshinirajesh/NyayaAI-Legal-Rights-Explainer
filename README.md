📘 NyayaAI – Legal Rights Assistant (RAG + Voice + Multilingual)

NyayaAI is an intelligent legal rights explainer designed for India.
Users can ask questions through text or voice, in any Indian language, and get clear legal guidance extracted from real government documents.

This project uses:

RAG (Retrieval Augmented Generation)

FAISS Vector Index

GGUF local LLM (CPU-friendly)

Whisper Medium (speech-to-text)

Googletrans for text translation (AI4Bharat optional)

Streamlit Chat UI with mic button

🚀 Features
✔ Ask legal questions using Text or Voice
✔ Supports all Indian languages (Hindi, Tamil, Telugu, Bengali, Marathi, Malayalam…)
✔ Local inference (NO API, NO GPU needed)
✔ Whisper Medium for accurate multilingual transcription
✔ RAG using FAISS for reliable legal answers
✔ GGUF model (3B/8B) for CPU-friendly generation
✔ Clean ChatGPT-style UI
✔ Works offline once setup is done
📂 Project Directory Structure
NyayaAI-Legal-Rights-Explainer/
│
├── app.py                          # Main Streamlit UI
├── README.md                       # Documentation
│
├── data/
│   ├── raw_docs/                   # Place all PDFs, text documents here
│   ├── extracted/                  # Auto-generated
│   ├── chunks/                     # Auto-generated
│   ├── embeddings/                 # Auto-generated
│   ├── faiss_index.faiss           # Auto-generated
│
├── models/
│   ├── llm/
│   │   └── llama_3b.gguf           # Your GGUF model
│
├── src/
│   ├── utils/
│   │   └── audio_tools.py          # Whisper audio recorder + STT
│   │
│   ├── nyayaai_core.py             # Translation + RAG orchestration
│   ├── ingestion/
│   ├── embeddings/
│   ├── rag/
│
└── venv / .venv                    # Python virtual environment

🛠️ 1. System Requirements
Minimum

Windows 10 / macOS / Linux

RAM: 8 GB

CPU: Any modern processor

Recommended

RAM: 16 GB

CPU: i5/i7/Ryzen

No GPU required.

🐍 2. Create Virtual Environment

Open Terminal / PowerShell inside project folder:

python -m venv .venv


Activate it:

Windows
.venv\Scripts\activate

macOS/Linux
source .venv/bin/activate

📦 3. Install Dependencies

Run:

pip install -r requirements.txt


If you don’t have a requirements.txt, install manually:

pip install streamlit
pip install googletrans==4.0.0-rc1
pip install faiss-cpu
pip install sentence-transformers
pip install pypdf
pip install streamlit-audiorecorder
pip install openai-whisper
pip install ffmpeg-python
pip install numba

🎧 4. Install FFmpeg (Required for audio)

Whisper requires FFmpeg, otherwise audio recording & transcription WILL FAIL.

Download:

https://www.gyan.dev/ffmpeg/builds/

Steps:

Download ffmpeg-gpl-essentials.zip

Extract it

Copy the bin/ folder path

Add to Windows PATH

Search Edit system environment variables

Add the path to Path

Check installation:

ffmpeg -version


If you see version info → ✔ Installed.

🧠 5. Download LLM (GGUF)

Use a small, fast CPU model:

Recommended:

Llama 3.1 - 3B Instruct (Q4_K_M).gguf

Download:
https://huggingface.co/MaziyarPanahi/Meta-Llama-3.1-3B-Instruct-GGUF

Place it here:

models/llm/llama.gguf

🗃️ 6. Prepare Legal Documents

Put all PDFs, text documents, Bare Acts inside:

data/raw_docs/


Examples:

Domestic Violence Act

Dowry Prohibition Act

Widow Pension Schemes

Maintenance rights

Police procedures

⚙️ 7. Backend Pipeline (Auto Runs Inside app.py)

The following steps run automatically when Streamlit starts:

✔ Extract Text from PDFs
✔ Chunk Documents
✔ Generate Embeddings
✔ Build FAISS Index

This ensures correct RAG working.

🎙️ 8. Configure Speech-to-Text

NyayaAI uses:

✔ Whisper Medium

Best accuracy for Indian languages on CPU.

Audio is handled through:

src/utils/audio_tools.py


This file:
✔ Records audio
✔ Saves WAV
✔ Transcribes with Whisper Medium
✔ Returns clean text

📝 9. Running the App

Activate venv:

.venv\Scripts\activate


Run Streamlit:

streamlit run app.py


Open in browser:

http://localhost:8501

💬 10. How to Use NyayaAI
1️⃣ Ask using Text

Type a question:

What are my rights as a tenant?

2️⃣ Ask using Voice

Tap 🎤
Speak in ANY language (Hindi/Tamil/Telugu/Marathi/Bengali etc.)

Whisper Medium → converts speech → text
NyayaAI → answers

🔍 11. How RAG Works
User Query → Translate → Retrieve (FAISS) → Create Prompt → LLM → Translate Back → Answer

🌐 12. Supported Languages
Voice (Whisper Medium):

✔ Hindi
✔ English

Text:


🛠️ 13. Troubleshooting
❌ “No module named X”

Activate venv:

.venv\Scripts\activate

❌ FFmpeg not found

Ensure:

ffmpeg -version


returns version info.

❌ Whisper too slow

Switch model:

whisper.load_model("small")

❌ RAG not retrieving context

Ensure documents are inside:

data/raw_docs/

🚀 14. Deployment Options
✔ Streamlit Cloud

Fastest.

✔ Render

(Need Always On instance)

✔ Local app with EXE

Using PyInstaller (optional)

❤️ 15. Credits

Meta Llama 3.1

OpenAI Whisper

FAISS

Streamlit

Googletrans