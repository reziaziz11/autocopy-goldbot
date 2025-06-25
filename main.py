from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import asyncio
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = Flask(__name__)
application = Application.builder().token(BOT_TOKEN).build()

# Handler /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        user = update.effective_user
        keyboard = [
            [InlineKeyboardButton("📥 Daftar Akun MT5", callback_data="daftar")],
            [InlineKeyboardButton("💳 Bayar Membership", callback_data="bayar")],
            [InlineKeyboardButton("📊 Cek Status", callback_data="status")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"👋 Selamat datang, {user.first_name}!\n\n"
            "🔰 Ini adalah *DJ GOLD Sync Bot*, sistem copy trade otomatis XAUUSD.\n\n"
            "Silakan pilih menu di bawah untuk mulai:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

# Endpoint webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)
        asyncio.run(application.process_update(update))
    except Exception as e:
        print("❌ Error di /webhook:", e)
        return f"Error: {e}", 500
    return "OK"

# Tambahkan handler setelah Application dibuat
application.add_handler(CommandHandler("start", start))

# Set webhook saat mulai
if __name__ == "__main__":
    def run_webhook():
        asyncio.run(application.bot.set_webhook(WEBHOOK_URL))

    threading.Thread(target=run_webhook).start()
    app.run(host="0.0.0.0", port=10000)
