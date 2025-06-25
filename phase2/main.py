import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Ambil variabel environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN belum diatur di environment")

# Inisialisasi bot
app = Flask(__name__)
telegram_app = Application.builder().token(BOT_TOKEN).build()

# ===== HANDLER =====
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Selamat datang di DJGOLD BOT 🚀\n\nKetik /menu untuk mulai.")

telegram_app.add_handler(CommandHandler("start", start_handler))

# ===== ROUTE FLASK =====
@app.route("/")
def index():
    return "DJGOLD BOT aktif ✅", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        telegram_app.update_queue.put_nowait(Update.de_json(request.get_json(force=True), telegram_app.bot))
        return "OK", 200
    return "Method not allowed", 405

# ===== SETUP WEBHOOK SAAT APLIKASI MULAI =====
@app.before_first_request
def activate_webhook():
    if WEBHOOK_URL:
        telegram_app.bot.set_webhook(WEBHOOK_URL)
        print("Webhook diatur ke:", WEBHOOK_URL)

# ===== JALANKAN TELEGRAM BOT DI BACKGROUND =====
import threading
def run_telegram_polling():
    telegram_app.run_polling(allowed_updates=Update.ALL_TYPES)

threading.Thread(target=run_telegram_polling, daemon=True).start()

# ===== JALANKAN FLASK APP =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
