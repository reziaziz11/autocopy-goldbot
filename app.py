import os
import asyncio
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import nest_asyncio

# Setup
nest_asyncio.apply()
load_dotenv()

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Inisialisasi Telegram bot
application = ApplicationBuilder().token(TOKEN).build()

# Handler /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

application.add_handler(CommandHandler("start", start))

# Set Webhook
async def set_webhook():
    await application.bot.set_webhook(WEBHOOK_URL)

asyncio.get_event_loop().run_until_complete(set_webhook())

# Flask App (Wajib pakai nama "app" untuk Render/gunicorn)
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Bot is running..."

@app.route("/webhook", methods=["POST"])
async def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), application.bot)
        await application.process_update(update)
        return "OK", 200
