import hashlib
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import PyPDF2
import pdfplumber
import re
from datetime import datetime
from config.logging_config import log
from config.settings import settings

class DocumentProcessor:
    """Advanced document processor for legal documents"""
    
    def __init__(self):
        self.processed_dir = settings.PROCESSED_DIR
        self.metadata_dir = self.processed_dir / "metadata"
        self.text_dir = self.processed_dir / "extracted_text"
        self.chunks_dir = self.processed_dir / "chunks"
        
        # Create subdirectories
        for dir_path in [self.metadata_dir, self.text_dir, self.chunks_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Legal document patterns
        self.section_patterns = {
            'eligibility': r'(?i)(eligib|qualify|who can|entitled)',
            'documents': r'(?i)(documents?|papers?|proof|certificate)',
            'procedure': r'(?i)(procedure|process|how to|steps|apply)',
            'benefits': r'(?i)(benefit|amount|payment|compensation)',
            'timeline': r'(?i)(timeline|deadline|within|days|months)',
            'contact': r'(?i)(contact|office|address|phone|email)',
            'penalties': r'(?i)(penalty|fine|punishment|violation)',
            'rights': r'(?i)(rights?|entitle|claim|privilege)'
        }
    
    def process_pdf(self, pdf_path: Path) -> Dict[str, Any]:
        """Process a PDF file and extract structured information"""
        log.info(f"Processing PDF: {pdf_path}")
        
        # Generate document ID
        doc_id = self._generate_doc_id(pdf_path)
        
        # Extract text
        text = self._extract_text_from_pdf(pdf_path)
        
        # Extract metadata
        metadata = self._extract_metadata(pdf_path, text)
        
        # Extract sections
        sections = self._extract_sections(text)
        
        # Create chunks
        chunks = self._create_intelligent_chunks(text, sections)
        
        # Save processed data
        self._save_processed_data(doc_id, text, metadata, chunks)
        
        return {
            'doc_id': doc_id,
            'metadata': metadata,
            'sections': sections,
            'chunks': chunks,
            'status': 'success'
        }
    
    def _extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text from PDF using multiple methods"""
        text = ""
        
        try:
            # Try pdfplumber first (better for tables)
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            log.warning(f"pdfplumber failed, trying PyPDF2: {e}")
            
            # Fallback to PyPDF2
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e:
                log.error(f"Failed to extract text from {pdf_path}: {e}")
                return ""
        
        # Clean text
        text = self._clean_text(text)
        return text
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common OCR errors
        replacements = {
            '|': 'I',
            '0': 'O',  # Context-dependent
            '5': 'S',  # Context-dependent
        }
        
        # Remove page numbers and headers
        text = re.sub(r'Page \d+', '', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Fix sentence boundaries
        text = re.sub(r'([a-z])\.([A-Z])', r'\1. \2', text)
        
        return text.strip()
    
    def _extract_metadata(self, pdf_path: Path, text: str) -> Dict[str, Any]:
        """Extract metadata from document"""
        metadata = {
            'filename': pdf_path.name,
            'file_size': pdf_path.stat().st_size,
            'processed_date': datetime.now().isoformat(),
            'document_type': self._classify_document(pdf_path.name, text),
            'language': self._detect_language(text),
            'page_count': self._get_page_count(pdf_path),
            'acts_mentioned': self._extract_acts(text),
            'sections_mentioned': self._extract_legal_sections(text),
            'dates_mentioned': self._extract_dates(text)
        }
        return metadata
    
    def _classify_document(self, filename: str, text: str) -> str:
        """Classify document type"""
        filename_lower = filename.lower()
        text_lower = text.lower()[:1000]  # Check first 1000 chars
        
        classifications = {
            'pension': ['pension', 'elderly', 'widow', 'old age'],
            'domestic_violence': ['domestic violence', 'protection of women', 'abuse'],
            'land': ['land acquisition', 'compensation', 'property'],
            'labor': ['wages', 'employment', 'worker', 'labor'],
            'legal_aid': ['legal services', 'legal aid', 'free legal']
        }
        
        for category, keywords in classifications.items():
            if any(kw in filename_lower or kw in text_lower for kw in keywords):
                return category
        
        return 'general'
    
    def _extract_sections(self, text: str) -> Dict[str, List[str]]:
        """Extract relevant sections from text"""
        sections = {}
        
        for section_type, pattern in self.section_patterns.items():
            matches = []
            for match in re.finditer(pattern, text):
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 500)
                context = text[start:end]
                matches.append(context)
            
            if matches:
                sections[section_type] = matches
        
        return sections
    
    def _create_intelligent_chunks(self, text: str, sections: Dict) -> List[Dict[str, Any]]:
        """Create semantically meaningful chunks"""
        chunks = []
        chunk_id = 0
        
        # First, chunk the sections
        for section_type, section_texts in sections.items():
            for section_text in section_texts:
                if len(section_text) <= settings.CHUNK_SIZE:
                    chunks.append({
                        'chunk_id': chunk_id,
                        'text': section_text,
                        'type': section_type,
                        'source': 'section'
                    })
                    chunk_id += 1
                else:
                    # Split large sections
                    sub_chunks = self._split_text_into_chunks(section_text)
                    for sub_chunk in sub_chunks:
                        chunks.append({
                            'chunk_id': chunk_id,
                            'text': sub_chunk,
                            'type': section_type,
                            'source': 'section_split'
                        })
                        chunk_id += 1
        
        # Then, chunk the remaining text
        sentences = self._split_into_sentences(text)
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= settings.CHUNK_SIZE:
                current_chunk += " " + sentence
            else:
                if current_chunk:
                    chunks.append({
                        'chunk_id': chunk_id,
                        'text': current_chunk.strip(),
                        'type': 'general',
                        'source': 'document'
                    })
                    chunk_id += 1
                current_chunk = sentence
        
        # Add last chunk
        if current_chunk:
            chunks.append({
                'chunk_id': chunk_id,
                'text': current_chunk.strip(),
                'type': 'general',
                'source': 'document'
            })
        
        return chunks
    
    def _split_text_into_chunks(self, text: str, chunk_size: int = None) -> List[str]:
        """Split text into chunks with overlap"""
        chunk_size = chunk_size or settings.CHUNK_SIZE
        overlap = settings.CHUNK_OVERLAP
        chunks = []
        
        words = text.split()
        current_pos = 0
        
        while current_pos < len(words):
            chunk_words = words[current_pos:current_pos + chunk_size]
            chunks.append(' '.join(chunk_words))
            current_pos += chunk_size - overlap
        
        return chunks
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitter
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _extract_acts(self, text: str) -> List[str]:
        """Extract mentioned acts from text"""
        act_pattern = r'(?i)([A-Z][A-Za-z\s]+Act,?\s*\d{4})'
        acts = re.findall(act_pattern, text)
        return list(set(acts))
    
    def _extract_legal_sections(self, text: str) -> List[str]:
        """Extract legal sections mentioned"""
        section_pattern = r'(?i)Section\s*(\d+[A-Z]?)'
        sections = re.findall(section_pattern, text)
        return list(set(sections))
    
    def _extract_dates(self, text: str) -> List[str]:
        """Extract dates from text"""
        date_patterns = [
            r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}',
            r'\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{2,4}',
            r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{2,4}'
        ]
        
        dates = []
        for pattern in date_patterns:
            dates.extend(re.findall(pattern, text, re.IGNORECASE))
        
        return list(set(dates))
    
    def _detect_language(self, text: str) -> str:
        """Detect document language"""
        # Simple language detection based on character ranges
        sample = text[:500]
        
        if re.search(r'[\u0900-\u097F]', sample):  # Devanagari
            return 'hi'
        elif re.search(r'[\u0B80-\u0BFF]', sample):  # Tamil
            return 'ta'
        elif re.search(r'[\u0C00-\u0C7F]', sample):  # Telugu
            return 'te'
        
        return 'en'
    
    def _get_page_count(self, pdf_path: Path) -> int:
        """Get page count of PDF"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return len(pdf_reader.pages)
        except:
            return 0
    
    def _generate_doc_id(self, pdf_path: Path) -> str:
        """Generate unique document ID"""
        content = f"{pdf_path.name}_{pdf_path.stat().st_size}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _save_processed_data(self, doc_id: str, text: str, metadata: Dict, chunks: List[Dict]):
        """Save processed data to files"""
        # Save text
        text_file = self.text_dir / f"{doc_id}.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        # Save metadata
        metadata_file = self.metadata_dir / f"{doc_id}.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # Save chunks
        chunks_file = self.chunks_dir / f"{doc_id}.json"
        with open(chunks_file, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
        
        log.info(f"Saved processed data for document {doc_id}")
    
    def process_all_documents(self) -> List[Dict[str, Any]]:
        """Process all PDFs in the raw documents directory"""
        results = []
        pdf_files = list(settings.RAW_DOCS_DIR.glob("*.pdf"))
        
        log.info(f"Found {len(pdf_files)} PDF files to process")
        
        for pdf_file in pdf_files:
            try:
                result = self.process_pdf(pdf_file)
                results.append(result)
            except Exception as e:
                log.error(f"Failed to process {pdf_file}: {e}")
                results.append({
                    'doc_id': None,
                    'filename': pdf_file.name,
                    'status': 'failed',
                    'error': str(e)
                })
        
        return results