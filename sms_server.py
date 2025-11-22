# sms_server.py

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from src.nyayaai_core import rag_answer

app = Flask(__name__)

MAX_SHORT = 110
MAX_STEP = 90
MAX_TOTAL = 300

def trim(text, limit):
    text = text.strip()
    return text if len(text) <= limit else text[:limit] + "..."

@app.route("/sms", methods=["POST"])
def sms_reply():
    query = request.form.get("Body", "").strip()
    print("\n==== QUERY RECEIVED ====")
    print(query)

    try:
        ans = rag_answer(query)

        # STRICT TWILIO-SAFE LIMITS
        short = trim(ans["short_answer"], MAX_SHORT)
        step1 = trim(ans["steps"][0], MAX_STEP)

        reply = f"{short}\n\n1. {step1}"

        # HARD ENFORCE total limit
        reply = trim(reply, MAX_TOTAL)

        print("\n==== FINAL SMS LENGTH:", len(reply))
        print(reply)

        resp = MessagingResponse()
        resp.message(reply)
        return str(resp)

    except Exception as e:
        print("ERROR:", e)
        resp = MessagingResponse()
        resp.message("NyayaAI error. Try again.")
        return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
