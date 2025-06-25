from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,  # ✅ perbaikan: pakai huruf kecil
    CallbackContext,
)
import os
import logging

# Inisialisasi Flask
app = Flask(__name__)

# Konfigurasi logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Token bot dari environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN belum diatur di environment")

# Inisialisasi Telegram Bot
application = Application.builder().token(BOT_TOKEN).build()

# ====== HANDLER TELEGRAM ======

# /start
async def start(update: Update, context: CallbackContext):
    keyboard = [["💰 Daftar Akun", "📊 Statistik"], ["📞 Bantuan"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Selamat datang di DJGOLD Bot! 🎯", reply_markup=reply_markup)

# Pesan umum
async def reply_text(update: Update, context: CallbackContext):
    await update.message.reply_text("Perintah tidak dikenali. Ketik /start untuk memulai.")

# Daftarkan handler ke application
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_text))

# ====== FLASK ROUTE UNTUK WEBHOOK ======

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        application.update_queue.put_nowait(update)
        return "ok", 200

@app.route("/", methods=["GET"])
def index():
    return "DJGOLD Bot aktif 🟢", 200

# ====== RUNNING ======
if __name__ == "__main__":
    print("Menjalankan bot di mode local/testing")
    application.run_polling()
