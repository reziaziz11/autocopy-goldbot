import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === Langsung pakai token (sementara, bypass .env)
TOKEN = "7524328423:AAGbx7KMgXRzIr9gAmg91aWznFRmiXKuNQ"
WEBHOOK_URL = "https://djgoldbot.onrender.com/webhook"

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
    await bot_app.update_queue.put(Update.de_json(request.get_json(force=True), bot_app.bot))
    return "ok", 200

# === Healthcheck ===
@flask_app.route("/", methods=["GET"])
def index():
    return "DJGOLD_BOT Webhook Active ✅", 200

# === Async main setup ===
async def main():
    await bot_app.bot.set_webhook(url=WEBHOOK_URL)
    print(f"✅ Webhook set ke: {WEBHOOK_URL}")
    await bot_app.initialize()
    await bot_app.start()
    await bot_app.updater.start_polling()
    print("🚀 Bot polling aktif...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())

    # Jalankan Flask server
    flask_app.run(host="0.0.0.0", port=10000)
