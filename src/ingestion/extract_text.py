# src/ingestion/extract_text.py
import fitz
import re
from pathlib import Path

RAW_DIR = Path("data/raw_docs")
OUT_DIR = Path("data/raw_text")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def clean_text(text: str) -> str:
    # Remove URLs
    text = re.sub(r"http\S+|www\.\S+", "", text)

    # Remove bullets / unicode marks
    text = re.sub(r"[•●■◆▶▷▪◦]+", "", text)

    # Remove page numbers
    text = re.sub(r"Page\s*\d+|\b\d+/\d+\b", "", text)

    # Remove copyright/footer lines
    text = re.sub(r"©.*?\n", "", text)

    # Remove extremely short lines
    cleaned = []
    for line in text.splitlines():
        line = line.strip()
        if len(line.split()) > 3:
            cleaned.append(line)
    text = "\n".join(cleaned)

    # Collapse blank lines
    text = re.sub(r"\n{2,}", "\n", text)

    return text.strip()


def extract_text_from_pdf(pdf_path: Path) -> str:
    doc = fitz.open(pdf_path)
    pages = []
    for p in doc:
        raw = p.get_text("text")
        pages.append(clean_text(raw))
    return "\n".join(pages)


def process_all():
    for f in RAW_DIR.glob("*"):

        if f.suffix.lower() == ".pdf":
            try:
                text = extract_text_from_pdf(f)
                out = OUT_DIR / (f.stem + ".txt")
                out.write_text(text, encoding="utf-8")
                print("Extracted:", out)
            except Exception as e:
                print("Error extracting", f, e)

        elif f.suffix.lower() in [".txt", ".md"]:
            content = f.read_text(encoding="utf-8")
            cleaned = clean_text(content)
            out = OUT_DIR / f.name
            out.write_text(cleaned, encoding="utf-8")
            print("Copied:", out)


if __name__ == "__main__":
    process_all()
