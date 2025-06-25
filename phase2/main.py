import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise Exception("BOT_TOKEN belum di-set!")

app = Flask(__name__)
application = Application.builder().token(BOT_TOKEN).build()

# Handler /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif via webhook ✅")

application.add_handler(CommandHandler("start", start))

# Webhook endpoint
@app.route('/webhook', methods=['POST'])
async def handle_webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok"

# Jalankan application saat Flask mulai
@app.before_first_request
def start_bot():
    asyncio.create_task(application.initialize())
