import os
import asyncio
from flask import Flask, request
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import nest_asyncio

# Load environment
load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://djgoldbot.onrender.com")
PORT = int(os.getenv("PORT", 10000))

# Inisialisasi Flask
app = Flask(__name__)
nest_asyncio.apply()

# Handler untuk command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

# Route untuk webhook
@app.route("/webhook", methods=["POST"])
async def webhook():
    if request.method == "POST":
        await bot_app.update_queue.put(Update.de_json(request.get_json(force=True), bot_app.bot))
        return "OK", 200

# Fungsi utama bot
async def main():
    global bot_app
    bot_app = Application.builder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))

    await bot_app.initialize()
    await bot_app.bot.set_webhook(f"{WEBHOOK_URL}/webhook")

    print(f"✅ Webhook telah diset ke: {WEBHOOK_URL}/webhook")
    await bot_app.start()
    await bot_app.updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="/webhook",
        webhook_url=f"{WEBHOOK_URL}/webhook",
    )
    await bot_app.updater.wait()

# Menjalankan bot di event loop
if __name__ == "__main__":
    asyncio.run(main())
