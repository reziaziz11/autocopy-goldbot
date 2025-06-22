import os
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

TOKEN = os.getenv("TOKEN")
WEBHOOK_PATH = f"/webhook"
BOT_URL = os.getenv("BOT_URL")  # contoh: https://djgoldbot.onrender.com

# === Inisialisasi Flask ===
flask_app = Flask(__name__)

# === Inisialisasi Telegram Bot ===
application = Application.builder().token(TOKEN).build()

# === Command Handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

application.add_handler(CommandHandler("start", start))

# === Route Webhook ===
@flask_app.post(WEBHOOK_PATH)
async def webhook_handler():
    if request.method == "POST":
        await application.update_queue.put(Update.de_json(request.get_json(force=True), application.bot))
        return "OK"
    return "Invalid method", 405

# === WSGI untuk Gunicorn ===
app = flask_app

# === Set Webhook saat start ===
import asyncio
async def set_webhook():
    url = f"{BOT_URL}{WEBHOOK_PATH}"
    await application.bot.set_webhook(url)
    print(f"✅ Webhook set ke: {url}")

asyncio.get_event_loop().run_until_complete(set_webhook())
