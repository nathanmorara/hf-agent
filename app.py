from flask import Flask, request
import requests
import os

app = Flask(__name__)

HF_API_KEY = os.getenv("HF_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

HF_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

def query_hf(text):
    response = requests.post(HF_URL, headers=HEADERS, json={"inputs": text})
    try:
        return response.json()[0]["generated_text"]
    except:
        return "Error processing request"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

@app.route("/", methods=["GET"])
def home():
    return "Telegram AI Bot is running 🚀"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"].get("text", "")

        reply = query_hf(user_text)
        send_message(chat_id, reply)

    return "ok"

app.run(host="0.0.0.0", port=5000)