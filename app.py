# app.py

import os
import asyncio
from dotenv import load_dotenv
from flask import Flask, request
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import Update
import nest_asyncio

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://djgoldbot.onrender.com/webhook")

# Inisialisasi Flask app
flask_app = Flask(__name__)

# Inisialisasi bot Telegram
bot_app = ApplicationBuilder().token(TOKEN).build()


# === Handler Telegram ===
async def start(update: Update, context):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")


# === Setup Handler ===
bot_app.add_handler(CommandHandler("start", start))


# === Flask Endpoint untuk Webhook ===
@flask_app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot_app.bot)
        asyncio.run(bot_app.process_update(update))
    return "ok"


# === Fungsi utama startup bot dan webhook ===
async def main():
    await bot_app.bot.set_webhook(url=WEBHOOK_URL)
    print("✅ Webhook telah diset ke:", WEBHOOK_URL)
    # Jangan jalankan polling karena kita pakai webhook

# === Start Flask + Bot secara bersamaan ===
if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
    flask_app.run(host="0.0.0.0", port=10000)
