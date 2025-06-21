# ======== DEBUG CHECK BOT DJGOLD_BOT ========

import os
import asyncio
import nest_asyncio
from dotenv import load_dotenv
from flask import Flask, request
from telegram.ext import ApplicationBuilder
from handlers.start import start_handler

# === Load .env ===
load_dotenv()
TOKEN = os.getenv("TOKEN")

# === Bot Setup ===
app = Flask(__name__)

async def run_bot():
    bot_app = ApplicationBuilder().token(TOKEN).build()
    bot_app.add_handler(start_handler)
    await bot_app.initialize()
    await bot_app.start()
    await bot_app.updater.start_polling()
    await bot_app.updater.idle()

@app.route('/')
def index():
    return "DJGOLD_BOT is alive!"

@app.route('/webhook', methods=['POST'])
def webhook():
    return "Webhook received", 200

if __name__ == '__main__':
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    app.run(host='0.0.0.0', port=10000)
