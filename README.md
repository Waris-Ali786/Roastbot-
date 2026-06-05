# RoastBot — AI Sarcastic Chat System

RoastBot is a Flask-based AI chat application powered by the Groq API using the LLaMA 3.3 70B model. It is designed to generate short-form, sarcastic, humor-driven responses to user input in real time through a web interface.

The system is built as a personality-driven conversational layer rather than a utility chatbot. Its core function is to interpret user input and return controlled, structured, humorous responses with a consistent tone.

---

# What It Does

- Accepts user input through a browser-based chat interface
- Processes input using Groq-hosted LLaMA 3.3 model
- Generates concise sarcastic responses (maximum two lines)
- Maintains a consistent roast-oriented personality across all interactions
- Handles empty or invalid input with fallback responses
- Streams responses back into a real-time chat UI
- Includes a responsive frontend with typing state simulation and message rendering

---

# System Overview

## Backend (app.py)

The backend is a Flask application exposing two routes:

- `/` serves the frontend interface  
- `/chat` processes POST requests containing user input  

### Flow:
- Receive user message
- Construct structured prompt enforcing tone and length constraints
- Send request to Groq API (llama-3.3-70b-versatile)
- Return generated response as JSON

No persistent memory is used. Each request is stateless.

---

## Frontend (templates/index.html)

Single-page chat interface implemented in HTML, CSS, and JavaScript.

### Functions:
- Sends asynchronous requests to `/chat`
- Dynamically renders chat bubbles for user and assistant
- Displays typing indicator during API calls
- Provides input prefill shortcuts for faster interaction
- Maintains a clean conversation flow without page reloads

---

# Tech Stack

- Python
- Flask
- Groq API (LLaMA 3.3 70B Versatile)
- HTML
- CSS
- JavaScript
- Vercel (Deployment)

---

# Project Structure

```text
RoastBot/
│
├── app.py                  # Flask backend API
├── templates/
│   └── index.html         # Frontend chat interface
├── requirements.txt       # Dependencies
└── README.md
