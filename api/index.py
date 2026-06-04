from flask import Flask, request, jsonify, render_template
from groq import Groq
import os

app = Flask(
    __name__,
    template_folder="../templates"
)

# Vercel environment variable
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -------------------
# HOME PAGE
# -------------------
@app.route("/")
def index():
    return render_template("index.html")


# -------------------
# CHAT ROUTE (YOUR PROMPT UNCHANGED)
# -------------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json() or {}
        user_answer = data.get("answer", "")

        if not user_answer:
            prompt = "The user did not provide an answer. Respond sarcastically, make a cutting joke, then ask a new question. Be funny and slightly mean, not more than 2 lines."
        else:
            prompt = f"The user answered: '{user_answer}'. Respond sarcastically, make a cutting joke, then ask a new question. Be funny and slightly mean. Not more than 2 lines."

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )

        return jsonify({
            "response": response.choices[0].message.content
        })

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500
