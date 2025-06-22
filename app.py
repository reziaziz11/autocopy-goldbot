import os
import logging
from flask import Flask, request
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
)
import asyncio

load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_PATH = "/webhook"

app = Flask(__name__)

# Bot init
bot_app = ApplicationBuilder().token(TOKEN).build()

# Handler /start
async def start(update: Update, context):
    print("📬 Handler /start dipanggil — chat_id:", update.effective_chat.id)
    await update.message.reply_text("✅ Bot aktif dan siap digunakan!")

bot_app.add_handler(CommandHandler("start", start))

# Webhook endpoint
@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    payload = request.get_json(force=True)
    print("👉 Dapat payload dari Telegram:", payload)
    update = Update.de_json(payload, bot_app.bot)
    await bot_app.process_update(update)
    return "OK", 200

# Run Flask server
if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    print("🚀 Starting Flask app + Telegram bot...")
    bot_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_path=WEBHOOK_PATH,
    )
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
