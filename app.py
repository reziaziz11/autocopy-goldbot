import os
import asyncio
import logging
from flask import Flask, request
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "djgoldwebhook")
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook/{WEBHOOK_SECRET}"

# Logging aktif
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

# Init Flask
app = Flask(__name__)

# Handler /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

# Init aplikasi Telegram
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))

# Webhook endpoint
@app.route(f"/webhook/{WEBHOOK_SECRET}", methods=["POST"])
async def webhook_handler():
    logging.debug("🔔 Webhook HIT! Incoming JSON: %s", request.get_json())
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.update_queue.put(update)
    return "OK", 200

# Jalankan bot dan webhook
async def main():
    await application.initialize()
    await application.bot.set_webhook(url=WEBHOOK_URL)
    await application.start()
    logging.info("🚀 Bot & webhook aktif di %s", WEBHOOK_URL)

# Start Flask + Bot
@app.before_first_request
def activate_bot():
    asyncio.get_event_loop().create_task(main())

@app.route("/")
def index():
    return "DJGOLD Bot Aktif!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
