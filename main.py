import os
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

API_KEY = os.getenv("610ea384232c14956b70a9bd7ba707c795a5157b3878e2987f107b118e1a0a66")
LLM_MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"

PROMPT = (
    "You are an Islamic teacher chatbot. Only answer based on the Qur’an, authentic Hadith, and respected scholars. "
    "Be kind, respectful to Sunni, Shia, and others. Give short answers for simple questions, and detailed ones when needed."
)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_message = data.get("message", "")
    sender = data.get("sender", "Unknown")

    reply = get_ai_reply(user_message)
    return jsonify({"reply": reply})

def get_ai_reply(message):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": message}
        ],
        "max_tokens": 500,
        "temperature": 0.6
    }

    response = requests.post("https://api.together.xyz/v1/chat/completions", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
