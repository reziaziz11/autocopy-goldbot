from flask import Flask, request
import requests
import json

app = Flask(__name__)

BOT_TOKEN = "7524328423:AAFPrLxZtxnyyGmmguhc5KU_e524xnq4thI"

def send_message(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)
    requests.post(url, json=payload)

@app.route('/')
def index():
    return 'OK'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data or "message" not in data:
        return "no message"

    message = data["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        welcome = "<b>Selamat datang di DJGOLD_BOT 🟡</b>\n\nSilakan pilih menu di bawah:"
        keyboard = {
            "keyboard": [
                [{"text": "📋 Daftar Akun"}],
                [{"text": "📊 Cek Status"}]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": False
        }
        send_message(chat_id, welcome, reply_markup=keyboard)

    return "ok"
