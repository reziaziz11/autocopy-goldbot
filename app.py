import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
from dotenv import load_dotenv
import nest_asyncio
import asyncio

load_dotenv()
TOKEN = os.getenv("TOKEN")

# Logging supaya error kelihatan
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
nest_asyncio.apply()

bot_app = ApplicationBuilder().token(TOKEN).build()

# Handler /start
async def start(update: Update, context):
    try:
        chat_id = update.effective_chat.id
        logger.info(f"📬 Handler /start dipanggil — chat_id: {chat_id}")
        await update.message.reply_text("✅ Bot aktif dan siap digunakan!")
    except Exception as e:
        logger.error(f"❌ Gagal handle /start: {e}")

bot_app.add_handler(CommandHandler("start", start))

# Endpoint webhook
@app.route("/webhook", methods=["POST"])
async def webhook():
    try:
        payload = request.get_json(force=True)
        logger.info(f"👉 Dapat payload dari Telegram: {payload}")
        update = Update.de_json(payload, bot_app.bot)
        await bot_app.process_update(update)
    except Exception as e:
        logger.error(f"❌ Gagal proses webhook: {e}")
    return "OK", 200

if __name__ == "__main__":
    logger.info("🚀 Bot dan Flask server mulai jalan...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
