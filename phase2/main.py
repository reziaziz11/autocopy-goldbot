import os
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Load token dari .env / render environment
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Cek apakah token valid
if not TOKEN:
    raise Exception("❌ TOKEN Telegram tidak ditemukan. Cek .env atau Render Environment.")

# Inisialisasi Flask dan Telegram bot
app = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()

# Command handler contoh
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Bot aktif sukses!")

bot_app.add_handler(CommandHandler("start", start))

# Endpoint webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    bot_app.update_queue.put(update)
    return "OK"

# Run bot
if __name__ == "__main__":
    bot_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=os.getenv("WEBHOOK_URL")  # Jangan lupa set ini juga di Render
    )
