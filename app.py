import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

from bot.handlers import start_handler

app = Flask(__name__)

# === Setup Bot ===
TOKEN = os.getenv("TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # contoh: https://djgoldbot.onrender.com/webhook

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start_handler))

@app.route("/", methods=["GET"])
def home():
    return "✅ DJGOLD_BOT is running!"

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)

        async def process():
            await application.initialize()  # WAJIB sebelum process_update
            await application.process_update(update)

        asyncio.run(process())
        return "OK", 200
