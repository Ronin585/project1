import os
import openai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from utils.helpers import num_tokens_from_messages, trim_messages, safe_response, save_chat_to_txt, save_chat_to_json
import logging
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key or openai.api_key.strip() == "" or openai.api_key == "DEMO_DISABLED":
        logging.error("❌ API key is missing or invalid in .env file. Exiting...")
        raise RuntimeError("OpenAI API key missing or invalid.")

app = Flask(__name__)
chat_history = []
if os.path.exists("chat_history.json"):
    with open("chat_history.json", "r", encoding="utf-8") as f:
        try:
            chat_history = json.load(f)
        except Exception as e:
            logging.warning(f"Could not load existing chat history: {e}")
            
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "You are a helpful clothing store assistant.")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 3000))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return safe_response("No input message provided.")

    chat_history.append({"role": "user", "content": user_input})
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history
    full_messages = trim_messages(full_messages, MAX_TOKENS)
    
    if not openai.api_key or openai.api_key.strip() == "" or openai.api_key == "DEMO_DISABLED":
      return jsonify({"reply": "❌ Error: API key is missing or invalid. Please check your .env file or contact the developer."})
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=full_messages,
        )
        reply = response['choices'][0]['message']['content'].strip()
        chat_history.append({"role": "assistant", "content": reply})
        save_chat_to_txt(chat_history)
        save_chat_to_json(chat_history)
        return jsonify({"reply": reply})
    except Exception as e:
        logging.error(f"Error calling OpenAI API: {e}")
        return safe_response("An unexpected error occurred. Please try again later.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
