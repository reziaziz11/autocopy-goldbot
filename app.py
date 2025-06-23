import os
import asyncio
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application, ApplicationBuilder, CommandHandler, ContextTypes
)
import nest_asyncio

nest_asyncio.apply()
load_dotenv()

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Inisialisasi Telegram bot
app_telegram = ApplicationBuilder().token(TOKEN).build()

# Handler /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

app_telegram.add_handler(CommandHandler("start", start))

# Setup Flask
flask_app = Flask(__name__)

@flask_app.get("/")
def index():
    return "DJGOLD_BOT aktif..."

@flask_app.post("/webhook")
async def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), app_telegram.bot)
    await app_telegram.process_update(update)
    return "OK", 200

# Setup dan jalankan Webhook dengan cara async
async def main():
    await app_telegram.bot.set_webhook(WEBHOOK_URL)
    print(f"✅ Webhook berhasil diset ke: {WEBHOOK_URL}")

if __name__ == "__main__":
    asyncio.run(main())
    flask_app.run(port=10000)
