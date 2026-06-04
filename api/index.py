import os
from pathlib import Path
from dotenv import load_dotenv

# ------------------------------------------------------------------
# 1. Locate .env file absolutely
# ------------------------------------------------------------------
script_dir = Path(__file__).resolve().parent          # /funnybot/api
project_root = script_dir.parent                      # /funnybot
env_path = project_root / ".env"

print(f"Looking for .env at: {env_path}")
print(f".env exists: {env_path.exists()}")

if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)
    print(".env loaded successfully")
else:
    print("WARNING: .env file not found. Will try environment variable directly.")

# ------------------------------------------------------------------
# 2. Get API key
# ------------------------------------------------------------------
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    # Try to read from .env manually as fallback
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('GROQ_API_KEY='):
                    api_key = line.strip().split('=', 1)[1]
                    break
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set. Please set it in .env or as an environment variable.")

print(f"API key loaded (first 10 chars): {api_key[:10]}...")

# ------------------------------------------------------------------
# 3. Initialize Groq and Flask
# ------------------------------------------------------------------
from flask import Flask, request, jsonify, render_template
from groq import Groq

client = Groq(api_key=api_key)

BASE_DIR = script_dir
PROJECT_ROOT = project_root
TEMPLATE_DIR = PROJECT_ROOT / 'templates'

app = Flask(__name__, template_folder=str(TEMPLATE_DIR))

@app.route("/")
def index():
    return render_template("index.html")

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
        reply = response.choices[0].message.content
        return jsonify({"response": reply})
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
