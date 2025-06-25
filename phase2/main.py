from flask import Flask, request
from telegram import Bot, Update
import os

# Token bot Telegram
BOT_TOKEN = "7524328423:AAFPrLxZtxnyyGmmguhc5KU_e524xnq4thI"
bot = Bot(token=BOT_TOKEN)

app = Flask(__name__)

@app.route("/")
def index():
    return "DJGOLD BOT IS RUNNING ✅"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, bot)

        chat_id = update.effective_chat.id
        message = update.effective_message.text

        print(f"[LOG] Pesan dari {chat_id}: {message}")

        if message == "/start":
            bot.send_message(chat_id=chat_id, text="Selamat datang di DJGOLD BOT 💰\n\nPantau sinyal & auto-copy XAUUSD di sini!")

        elif "halo" in message.lower():
            bot.send_message(chat_id=chat_id, text="Halo juga! Ada yang bisa dibantu?")

        else:
            bot.send_message(chat_id=chat_id, text="Perintah tidak dikenali. Ketik /start untuk memulai.")

        return "OK", 200

    except Exception as e:
        print("[ERROR]", e)
        return "Internal Server Error", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # default port Render
    app.run(host="0.0.0.0", port=port)
