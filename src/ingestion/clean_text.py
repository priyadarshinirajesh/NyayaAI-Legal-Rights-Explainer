# src/ingestion/clean_text.py

import re

def clean_extracted_text(text: str) -> str:
    """Clean noisy extracted text before chunking."""

    # Remove multiple blank lines
    text = re.sub(r"\n\s*\n+", "\n", text)

    # Remove page numbers like "Page 2", "2 / 45", "—2—"
    text = re.sub(r"Page\s*\d+", "", text, flags=re.I)
    text = re.sub(r"\b\d+\s*/\s*\d+\b", "", text)
    text = re.sub(r"—\s*\d+\s*—", "", text)

    # Remove table-of-contents dotted patterns
    text = re.sub(r"\.{5,}", "", text)

    # Remove long copyright / footer statements
    text = re.sub(r"©.*?\n", "", text)

    # Remove repeated blank spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Fix broken hyphenated words across lines
    text = re.sub(r"-\n", "", text)

    # Fix random line breaks inside paragraphs
    text = re.sub(r"\n(?=[a-z])", " ", text)

    # Remove leftover weird unicode bullets
    text = text.replace("", "•").replace("", "•")

    # Final trim
    text = text.strip()

    return text
