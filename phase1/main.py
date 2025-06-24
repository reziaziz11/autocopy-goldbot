from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "7524328423:AAFPrLxZtxnyyGmmguhc5KU_e524xnq4thI"
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

@app.route("/", methods=["GET"])
def index():
    return "Bot Aktif (Phase 1)"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    message = data.get("message")
    if message:
        chat_id = message["chat"]["id"]
        text = message.get("text", "")
        payload = {
            "chat_id": chat_id,
            "text": f"Halo! Kamu mengirim: {text}"
        }
        requests.post(URL, json=payload)
    return {"ok": True}
