import re
from typing import Dict, Any, List, Optional
from datetime import datetime
import spacy
from config.logging_config import log

class QueryProcessor:
    """Advanced query processing and understanding"""
    
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            log.warning("spaCy model not found, downloading...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        
        # Query patterns
        self.intent_patterns = {
            'eligibility': [
                r'(?i)(am i eligible|can i apply|qualify for|entitled to)',
                r'(?i)(who can get|requirements for)'
            ],
            'procedure': [
                r'(?i)(how to apply|how do i|what is the process)',
                r'(?i)(steps to|procedure for)'
            ],
            'documents': [
                r'(?i)(what documents|papers needed|documents required)',
                r'(?i)(proof needed|certificates)'
            ],
            'complaint': [
                r'(?i)(file complaint|report|register case)',
                r'(?i)(complain about|take action)'
            ],
            'benefits': [
                r'(?i)(how much|amount|payment|compensation)',
                r'(?i)(benefits|money|financial)'
            ],
            'status': [
                r'(?i)(check status|track application|pending)',
                r'(?i)(application status|where is my)'
            ],
            'help': [
                r'(?i)(help me|need help|assist|support)',
                r'(?i)(what should i do|confused about)'
            ]
        }
    
    def process_query(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Process and understand user query"""
        # Clean query
        query = self._clean_query(query)
        
        # Detect language
        language = self._detect_language(query)
        
        # Extract intent
        intent = self._extract_intent(query)
        
        # Extract entities
        entities = self._extract_entities(query)
        
        # Detect urgency
        urgency = self._detect_urgency(query)
        
        # Expand query
        expanded_query = self._expand_query(query)
        
        # Determine category
        category = self._determine_category(query, entities)
        
        return {
            'original_query': query,
            'cleaned_query': query,
            'language': language,
            'intent': intent,
            'entities': entities,
            'urgency': urgency,
            'expanded_query': expanded_query,
            'category': category,
            'timestamp': datetime.now().isoformat()
        }
    
    def _clean_query(self, query: str) -> str:
        """Clean and normalize query"""
        # Remove extra spaces
        query = re.sub(r'\s+', ' ', query)
        
        # Fix common typos
        typo_corrections = {
            'widoe': 'widow',
            'pention': 'pension',
            'violance': 'violence',
            'complan': 'complain'
        }
        
        for typo, correct in typo_corrections.items():
            query = re.sub(rf'\b{typo}\b', correct, query, flags=re.IGNORECASE)
        
        return query.strip()
    
    def _detect_language(self, text: str) -> str:
        """Detect query language"""
        # Character-based detection
        if re.search(r'[\u0900-\u097F]', text):
            return 'hi'
        elif re.search(r'[\u0B80-\u0BFF]', text):
            return 'ta'
        elif re.search(r'[\u0C00-\u0C7F]', text):
            return 'te'
        return 'en'
    
    def _extract_intent(self, query: str) -> str:
        """Extract user intent from query"""
        query_lower = query.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return intent
        
        # Default intent based on keywords
        if 'pension' in query_lower:
            return 'eligibility'
        elif 'violence' in query_lower or 'abuse' in query_lower:
            return 'complaint'
        elif 'land' in query_lower or 'property' in query_lower:
            return 'dispute'
        
        return 'general'
    
    def _extract_entities(self, query: str) -> Dict[str, List[str]]:
        """Extract named entities from query"""
        doc = self.nlp(query)
        
        entities = {
            'persons': [],
            'locations': [],
            'organizations': [],
            'dates': [],
            'money': [],
            'documents': [],
            'schemes': []
        }
        
        # Extract spaCy entities
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                entities['persons'].append(ent.text)
            elif ent.label_ in ["GPE", "LOC"]:
                entities['locations'].append(ent.text)
            elif ent.label_ == "ORG":
                entities['organizations'].append(ent.text)
            elif ent.label_ == "DATE":
                entities['dates'].append(ent.text)
            elif ent.label_ == "MONEY":
                entities['money'].append(ent.text)
        
        # Custom entity extraction
        # Documents
        doc_patterns = [
            'aadhaar', 'pan card', 'ration card', 'voter id',
            'birth certificate', 'death certificate'
        ]
        for pattern in doc_patterns:
            if pattern in query.lower():
                entities['documents'].append(pattern)
        
        # Schemes
        scheme_patterns = [
            'widow pension', 'old age pension', 'disability pension',
            'pm kisan', 'mgnrega'
        ]
        for pattern in scheme_patterns:
            if pattern in query.lower():
                entities['schemes'].append(pattern)
        
        return entities
    
    def _detect_urgency(self, query: str) -> str:
        """Detect query urgency level"""
        urgent_keywords = [
            'urgent', 'emergency', 'immediately', 'help',
            'danger', 'threat', 'violence', 'abuse'
        ]
        
        query_lower = query.lower()
        
        if any(keyword in query_lower for keyword in urgent_keywords):
            return 'high'
        
        deadline_keywords = ['deadline', 'last date', 'expire']
        if any(keyword in query_lower for keyword in deadline_keywords):
            return 'medium'
        
        return 'normal'
    
    def _expand_query(self, query: str) -> str:
        """Expand query with synonyms and related terms"""
        expansions = {
            'widow': 'widow widowed husband died spouse death',
            'pension': 'pension allowance benefit scheme',
            'violence': 'violence abuse harassment assault',
            'land': 'land property acquisition compensation',
            'apply': 'apply application submit register enroll'
        }
        
        expanded = query
        for term, expansion in expansions.items():
            if term in query.lower():
                expanded += f" {expansion}"
        
        return expanded
    
    def _determine_category(self, query: str, entities: Dict) -> str:
        """Determine query category"""
        query_lower = query.lower()
        
        if 'pension' in query_lower or 'widow' in entities.get('schemes', []):
            return 'pension'
        elif 'violence' in query_lower or 'abuse' in query_lower:
            return 'domestic_violence'
        elif 'land' in query_lower or 'property' in query_lower:
            return 'land'
        elif 'wage' in query_lower or 'salary' in query_lower:
            return 'labor'
        
        return 'general'