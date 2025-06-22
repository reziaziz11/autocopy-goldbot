import os
import logging
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === Load Token dan Init ===
load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_PATH = "/webhook"
app = Flask(__name__)

# === Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Bot Setup ===
bot_app = ApplicationBuilder().token(TOKEN).build()

# === Command Handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap digunakan!")

bot_app.add_handler(CommandHandler("start", start))

# === Webhook Endpoint ===
@app.post(WEBHOOK_PATH)
async def telegram_webhook():
    """Endpoint utama yang diakses Telegram saat kirim update"""
    try:
        update = Update.de_json(request.get_json(force=True), bot_app.bot)
        await bot_app.update_queue.put(update)
        return "ok"
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return "error", 500

# === Start Flask Server ===
if __name__ == "__main__":
    import nest_asyncio
    import asyncio
    nest_asyncio.apply()
    logger.info("🚀 Bot dan Flask server mulai jalan...")
    asyncio.get_event_loop().run_until_complete(bot_app.initialize())
    app.run(host="0.0.0.0", port=10000)
