# src/rag/generator.py
from src.llm.local_llm import LocalLLM

llm = LocalLLM()

def generate_answer(query, retrieved_passages):
    combined_context = "\n\n".join([p["text"] for p in retrieved_passages])

    prompt = f"""
You are NyayaAI, a legal assistant for Indian citizens.

You must ALWAYS return your answer in strict JSON with the following keys:
- "short_answer": brief direct answer (2-4 sentences)
- "steps": step-by-step actions as a list of strings
- "sources": list of filenames used

NEVER add extra text. ONLY output valid JSON.

Context:
{combined_context}

User question:
{query}

Return JSON now:
"""

    response = llm.generate(prompt, max_tokens=500)

    # Try converting to Python dict
    import json
    try:
        return json.loads(response)
    except:
        # If model adds extra text, try to extract JSON
        import re
        match = re.search(r"\{[\s\S]*\}", response)
        if match:
            return json.loads(match.group(0))

        # fallback minimal skeleton
        return {
            "short_answer": response.strip(),
            "steps": ["Step information not available"],
            "sources": list({p["source"] for p in retrieved_passages})
        }
