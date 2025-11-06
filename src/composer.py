def compose_response(intent, matches, lang="en"):
    if not matches or intent == "unknown":
        return "Sorry, I don't have info on that. Please contact your nearest legal aid office."

    top = matches[0]
    base = top["plain_text_ta"] if lang == "ta" else top["plain_text_en"]

    if intent == "domestic_violence":
        base += " Call 181 if in danger."
    elif intent == "unpaid_wages":
        base += " Reply YES for steps."
    elif intent == "widow_pension":
        base += " Visit local office for help."

    return base
