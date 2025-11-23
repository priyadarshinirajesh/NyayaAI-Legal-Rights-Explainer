# src/ingestion/extract_text.py
import fitz
import re
from pathlib import Path

RAW_DIR = Path("data/raw_docs")
OUT_DIR = Path("data/raw_text")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def clean_text(text: str) -> str:
    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = re.sub(r"[•●■◆▶▷▪◦]+", "", text)
    text = re.sub(r"Page\s*\d+|\b\d+/\d+\b", "", text)
    text = re.sub(r"©.*?\n", "", text)

    cleaned = []
    for line in text.splitlines():
        line = line.strip()
        if len(line.split()) > 3:
            cleaned.append(line)

    text = "\n".join(cleaned)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def extract_text_from_pdf(pdf_path: Path) -> str:
    doc = fitz.open(pdf_path)
    pages = [clean_text(p.get_text("text")) for p in doc]
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
            cleaned = clean_text(f.read_text(encoding="utf-8"))
            out = OUT_DIR / f.name
            out.write_text(cleaned, encoding="utf-8")
            print("Copied:", out)
