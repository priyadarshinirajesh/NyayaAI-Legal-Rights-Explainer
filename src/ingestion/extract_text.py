# src/ingestion/extract_text.py
import fitz
from pathlib import Path

RAW_DIR = Path("data/raw_docs")
OUT_DIR = Path("data/raw_text")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_text_from_pdf(pdf_path: Path) -> str:
    doc = fitz.open(pdf_path)
    pages = []
    for p in doc:
        pages.append(p.get_text())
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
            # copy simple text files
            out = OUT_DIR / f.name
            out.write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
            print("Copied text:", out)

if __name__ == "__main__":
    process_all()
