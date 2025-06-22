import os
import logging
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import nest_asyncio
import asyncio

# === Init Logging & Env ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

TOKEN = os.getenv("TOKEN")
app = Flask(__name__)
bot_app = ApplicationBuilder().token(TOKEN).build()

# === Handler /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap digunakan!")

bot_app.add_handler(CommandHandler("start", start))

# === Webhook Route ===
@app.post("/webhook")
async def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, bot_app.bot)
        await bot_app.update_queue.put(update)
        return "ok", 200
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return "error", 500

# === Start App ===
if __name__ == "__main__":
    nest_asyncio.apply()
    logger.info("🚀 Bot dan Flask server mulai jalan...")
    asyncio.get_event_loop().run_until_complete(bot_app.initialize())
    app.run(host="0.0.0.0", port=10000)
