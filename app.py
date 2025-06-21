import os
import asyncio
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler

# === Load .env ===
load_dotenv()
TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", 10000))

# === Validasi Token ===
if not TOKEN or not TOKEN.startswith("7524328423:"):
    raise ValueError("❌ TOKEN tidak valid atau belum di-set! Harap isi variabel lingkungan TOKEN di Render.")

# === Setup Telegram Bot ===
bot_app = ApplicationBuilder().token(TOKEN).build()
bot = Bot(token=TOKEN)

# === Handler /start ===
async def start(update, context):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

bot_app.add_handler(CommandHandler("start", start))

# === Setup Flask (Render butuh endpoint) ===
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    return "Webhook received!", 200

# === Jalankan Webhook Telegram ===
async def main():
    print("✅ Webhook telah diset ke: https://djgoldbot.onrender.com/webhook")
    await bot_app.initialize()
    await bot_app.start()
    await bot_app.updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook",
        webhook_url="https://djgoldbot.onrender.com/webhook"
    )
    await bot_app.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
