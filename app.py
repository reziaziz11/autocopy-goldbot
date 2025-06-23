import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from stage2.welcome import start_handler  # Tahap 2 import

app = Flask(__name__)

# === Setup Bot ===
TOKEN = os.getenv("TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # misalnya https://djgoldbot.onrender.com/webhook

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start_handler))

@app.route("/", methods=["GET"])
def home():
    return "✅ DJGOLD_BOT is running!"

@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        await application.initialize()  # WAJIB agar bisa proses update
        await application.process_update(update)
        return "OK", 200
