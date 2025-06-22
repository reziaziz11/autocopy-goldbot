import os
import asyncio
import nest_asyncio
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

nest_asyncio.apply()
load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://djgoldbot.onrender.com{WEBHOOK_PATH}"

app = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()

# Handler /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📬 Handler /start dipanggil—chat_id:", update.effective_chat.id)
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

bot_app.add_handler(CommandHandler("start", start))

@app.route("/")
def index():
    return "✅ DJGOLD BOT AKTIF"

@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    payload = request.get_json(force=True)
    print("👉 Update diterima di Webhook:", payload)
    update = Update.de_json(payload, bot_app.bot)
    await bot_app.process_update(update)
    return "OK", 200

async def main():
    print("🚀 Inisialisasi Bot & Webhook...")
    await bot_app.initialize()
    await bot_app.bot.set_webhook(url=WEBHOOK_URL)
    print(f"✅ Webhook telah diset: {WEBHOOK_URL}")
    await bot_app.start()
    print("✅ Bot App berjalan")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    app.run(host="0.0.0.0", port=10000)
