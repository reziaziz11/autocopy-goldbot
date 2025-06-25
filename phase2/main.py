from flask import Flask, request
from telegram import Bot

import os

app = Flask(__name__)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

@app.route('/')
def home():
    return 'Bot is live!', 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("==> Received:", data)  # Debug

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        # Start form interaktif
        if text == "/start":
            bot.send_message(chat_id=chat_id, text="👋 Selamat datang di DJGOLD BOT!\n\nSilakan isi formulir berikut untuk mendaftar.")
            bot.send_message(chat_id=chat_id, text="📌 Masukkan *nama lengkap* kamu:", parse_mode="Markdown")

            # Simpan state user di dict (nanti akan diganti dengan DB)
            # Sementara simple dict
            user_state[chat_id] = {"step": "nama"}

        elif chat_id in user_state:
            step = user_state[chat_id]["step"]

            if step == "nama":
                user_state[chat_id]["nama"] = text
                user_state[chat_id]["step"] = "email"
                bot.send_message(chat_id=chat_id, text="📧 Masukkan *email* kamu:", parse_mode="Markdown")

            elif step == "email":
                user_state[chat_id]["email"] = text
                user_state[chat_id]["step"] = "hp"
                bot.send_message(chat_id=chat_id, text="📱 Masukkan *nomor HP* kamu:", parse_mode="Markdown")

            elif step == "hp":
                user_state[chat_id]["hp"] = text
                user_state[chat_id]["step"] = "broker"
                bot.send_message(chat_id=chat_id, text="💹 Masukkan *broker* yang digunakan:", parse_mode="Markdown")

            elif step == "broker":
                user_state[chat_id]["broker"] = text
                user_state[chat_id]["step"] = "akun"
                bot.send_message(chat_id=chat_id, text="🔢 Masukkan *nomor akun MT5* kamu:", parse_mode="Markdown")

            elif step == "akun":
                user_state[chat_id]["akun"] = text
                user_data = user_state[chat_id]

                # Kirim data konfirmasi
                message = (
                    "✅ Pendaftaran selesai!\n\n"
                    f"👤 Nama: {user_data['nama']}\n"
                    f"📧 Email: {user_data['email']}\n"
                    f"📱 HP: {user_data['hp']}\n"
                    f"💹 Broker: {user_data['broker']}\n"
                    f"🔢 Akun MT5: {user_data['akun']}"
                )
                bot.send_message(chat_id=chat_id, text=message)
                del user_state[chat_id]  # reset

    return 'OK', 200

# Tempat simpan state user sementara
user_state = {}

if __name__ == '__main__':
    app.run(debug=True)
