class ResponseTemplates:
    """Response templates for different scenarios"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self):
        """Load response templates"""
        return {
            'pension': {
                'intro': "Regarding pension schemes:",
                'steps': [
                    "Visit your nearest CSC or Tehsildar office",
                    "Carry Aadhaar card, bank passbook, and age/income proof",
                    "Fill application form (available free)",
                    "Submit form with documents",
                    "Collect acknowledgment receipt",
                    "Check status after 30 days"
                ],
                'contact': "For help, contact District Social Welfare Office"
            },
            'domestic_violence': {
                'intro': "If you are facing domestic violence:",
                'steps': [
                    "Call Women Helpline 181 immediately",
                    "Go to nearest police station",
                    "File complaint under Domestic Violence Act",
                    "Ask for NCR copy",
                    "Contact Protection Officer in your area",
                    "Get medical examination if injured",
                    "Contact local NGO for free legal help"
                ],
                'contact': "Emergency: Call 181 or 100"
            },
            'land': {
                'intro': "For land-related matters:",
                'steps': [
                    "Gather all land documents (patta, sale deed, etc.)",
                    "Visit Tehsildar/Revenue office",
                    "Check land records and verify ownership",
                    "File written objection if needed",
                    "Get legal notice drafted",
                    "Apply for legal aid if cannot afford lawyer",
                    "Attend all hearings"
                ],
                'contact': "Contact District Legal Services Authority for free legal aid"
            }
        }
    
    def get_steps_template(self, category: str, intent: str = None):
        """Get steps for a category"""
        template = self.templates.get(category, self.templates.get('pension'))
        return template['steps']
    
    def get_no_info_template(self, category: str):
        """Template when no information is found"""
        return (
            f"I don't have specific information about your query. "
            f"Please contact your nearest government office or "
            f"call the helpline for assistance."
        )
    
    def wrap_with_category_context(self, answer: str, category: str):
        """Add category-specific context to answer"""
        template = self.templates.get(category, {})
        intro = template.get('intro', '')
        contact = template.get('contact', '')
        
        return f"{intro}\n\n{answer}\n\n{contact}"