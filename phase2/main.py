import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Token bot dari environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Inisialisasi aplikasi Telegram
telegram_app = Application.builder().token(BOT_TOKEN).build()

# Handler command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Selamat datang di DJGOLD BOT 🚀")

# Tambahkan semua handler yang kamu punya
telegram_app.add_handler(CommandHandler("start", start))

# Flask app untuk webhook
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "DJGOLD BOT online!"

@flask_app.route("/webhook", methods=["POST"])
async def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), telegram_app.bot)
        await telegram_app.process_update(update)
        return "ok", 200

# Untuk Render: Flask app yang akan dipanggil oleh gunicorn
app = flask_app
