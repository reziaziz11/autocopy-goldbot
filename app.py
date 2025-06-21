import os
import asyncio
from flask import Flask, request
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === Load environment ===
load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://djgoldbot.onrender.com/webhook")

# === Flask app init ===
flask_app = Flask(__name__)

# === Command handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

# === Telegram bot app ===
bot_app = ApplicationBuilder().token(TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))

# === Webhook endpoint ===
@flask_app.route("/webhook", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    await bot_app.update_queue.put(update)
    return "ok", 200

# === Healthcheck ===
@flask_app.route("/", methods=["GET"])
def index():
    return "DJGOLD_BOT Webhook Active ✅", 200

# === Async main setup ===
async def main():
    await bot_app.initialize()
    await bot_app.start()
    await bot_app.bot.set_webhook(url=WEBHOOK_URL)
    print(f"✅ Webhook di-set ke: {WEBHOOK_URL}")
    print("🚀 Bot siap menerima update dari Telegram")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        # Untuk Python 3.11+ default di Render
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())

    # Jalankan Flask server
    flask_app.run(host="0.0.0.0", port=10000)
