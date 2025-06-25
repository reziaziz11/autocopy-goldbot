from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import CommandHandler, ContextTypes
from telegram.ext import Dispatcher
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Init Flask app
app = Flask(__name__)
bot = Bot(token=TOKEN)

@app.route('/')
def home():
    return 'Bot is Live!'

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        handle_update(update)
    return "ok"

# Handler langsung tanpa Application
def handle_update(update: Update):
    message = update.message
    if message:
        text = message.text
        chat_id = message.chat.id

        if text == "/start":
            bot.send_message(chat_id=chat_id, text="Selamat datang di GOLD EXPERT BOT 🚀\nKetik /daftar untuk memulai.")
        elif text == "/daftar":
            bot.send_message(chat_id=chat_id, text="📝 Silakan masukkan *Nama Lengkap* kamu:", parse_mode="Markdown")

# Run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
