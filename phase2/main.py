import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Flask(__name__)

application = Application.builder().token(BOT_TOKEN).build()


@app.route("/webhook", methods=["POST"])
async def webhook():
    if request.method == "POST":
        data = request.get_json(force=True)
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return "ok"
    return "method not allowed", 405


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif! 🚀")


application.add_handler(CommandHandler("start", start))


if __name__ == "__main__":
    import asyncio

    # Jalankan Flask server
    from threading import Thread

    def run_flask():
        app.run(host="0.0.0.0", port=10000)

    # Jalankan aplikasi Telegram dalam mode async (tanpa polling!)
    Thread(target=run_flask).start()
    asyncio.run(application.initialize())
    print("Bot Telegram siap menerima webhook.")
