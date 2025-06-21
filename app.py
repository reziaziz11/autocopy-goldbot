import os
import logging
import asyncio
import nest_asyncio
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === Setup dasar ===
load_dotenv()
nest_asyncio.apply()

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Contoh: https://djgoldbot.onrender.com/webhook

app = Flask(__name__)

# === Command Handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

# === Init Telegram Bot ===
bot_app = ApplicationBuilder().token(TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))

# === Flask endpoint untuk Webhook ===
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    asyncio.run(bot_app.process_update(update))
    return "OK"

# === Endpoint root buat test Render ===
@app.route("/", methods=["GET", "HEAD"])
def index():
    return "DJGOLD_BOT Aktif!"

# === Start Flask Server ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
