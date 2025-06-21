import os
import asyncio
from flask import Flask, request
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === Load environment variables ===
load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://djgoldbot.onrender.com/webhook")

# === Init Flask App ===
flask_app = Flask(__name__)

# === Command Handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

# === Telegram Bot Setup ===
bot_app = ApplicationBuilder().token(TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))

# === Webhook endpoint ===
@flask_app.route("/webhook", methods=["POST"])
async def webhook():
    if request.method == "POST":
        await bot_app.update_queue.put(Update.de_json(request.get_json(force=True), bot_app.bot))
        return "ok", 200

# === Health Check (optional) ===
@flask_app.route("/", methods=["GET"])
def index():
    return "DJGOLD_BOT Webhook Active ✅", 200

# === Main Async Runner ===
async def main():
    # Set webhook to Telegram
    await bot_app.bot.set_webhook(url=WEBHOOK_URL)
    print(f"Webhook set to: {WEBHOOK_URL}")
    # Run polling background queue
    await bot_app.initialize()
    await bot_app.start()
    await bot_app.updater.start_polling()  # needed to process update_queue
    print("Bot polling started.")

if __name__ == "__main__":
    # Jalankan async loop untuk bot Telegram
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    # Jalankan Flask server
    flask_app.run(host="0.0.0.0", port=10000)
