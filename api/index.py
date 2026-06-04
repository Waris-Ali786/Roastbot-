from flask import Flask, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/")
def home():
    return "RoastBot is live 🔥"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json() or {}
        user_answer = data.get("answer", "")

        if not user_answer:
            prompt = "User gave no answer. Respond sarcastically in 2 lines."
        else:
            prompt = f"User said: {user_answer}. Reply sarcastically in 2 lines."

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        return jsonify({"response": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔥 IMPORTANT FOR VERCEL
def handler(environ, start_response):
    return app(environ, start_response)
