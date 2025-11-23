# src/rag/generator.py
import re
from src.llm.local_llm import LocalLLM

llm = LocalLLM()


def clean_answer(text):
    lines = text.splitlines()
    seen = set()
    out = []
    for line in lines:
        s = line.strip()
        if s and s not in seen:
            out.append(line)
            seen.add(s)
    return "\n".join(out).strip()


def generate_answer(query, context):
    prompt = f"""
You are **NyayaAI**, India’s legal helper. Provide accurate, simple and clear legal guidance.

### RULES:
- Only use information from the context.
- DO NOT repeat the context.
- DO NOT invent facts.
- Keep the answer clean and structured.

### FORMAT TO FOLLOW:
1. **Direct Answer** (3–5 sentences)
2. **Steps to follow** (bullet points)
3. **Laws or Sources referenced**

### Context:
{context}

### User Question:
{query}

### Now give the final answer:
""".strip()

    print("\n==================== LLM PROMPT SENT ====================")
    print(prompt)
    print("==========================================================\n")

    raw = llm.generate(prompt, max_tokens=500)
    print("=============== RAW LLM OUTPUT ===============")
    print(raw)
    print("=============== END RAW OUTPUT ===============\n")

    return clean_answer(raw)
