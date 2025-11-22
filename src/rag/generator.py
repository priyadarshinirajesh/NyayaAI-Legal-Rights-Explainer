# src/rag/generator.py
import re
from src.llm.local_llm import LocalLLM
from src.rag.safe_context import safe_combine_passages

llm = LocalLLM()


def clean_llm_output(text):
    """Remove duplicate lines."""
    lines = text.splitlines()
    seen = set()
    final = []

    for line in lines:
        l = line.strip()
        if l not in seen:
            seen.add(l)
            final.append(line)

    cleaned = "\n".join(final).strip()

    # remove repeated question blocks
    cleaned = re.sub(r"(### User Question:.*?)(### User Question)", r"\1", cleaned, flags=re.S)

    return cleaned.strip()


def generate_answer(query, retrieved_passages):
    # -------- FIX: TRUNCATE CONTEXT SAFELY --------
    combined_context = safe_combine_passages(retrieved_passages)

    # -------- Professional Prompt --------
    prompt = f"""
You are **NyayaAI**, India’s legal helper. Provide accurate, simple and clear legal guidance.

### RULES:
- Only use information from the context.
- Do NOT repeat the context.
- Do NOT invent facts.
- Keep the answer clean and structured.

### FORMAT TO FOLLOW:
1. **Direct Answer** (3–5 sentences)
2. **Steps to follow** (bullet points)
3. **Laws or Sources referenced**

### Context:
{combined_context}

### User Question:
{query}

### Now give the final answer:
""".strip()

    print("\n\n==================== LLM PROMPT SENT ====================")
    print(prompt)
    print("================== END OF LLM PROMPT ====================\n\n")

    raw_output = llm.generate(prompt, max_tokens=500)

    print("=============== RAW LLM OUTPUT ===============")
    print(raw_output)
    print("=============== END RAW OUTPUT ===============\n")

    return clean_llm_output(raw_output)
