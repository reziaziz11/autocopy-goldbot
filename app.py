import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
)
from bot.handlers import start
from dotenv import load_dotenv
import asyncio

# Load .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Flask app
app = Flask(__name__)

# Init Telegram bot
bot_app = ApplicationBuilder().token(TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))

@app.route("/")
def home():
    return "✅ DJGOLD_BOT aktif!"

@app.route("/webhook", methods=["POST"])
async def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot_app.bot)
        await bot_app.process_update(update)
        return "ok", 200

# Jalankan Flask + Telegram polling di background
def run():
    loop = asyncio.get_event_loop()
    loop.create_task(bot_app.initialize())
    loop.create_task(bot_app.start())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

if __name__ == "__main__":
    run()
