import os
import asyncio
import logging
from flask import Flask, request
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from threading import Thread

# Load .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "djgoldwebhook")
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook/{WEBHOOK_SECRET}"

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

# Init Flask
app = Flask(__name__)

# Bot command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

# Init Bot Application
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))

# Webhook endpoint
@app.route(f"/webhook/{WEBHOOK_SECRET}", methods=["POST"])
async def webhook_handler():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.update_queue.put(update)
    return "OK", 200

# Bot runner
async def main():
    await application.initialize()
    await application.bot.set_webhook(url=WEBHOOK_URL)
    await application.start()
    logging.info(f"🚀 Bot & webhook aktif di {WEBHOOK_URL}")

# Run bot on separate thread
def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

# Default route
@app.route("/")
def index():
    return "DJGOLD Bot is running."

if __name__ == "__main__":
    Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
