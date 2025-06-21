# app.py

import os
import asyncio
from dotenv import load_dotenv
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from threading import Thread

# === Load .env ===
load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not TOKEN or not WEBHOOK_URL:
    raise ValueError("❌ TOKEN atau WEBHOOK_URL belum diatur di Render!")

# === Flask App ===
flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return "✅ DJGOLD_BOT Aktif (Webhook)"

# === Telegram Handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ DJGOLD_BOT aktif dan siap menerima perintah!")

# === Bot App ===
async def main():
    bot_app = ApplicationBuilder().token(TOKEN).build()

    bot_app.add_handler(CommandHandler("start", start))

    # Set webhook
    await bot_app.bot.set_webhook(WEBHOOK_URL)
    print(f"✅ Webhook telah diset ke: {WEBHOOK_URL}")

    # Start aplikasi Telegram
    await bot_app.start()
    await asyncio.Event().wait()

def run_flask():
    flask_app.run(host="0.0.0.0", port=10000)

if __name__ == '__main__':
    Thread(target=run_flask).start()
    asyncio.run(main())
