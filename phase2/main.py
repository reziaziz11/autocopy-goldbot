import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

# Buat aplikasi Telegram bot
application = Application.builder().token(BOT_TOKEN).build()

# Handler command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Bot DJGOLD aktif via webhook ✅")

application.add_handler(CommandHandler("start", start))

# Endpoint webhook
@app.route('/webhook', methods=["POST"])
async def telegram_webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "OK"

# Flask app agar dikenali Gunicorn
app.wsgi_app = app

# Jangan lupa initialize bot saat start
@app.before_first_request
def init_telegram():
    import asyncio
    asyncio.create_task(application.initialize())
