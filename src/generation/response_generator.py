from typing import List, Dict, Any, Optional
from datetime import datetime
from config.settings import settings
from config.logging_config import log
from src.generation.templates import ResponseTemplates
from src.nlp.simplifier import TextSimplifier

class ResponseGenerator:
    """Generate user-friendly responses"""
    
    def __init__(self):
        self.templates = ResponseTemplates()
        self.simplifier = TextSimplifier()
    
    def generate_response(self,
                         query_info: Dict[str, Any],
                         retrieved_docs: List[Dict[str, Any]],
                         user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate complete response"""
        
        # Extract information
        intent = query_info.get('intent', 'general')
        category = query_info.get('category', 'general')
        urgency = query_info.get('urgency', 'normal')
        language = query_info.get('language', 'en')
        
        # Combine retrieved content
        combined_content = self._combine_retrieved_content(retrieved_docs)
        
        # Generate main answer
        if retrieved_docs:
            answer = self._generate_contextual_answer(
                combined_content,
                intent,
                category
            )
        else:
            answer = self.templates.get_no_info_template(category)
        
        # Simplify answer
        simplified_answer = self.simplifier.simplify(answer)
        
        # Generate practical steps
        steps = self._generate_steps(category, intent, retrieved_docs)
        
        # Add emergency information if needed
        emergency_info = None
        if urgency == 'high':
            emergency_info = self._get_emergency_info(category)
        
        # Format sources
        sources = self._format_sources(retrieved_docs)
        
        # Calculate confidence
        confidence = self._calculate_confidence(retrieved_docs)
        
        response = {
            'answer': simplified_answer,
            'practical_steps': steps,
            'emergency_info': emergency_info,
            'sources': sources,
            'confidence': confidence,
            'language': language,
            'category': category,
            'intent': intent,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add follow-up suggestions
        response['follow_up_questions'] = self._suggest_follow_ups(category, intent)
        
        return response
    
    def _combine_retrieved_content(self, documents: List[Dict]) -> str:
        """Combine content from retrieved documents"""
        if not documents:
            return ""
        
        contents = []
        for doc in documents[:3]:  # Use top 3 documents
            content = doc.get('text', doc.get('content', ''))
            contents.append(content)
        
        return "\n\n".join(contents)
    
    def _generate_contextual_answer(self,
                                   content: str,
                                   intent: str,
                                   category: str) -> str:
        """Generate answer based on content and context"""
        
        # Extract key information based on intent
        if intent == 'eligibility':
            answer = self._extract_eligibility_info(content)
        elif intent == 'procedure':
            answer = self._extract_procedure_info(content)
        elif intent == 'documents':
            answer = self._extract_documents_info(content)
        elif intent == 'benefits':
            answer = self._extract_benefits_info(content)
        else:
            answer = self._summarize_content(content)
        
        # Add category-specific context
        answer = self.templates.wrap_with_category_context(answer, category)
        
        return answer
    
    def _extract_eligibility_info(self, content: str) -> str:
        """Extract eligibility information"""
        import re
        
        # Look for eligibility patterns
        patterns = [
            r'eligible[^.]*\.',
            r'qualify[^.]*\.',
            r'entitled[^.]*\.',
            r'criteria[^.]*\.'
        ]
        
        eligibility_info = []
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            eligibility_info.extend(matches)
        
        if eligibility_info:
            return "Eligibility: " + " ".join(eligibility_info[:3])
        
        return "Please check with local office for eligibility criteria."
    
    def _extract_procedure_info(self, content: str) -> str:
        """Extract procedure information"""
        import re
        
        # Look for procedure patterns
        patterns = [
            r'step[^.]*\.',
            r'process[^.]*\.',
            r'apply[^.]*\.',
            r'submit[^.]*\.'
        ]
        
        procedure_info = []
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            procedure_info.extend(matches)
        
        if procedure_info:
            return "Process: " + " ".join(procedure_info[:3])
        
        return "Visit nearest office for application process."
    
    def _extract_documents_info(self, content: str) -> str:
        """Extract document requirements"""
        import re
        
        # Common document patterns
        doc_patterns = [
            'aadhaar', 'pan card', 'ration card', 'voter id',
            'birth certificate', 'death certificate', 'income certificate',
            'caste certificate', 'bank passbook', 'photograph'
        ]
        
        found_docs = []
        content_lower = content.lower()
        
        for doc in doc_patterns:
            if doc in content_lower:
                found_docs.append(doc.title())
        
        if found_docs:
            return f"Documents needed: {', '.join(found_docs)}"
        
        return "Contact office for document requirements."
    
    def _extract_benefits_info(self, content: str) -> str:
        """Extract benefit/amount information"""
        import re
        
        # Look for amount patterns
        amount_pattern = r'Rs\.?\s*\d+[,\d]*'
        amounts = re.findall(amount_pattern, content)
        
        if amounts:
            return f"Benefits: {', '.join(amounts[:2])}"
        
        return "Contact office for benefit details."
    
    def _summarize_content(self, content: str) -> str:
        """Create a simple summary"""
        sentences = content.split('.')
        summary = '. '.join(sentences[:3])
        return summary
    
    def _generate_steps(self,
                       category: str,
                       intent: str,
                       documents: List[Dict]) -> List[str]:
        """Generate practical steps"""
        return self.templates.get_steps_template(category, intent)
    
    def _get_emergency_info(self, category: str) -> Dict[str, str]:
        """Get emergency contact information"""
        emergency_contacts = {
            'domestic_violence': {
                'helpline': '181',
                'name': 'Women Helpline',
                'available': '24/7'
            },
            'general': {
                'helpline': '100',
                'name': 'Police',
                'available': '24/7'
            }
        }
        
        return emergency_contacts.get(category, emergency_contacts['general'])
    
    def _format_sources(self, documents: List[Dict]) -> List[str]:
        """Format document sources"""
        sources = []
        for doc in documents[:3]:
            metadata = doc.get('metadata', {})
            source = metadata.get('filename', 'Government Document')
            if source not in sources:
                sources.append(source)
        
        return sources
    
    def _calculate_confidence(self, documents: List[Dict]) -> float:
        """Calculate response confidence"""
        if not documents:
            return 0.0
        
        # Average of top document scores
        scores = [doc.get('score', 0) for doc in documents[:3]]
        avg_score = sum(scores) / len(scores)
        
        # Convert to 0-1 range
        confidence = min(max(avg_score, 0), 1)
        
        return round(confidence, 2)
    
    def _suggest_follow_ups(self, category: str, intent: str) -> List[str]:
        """Suggest follow-up questions"""
        follow_ups = {
            'pension': [
                "How to check pension application status?",
                "What if my application is rejected?",
                "How to update bank details for pension?"
            ],
            'domestic_violence': [
                "How to get protection order?",
                "Where is nearest shelter home?",
                "How to get free legal help?"
            ],
            'land': [
                "How to file objection to land acquisition?",
                "How compensation amount is calculated?",
                "What are my rights as land owner?"
            ]
        }
        
        return follow_ups.get(category, [
            "How to apply for this?",
            "What documents are needed?",
            "Where is the nearest office?"
        ])