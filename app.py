import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
from bot.handlers import start_handler
from dotenv import load_dotenv

# Load token & env
load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PATH = "/webhook"

# Init Flask
app = Flask(__name__)

# Init Telegram App
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start_handler))

# Set webhook manual
def set_webhook():
    application.bot.set_webhook(WEBHOOK_URL)

set_webhook()

@app.route("/", methods=["GET"])
def home():
    return "✅ DJGOLD_BOT aktif!"

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.process_update(update)
    return "OK", 200
