# src/rag/safe_context.py
def safe_combine_passages(passages, max_chars=3000):
    out = []
    total = 0

    for p in passages:
        t = p["text"].strip()
        if not t:
            continue

        if len(t) > max_chars:
            t = t[:max_chars - 500] + "\n...[truncated]..."

        if total + len(t) > max_chars:
            remaining = max_chars - total
            if remaining > 200:
                out.append(t[:remaining] + "\n...[truncated]...")
            break

        out.append(t)
        total += len(t)

    # Format neatly for readability
    return "\n\n---\n\n".join(out)
