# src/rag/generator.py
import re
from src.llm.local_llm import LocalLLM

llm = LocalLLM()

def clean_answer(text):
    """Remove duplicates & irrelevant extra sections."""
    lines = text.splitlines()
    seen = set()
    out = []
    skip_sections = ("additional information", "final note", "note:", "disclaimer")

    for line in lines:
        l = line.strip().lower()

        # remove unwanted sections
        if any(l.startswith(s) for s in skip_sections):
            continue

        if l and l not in seen:
            out.append(line)
            seen.add(l)

    cleaned = "\n".join(out).strip()

    # HARD FILTER: cut off anything after "###" or markdown headers
    cleaned = cleaned.split("## ")[0]
    cleaned = cleaned.split("### ")[0]

    return cleaned.strip()


def generate_answer(query, context_blocks):
    """Generate short, structured, strict answers."""

    context_str = "\n\n".join([p["text"] for p in context_blocks])
    context_str = re.sub(r"\s+", " ", context_str).strip()

    prompt = f"""
You are **NyayaAI**, India’s legal helper.  
Give clear and simple legal guidance using ONLY the information from the context.

### STRICT RULES:
- **Use only the context.**
- **Do not add anything extra.**
- **Do not give disclaimers.**
- **Do not include additional information.**
- **Do not repeat sentences.**
- **No long paragraphs. Keep it concise.**

### REQUIRED FORMAT (FOLLOW EXACTLY):
**Direct Answer:** (2–4 sentences only)

**Steps to follow:**  
- Step 1  
- Step 2  
- Step 3  
(3–5 steps max)

**Laws or Sources referenced:**  
- Source 1  
- Source 2

### Context:
{context_str}

### User Question:
{query}

### Now give the final answer (ONLY the required sections, nothing else):
""".strip()

    print("\n==================== LLM PROMPT SENT ====================")
    print(prompt)
    print("==========================================================\n")

    raw = llm.generate(prompt, max_tokens=300)

    print("=============== RAW LLM OUTPUT ===============")
    print(raw)
    print("=============== END RAW OUTPUT ===============\n")

    return clean_answer(raw)
