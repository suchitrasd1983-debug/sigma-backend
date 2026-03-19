from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic

app = Flask(__name__)
CORS(app)

API_KEY = "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"

SYSTEM = """You are SIGMA AI - a savage desi bro who talks in Hinglish like close Indian friends do.
- SHORT replies only - WhatsApp style
- MIRROR user energy - gaaliyan mile toh gaaliyan do, normal mile toh clean raho
- Savage, witty, brutally honest
- Desi references - IIT, exams, cricket, anime"""

client = anthropic.Anthropic(api_key=API_KEY)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        messages = data.get("messages", [])
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=SYSTEM,
            messages=messages
        )
        return jsonify({"reply": response.content[0].text})
    except Exception as e:
        return jsonify({"reply": "Server gaya tel lene."}), 500

@app.route("/")
def home():
    return "SIGMA AI chal raha hai!"

application = app
import os
port = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
