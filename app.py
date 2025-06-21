import os
import asyncio
from flask import Flask, request
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import nest_asyncio

# === Load .env ===
load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://djgoldbot.onrender.com")
PORT = int(os.getenv("PORT", 10000))

# === Inisialisasi Flask ===
flask_app = Flask(__name__)
nest_asyncio.apply()

# === Inisialisasi Telegram Application ===
bot_app = Application.builder().token(TOKEN).build()

# === Command /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

# === Tambahkan handler ke bot ===
bot_app.add_handler(CommandHandler("start", start))

# === Webhook endpoint ===
@flask_app.route("/webhook", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return "OK", 200

# === Start function ===
async def main():
    await bot_app.initialize()
    await bot_app.bot.set_webhook(f"{WEBHOOK_URL}/webhook")
    print(f"✅ Webhook telah diset ke: {WEBHOOK_URL}/webhook")
    await bot_app.start()
    await bot_app.updater.wait()  # ❌ GANTI baris ini!

# === Run Flask + Bot ===
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    flask_app.run(host="0.0.0.0", port=PORT)
