from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
)
import os
import logging

# Inisialisasi Flask
app = Flask(__name__)

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Ambil token dari environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN belum diatur di environment")

# Inisialisasi Bot
application = Application.builder().token(BOT_TOKEN).build()

# Handler /start
async def start(update: Update, context: CallbackContext):
    keyboard = [["💰 Daftar Akun", "📊 Statistik"], ["📞 Bantuan"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Selamat datang di DJGOLD Bot! 🎯", reply_markup=reply_markup)

# Handler default
async def reply_text(update: Update, context: CallbackContext):
    await update.message.reply_text("Perintah tidak dikenali. Ketik /start untuk memulai.")

# Pasang handler
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_text))

# Webhook endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        application.update_queue.put_nowait(update)
        return "ok", 200

# Cek status
@app.route("/", methods=["GET"])
def index():
    return "DJGOLD Bot aktif 🟢", 200

# Run lokal (opsional, untuk development)
if __name__ == "__main__":
    print("Menjalankan DJGOLD bot secara lokal...")
    application.run_polling()
