INTENT_KEYWORDS = {
    "domestic_violence": ["husband", "beat", "violence", "abuse", "அடிக்க"],
    "unpaid_wages": ["salary", "wages", "employer", "pay", "பணம்"],
    "widow_pension": ["widow", "pension", "பென்ஷன்", "husband died"]
}

def detect_language(text):
    for ch in text:
        if '\u0B80' <= ch <= '\u0BFF':
            return "ta"
    return "en"

def detect_intent(text):
    t = text.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(k in t for k in keywords):
            return intent
    return "unknown"
