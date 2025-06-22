# app.py

import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.ext import Dispatcher, CallbackContext
from telegram.ext.webhookhandler import WebhookHandler
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # ex: https://djgoldbot.onrender.com/webhook

app = Flask(__name__)

# Logger (penting buat debugging)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ DJGOLD_BOT aktif dan siap menerima perintah!")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Perintah tidak dikenali.")

# === Setup Bot Telegram ===
application = ApplicationBuilder().token(TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.COMMAND, unknown))

# === Flask route ===
@app.route("/", methods=["GET"])
def home():
    return "✅ Bot aktif di server", 200

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    """Handle webhook from Telegram"""
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        application.update_queue.put_nowait(update)
        return "OK", 200
    return "Method Not Allowed", 405

# === Webhook Setup (Run once) ===
@app.before_first_request
def setup_webhook():
    from telegram import Bot
    bot = Bot(token=TOKEN)
    bot.set_webhook(f"{WEBHOOK_URL}{WEBHOOK_PATH}")
    logger.info(f"Webhook disetel ke {WEBHOOK_URL}{WEBHOOK_PATH}")
