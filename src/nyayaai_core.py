# nyayaai_core.py

from googletrans import Translator
from src.rag.retriever import retrieve
from src.rag.generator import generate_answer

translator = Translator()

def detect_language(text):
    try:
        return translator.detect(text).lang
    except:
        return "en"

def translate(text, target="en"):
    try:
        return translator.translate(text, dest=target).text
    except:
        return text

def rag_answer(user_question: str):

    # 1️⃣ Detect original language
    lang = detect_language(user_question)

    # 2️⃣ Translate to English if needed
    query_en = translate(user_question, "en") if lang != "en" else user_question

    # 3️⃣ Retrieve top passages
    passages = retrieve(query_en, top_k=4)

    # 4️⃣ Generate answer in English
    answer = generate_answer(query_en, passages)

    # 5️⃣ Translate answer back to user’s language
    if lang != "en":
        answer["short_answer"] = translate(answer["short_answer"], lang)
        answer["steps"] = [translate(step, lang) for step in answer["steps"]]

    return answer
