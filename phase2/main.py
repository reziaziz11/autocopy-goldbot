import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Ambil variabel dari environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN belum diatur di environment")

# Inisialisasi Flask
flask_app = Flask(__name__)

# Inisialisasi bot Telegram (Application)
tg_app = Application.builder().token(BOT_TOKEN).build()

# === HANDLER BOT ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Selamat datang di DJGOLD BOT 🚀\n\nKetik /menu untuk mulai.")

tg_app.add_handler(CommandHandler("start", start))

# === ROUTE FLASK ===
@flask_app.route("/")
def home():
    return "DJGOLD BOT AKTIF ✅", 200

@flask_app.route("/webhook", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, tg_app.bot)
    await tg_app.process_update(update)
    return "OK", 200

# === SET WEBHOOK ===
@flask_app.before_first_request
def setup_webhook():
    if WEBHOOK_URL:
        tg_app.bot.set_webhook(url=WEBHOOK_URL)
        print("Webhook diatur ke:", WEBHOOK_URL)

# === RUN ===
if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
