import os
import logging
import nest_asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# === Load ENV ===
load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # ex: https://djgoldbot.onrender.com

# === Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Flask ===
app = Flask(__name__)
nest_asyncio.apply()

# === Telegram Bot ===
bot_app = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

bot_app.add_handler(CommandHandler("start", start))

# === Webhook Endpoint ===
@app.post("/webhook")
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return "OK", 200

# === Root Endpoint ===
@app.get("/")
def home():
    return "✅ DJGOLD BOT AKTIF"

# === Jalankan Bot + Flask ===
if __name__ == "__main__":
    import asyncio

    async def main():
        await bot_app.initialize()
        await bot_app.start()
        await bot_app.set_webhook(WEBHOOK_URL + "/webhook")
        logger.info("🚀 Webhook berhasil di-SET")

    asyncio.get_event_loop().create_task(main())
    app.run(host="0.0.0.0", port=10000)
