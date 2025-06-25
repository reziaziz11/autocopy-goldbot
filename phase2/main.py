import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN belum di-set")

app = Flask(__name__)
application = Application.builder().token(BOT_TOKEN).build()

# Handler /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif via webhook ✅")

application.add_handler(CommandHandler("start", start))

# Endpoint untuk menerima webhook
@app.route('/webhook', methods=['POST'])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok"

# Inisialisasi bot saat pertama kali jalan
@app.before_first_request
def activate_bot():
    asyncio.create_task(application.initialize())
