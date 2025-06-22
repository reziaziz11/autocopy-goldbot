import os
import asyncio
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# === Load .env dan token ===
load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://djgoldbot.onrender.com{WEBHOOK_PATH}"

# === Flask & Bot Setup ===
app = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()

# === Command /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

bot_app.add_handler(CommandHandler("start", start))

# === Web Endpoint untuk cek (optional) ===
@app.route("/")
def home():
    return "DJGOLD BOT AKTIF ✅"

# === Webhook Endpoint ===
@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot_app.bot)
        await bot_app.process_update(update)
        return "OK", 200

# === Jalankan Bot dan Set Webhook ===
async def run():
    await bot_app.initialize()
    await bot_app.bot.set_webhook(url=WEBHOOK_URL)
    await bot_app.start()
    print(f"✅ Webhook aktif di {WEBHOOK_URL}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run())
    app.run(host="0.0.0.0", port=10000)
