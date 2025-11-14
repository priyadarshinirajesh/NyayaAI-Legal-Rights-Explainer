import re
from typing import Dict, List

class TextSimplifier:
    """Simplify legal text to common language"""
    
    def __init__(self):
        self.legal_terms = self._load_legal_dictionary()
        self.simplification_rules = self._load_simplification_rules()
    
    def _load_legal_dictionary(self) -> Dict[str, str]:
        """Dictionary of legal terms to simple language"""
        return {
            # Legal terms
            'plaintiff': 'person who files case',
            'defendant': 'person against whom case is filed',
            'affidavit': 'written statement under oath',
            'jurisdiction': 'authority of court',
            'suo moto': 'on its own',
            'prima facie': 'at first look',
            'bona fide': 'genuine/real',
            'ex parte': 'one-sided',
            'injunction': 'court order to stop',
            'cognizance': 'taking notice',
            
            # Common legal phrases
            'pursuant to': 'according to',
            'notwithstanding': 'despite',
            'aforementioned': 'mentioned above',
            'hereinafter': 'from now on',
            'thereof': 'of it',
            'therein': 'in it',
            'whereas': 'since',
            
            # Administrative terms
            'competent authority': 'authorized officer',
            'prescribed': 'specified',
            'deemed': 'considered',
            'vested': 'given',
            'constituted': 'formed',
            'promulgated': 'announced',
            
            # Document terms
            'attestation': 'verification',
            'notarized': 'officially certified',
            'requisite': 'required',
            'incumbent': 'necessary',
            
            # Process terms
            'adjudication': 'judgment',
            'arbitration': 'settlement by third party',
            'litigation': 'court case',
            'remand': 'send back',
            'acquittal': 'declared not guilty'
        }
    
    def _load_simplification_rules(self) -> List[tuple]:
        """Rules for simplifying sentences"""
        return [
            # Remove legal jargon connectors
            (r'\s+vis-a-vis\s+', ' regarding '),
            (r'\s+inter alia\s+', ' among other things '),
            (r'\s+ipso facto\s+', ' by that fact itself '),
            (r'\s+mutatis mutandis\s+', ' with necessary changes '),
            
            # Simplify complex structures
            (r'in the event that', 'if'),
            (r'in accordance with', 'following'),
            (r'with regard to', 'about'),
            (r'for the purpose of', 'to'),
            (r'in lieu of', 'instead of'),
            (r'by virtue of', 'because of'),
            
            # Simplify shall/may
            (r'\bshall\b', 'must'),
            (r'\bmay\b', 'can'),
            
            # Remove redundant phrases
            (r'null and void', 'invalid'),
            (r'cease and desist', 'stop'),
            (r'aid and abet', 'help'),
            (r'each and every', 'every'),
            (r'full and complete', 'complete')
        ]
    
    def simplify(self, text: str) -> str:
        """Simplify legal text"""
        if not text:
            return text
        
        simplified = text
        
        # Apply term replacements
        for legal_term, simple_term in self.legal_terms.items():
            pattern = re.compile(r'\b' + re.escape(legal_term) + r'\b', re.IGNORECASE)
            simplified = pattern.sub(simple_term, simplified)
        
        # Apply simplification rules
        for pattern, replacement in self.simplification_rules:
            simplified = re.sub(pattern, replacement, simplified, flags=re.IGNORECASE)
        
        # Break long sentences
        simplified = self._break_long_sentences(simplified)
        
        # Simplify numbers and dates
        simplified = self._simplify_numbers_dates(simplified)
        
        # Add explanations for remaining complex terms
        simplified = self._add_inline_explanations(simplified)
        
        return simplified
    
    def _break_long_sentences(self, text: str) -> str:
        """Break sentences longer than 20 words"""
        sentences = text.split('. ')
        simplified_sentences = []
        
        for sentence in sentences:
            words = sentence.split()
            if len(words) > 20:
                # Try to break at conjunctions
                parts = re.split(r'\s+(?:and|but|or|however|whereas)\s+', sentence)
                for part in parts:
                    if part:
                        simplified_sentences.append(part.strip())
            else:
                simplified_sentences.append(sentence)
        
        return '. '.join(simplified_sentences)
    
    def _simplify_numbers_dates(self, text: str) -> str:
        """Convert formal numbers/dates to simple format"""
        # Convert "twenty-one days" to "21 days"
        number_words = {
            'twenty-one': '21',
            'thirty': '30',
            'forty-five': '45',
            'sixty': '60',
            'ninety': '90'
        }
        
        for word, num in number_words.items():
            text = re.sub(rf'\b{word}\b', num, text, flags=re.IGNORECASE)
        
        return text
    
    def _add_inline_explanations(self, text: str) -> str:
        """Add explanations for complex terms that remain"""
        complex_terms = {
            'FIR': 'FIR (First Information Report - police complaint)',
            'RTI': 'RTI (Right to Information - request for government information)',
            'PIL': 'PIL (Public Interest Litigation - court case for public good)',
            'NGO': 'NGO (Non-Governmental Organization - social service group)'
        }
        
        for term, explanation in complex_terms.items():
            if term in text and explanation not in text:
                text = text.replace(term, explanation, 1)
        
        return text