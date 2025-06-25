from flask import Flask, request import requests import json

app = Flask(name)

BOT_TOKEN = "7524328423:AAFPrLxZtxnyyGmmguhc5KU_e524xnq4thI" API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

user_states = {} user_data = {}

DATA_FILE = "phase2/user_data.json"

def save_data(): with open(DATA_FILE, "w") as f: json.dump(user_data, f, indent=2)

def send_message(chat_id, text, reply_markup=None): payload = { "chat_id": chat_id, "text": text, "parse_mode": "HTML" } if reply_markup: payload["reply_markup"] = json.dumps(reply_markup) requests.post(f"{API_URL}/sendMessage", data=payload)

@app.route("/webhook", methods=["POST"]) def webhook(): data = request.get_json()

if "message" in data:
    chat_id = data["message"]["chat"]["id"]
    user_id = data["message"]["from"]["id"]
    text = data["message"].get("text", "")

    state = user_states.get(user_id)

    if text == "/start":
        send_message(chat_id, "Selamat datang di pendaftaran XAUUSD Elite!\nKetik /daftar untuk mulai.")
        user_states.pop(user_id, None)

    elif text == "/daftar":
        user_states[user_id] = "nama"
        user_data[user_id] = {}
        send_message(chat_id, "Masukkan nama lengkap Anda:")

    elif state == "nama":
        user_data[user_id]["nama"] = text
        user_states[user_id] = "email"
        send_message(chat_id, "Masukkan email aktif Anda:")

    elif state == "email":
        if "@" in text and "." in text:
            user_data[user_id]["email"] = text
            user_states[user_id] = "wa"
            send_message(chat_id, "Masukkan nomor WhatsApp Anda:")
        else:
            send_message(chat_id, "Format email tidak valid. Coba lagi:")

    elif state == "wa":
        if text.isdigit():
            user_data[user_id]["wa"] = text
            user_states[user_id] = "mt5"
            send_message(chat_id, "Masukkan nomor akun MT5 Anda:")
        else:
            send_message(chat_id, "Nomor WA harus berupa angka. Coba lagi:")

    elif state == "mt5":
        if text.isdigit():
            user_data[user_id]["mt5"] = text
            user_states.pop(user_id)
            save_data()
            u = user_data[user_id]
            msg = f"✅ Pendaftaran berhasil!\n\n<b>Nama:</b> {u['nama']}\n<b>Email:</b> {u['email']}\n<b>WA:</b> {u['wa']}\n<b>MT5:</b> {u['mt5']}"
            send_message(chat_id, msg)
        else:
            send_message(chat_id, "Nomor MT5 harus berupa angka. Coba lagi:")

return "ok"

@app.route("/", methods=["GET"]) def index(): return "BOT PHASE 2 ACTIVE"

