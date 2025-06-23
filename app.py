import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import Dispatcher

from dotenv import load_dotenv
load_dotenv()

# === Konfigurasi Token & Webhook ===
TOKEN = os.getenv("TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "secret")
WEBHOOK_PATH = f"/webhook/{WEBHOOK_SECRET}"
BASE_URL = os.getenv("BASE_URL")  # contoh: https://djgoldbot.onrender.com

# === Setup Logging ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# === Flask App ===
app = Flask(__name__)
bot_app = ApplicationBuilder().token(TOKEN).build()

# === Handler Bot ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

bot_app.add_handler(CommandHandler("start", start))


# === Webhook Route ===
@app.post(WEBHOOK_PATH)
async def webhook():
    if request.headers.get("content-type") == "application/json":
        update = Update.de_json(request.get_json(force=True), bot_app.bot)
        await bot_app.process_update(update)
        return "OK"
    return "Invalid content type", 400


# === Endpoint utama (cek status bot) ===
@app.get("/")
def index():
    return "DJGOLD BOT Aktif ✅"


# === Auto Set Webhook saat bot start ===
async def set_webhook():
    url = f"{BASE_URL}{WEBHOOK_PATH}"
    webhook_set = await bot_app.bot.set_webhook(url)
    if webhook_set:
        logging.info(f"Webhook set to {url}")
    else:
        logging.warning("❌ Gagal set webhook")


# === Jalankan bot (background) ===
async def run_bot():
    await set_webhook()
    await bot_app.initialize()
    await bot_app.start()
    logging.info("🤖 Bot Telegram sudah berjalan...")

# === Jalankan background saat server aktif ===
@app.before_serving
async def startup():
    await run_bot()

@app.after_serving
async def shutdown():
    await bot_app.stop()
    await bot_app.shutdown()
