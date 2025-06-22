import os
import asyncio
import nest_asyncio
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# === Setup dasar ===
nest_asyncio.apply()
load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://djgoldbot.onrender.com{WEBHOOK_PATH}"

# === Inisialisasi Flask dan Bot ===
app = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()

# === Handler command /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

bot_app.add_handler(CommandHandler("start", start))

# === Endpoint test ===
@app.route("/")
def index():
    return "✅ DJGOLD BOT AKTIF"

# === Endpoint webhook ===
@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    await bot_app.process_update(update)
    return "OK", 200

# === Fungsi untuk set webhook dan mulai bot ===
async def main():
    await bot_app.initialize()
    await bot_app.bot.set_webhook(url=WEBHOOK_URL)
    await bot_app.start()  # PENTING: WAJIB agar bot bisa merespons
    print(f"✅ Webhook aktif di: {WEBHOOK_URL}")

# === Jalankan Flask + bot bersamaan ===
if __name__ == "__main__":
    asyncio.get_event_loop().create_task(main())
    app.run(host="0.0.0.0", port=10000)
