# app.py

import os
import asyncio
from dotenv import load_dotenv
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler

# === Load Token ===
load_dotenv()
TOKEN = os.getenv("TOKEN")

# === Bot Handler ===
async def start(update, context):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

async def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("🚀 Bot Telegram dijalankan via polling...")
    await app.run_polling()

# === Flask Dummy Server ===
web_app = Flask(__name__)

@web_app.route('/')
def index():
    return "✅ DJGOLD_BOT aktif (dummy HTTP server)."

def run_web():
    web_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

# === Jalankan Flask + Bot ===
if __name__ == '__main__':
    # Jalanin Flask di thread terpisah
    Thread(target=run_web).start()
    # Jalanin bot di event loop utama
    asyncio.run(run_bot())
