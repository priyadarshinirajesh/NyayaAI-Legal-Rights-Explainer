# NyayaAI-Legal-Rights-Explainer

## 💡 Overview
NyayaAI is an AI-powered legal assistant that simplifies complex laws, rights, and government policies into plain-language, voice-based explanations — helping marginalized citizens understand and claim their rights.

## 🎯 Problem
Millions of citizens in rural and low-literacy communities struggle to understand their legal rights or navigate government schemes due to:
- Complex legal language
- Lack of awareness
- Poor internet access
- Limited literacy

## 🌍 Our Solution
NyayaAI answers legal queries in **simple words** and **regional languages**, through both text and voice.

Users can ask:
> “My husband beats me, what should I do?”  
> “How to apply for widow pension?”  
> “My employer didn’t pay salary.”

and receive step-by-step help in their local language.

## ⚙️ Features
✅ Simplifies legal jargon using NLP  
✅ Supports regional dialects (Tamil/English)  
✅ Voice input/output for low-literacy users  
✅ Works offline with cached results  
✅ Can extend to SMS-based 2G phones

## 🧠 Tech Stack
| Component | Technology |
|------------|-------------|
| NLP | IndicBERT / mT5 |
| Retrieval | FAISS + Sentence Transformers |
| Text-to-Speech | gTTS / pyttsx3 |
| Frontend | Streamlit |
| Language Translation | IndicTrans2 |
| Database | CSV / SQLite |

## 🚀 How to Run
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/embed_index.py
streamlit run src/app_streamlit.py
