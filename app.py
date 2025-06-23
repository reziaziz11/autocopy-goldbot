import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

from bot.handlers import start_handler

app = Flask(__name__)

TOKEN = os.getenv("TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Setup Bot
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start_handler))
application.initialize()  # jangan lupa initialize

# Set webhook saat startup
@app.before_first_request
def set_webhook():
    application.bot.set_webhook(WEBHOOK_URL)

@app.route("/", methods=["GET"])
def home():
    return "✅ DJGOLD_BOT is running!"

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.process_update(update)  # sync processing
    return "OK", 200

if __name__ == "__main__":
    app.run()
