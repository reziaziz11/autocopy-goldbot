import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Aplikasi Flask untuk webhook
app = Flask(__name__)

# Aplikasi Telegram Bot
application = Application.builder().token(BOT_TOKEN).build()


@app.route('/webhook', methods=['POST'])
async def webhook():
    if request.method == "POST":
        data = request.get_json(force=True)
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return 'OK'
    return 'Method Not Allowed', 405


# Command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Bot aktif dan siap jalan via webhook 🚀")


# Tambahkan handler /start
application.add_handler(CommandHandler("start", start))


# Jalankan Flask dan inisialisasi bot Telegram
if __name__ == "__main__":
    import asyncio
    from threading import Thread

    def run_flask():
        app.run(host="0.0.0.0", port=10000)

    # Mulai Flask dalam thread terpisah
    Thread(target=run_flask).start()

    # Jalankan Telegram application tanpa polling
    asyncio.run(application.initialize())
