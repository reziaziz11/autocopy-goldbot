import os
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
import nest_asyncio
import asyncio

# === Setup ===
nest_asyncio.apply()
load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://djgoldbot.onrender.com{WEBHOOK_PATH}"

app = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()

# === Handler /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

bot_app.add_handler(CommandHandler("start", start))

# === Flask route untuk tes ===
@app.route("/")
def home():
    return "DJGOLD BOT AKTIF ✅"

# === Flask route webhook ===
@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    await bot_app.process_update(update)
    return "OK", 200

# === Jalankan Webhook dan Bot ===
async def main():
    await bot_app.initialize()
    await bot_app.bot.set_webhook(url=WEBHOOK_URL)
    await bot_app.start()  # Ini yang buat bot bisa kirim balasan
    print(f"✅ Webhook aktif: {WEBHOOK_URL}")

if __name__ == "__main__":
    asyncio.get_event_loop().create_task(main())
    app.run(host="0.0.0.0", port=10000)
