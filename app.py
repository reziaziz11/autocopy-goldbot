import os
from dotenv import load_dotenv
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler
import asyncio

# === Load Token ===
load_dotenv()
TOKEN = os.getenv("TOKEN")

# === Flask App ===
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "✅ DJGOLD_BOT is running!"

# === Bot Handler ===
async def start(update, context):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

async def telegram_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    # Jangan pakai `await app.run_polling()` karena dia blocking loop

def run_bot():
    asyncio.run(telegram_bot())

# === Jalankan Flask dan Bot Secara Paralel ===
if __name__ == "__main__":
    Thread(target=run_bot).start()
    flask_app.run(host="0.0.0.0", port=10000)
