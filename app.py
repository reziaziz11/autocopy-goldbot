import os
import asyncio
from dotenv import load_dotenv
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder
from handlers.start import start_handler  # pastikan handler ini udah benar dan ada

import nest_asyncio

# === Init Flask ===
app_flask = Flask(__name__)

@app_flask.route("/")
def home():
    return "✅ DJGOLD Bot is live and running!"

# === Load Token ===
load_dotenv()
TOKEN = os.getenv("TOKEN")

# === Bot Handler ===
async def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(start_handler)
    print("🚀 Bot Telegram dijalankan via polling...")
    await app.run_polling()

# === Run Both Flask & Telegram Bot Together ===
if __name__ == "__main__":
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    app_flask.run(host="0.0.0.0", port=10000)
