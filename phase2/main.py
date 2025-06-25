from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os
import asyncio

# Load env
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Flask app
flask_app = Flask(__name__)

# Telegram app
bot_app = Application.builder().token(TOKEN).build()

# Handler /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Bot DJGOLD aktif dan siap digunakan.")

# Register handler
bot_app.add_handler(CommandHandler("start", start))

# Endpoint root
@flask_app.route("/", methods=["GET"])
def index():
    return "Bot DJGOLD aktif via Flask!"

# Webhook endpoint
@flask_app.route("/webhook", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    await bot_app.process_update(update)
    return "OK", 200

# Start Flask + webhook
if __name__ == "__main__":
    bot_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url="https://djgoldbot.onrender.com/webhook"
    )
