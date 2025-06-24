import os, asyncio, logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from threading import Thread

load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "djgoldwebhook")
HOST = os.getenv('RENDER_EXTERNAL_HOSTNAME')
WEBHOOK_URL = f"https://{HOST}/webhook/{WEBHOOK_SECRET}"

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)

# handler /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📝 Daftar"]]
    await update.message.reply_text("Selamat datang! Tekan tombol atau ketik /daftar", reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))

# handler /daftar
async def daftar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(f"Silakan isi form pendaftaran, @{user.username} 🚀")

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("daftar", daftar))

@app.route(f"/webhook/{WEBHOOK_SECRET}", methods=["POST"])
def webhook_handler():
    payload = request.get_json(force=True)
    update = Update.de_json(payload, application.bot)
    application.update_queue.put_nowait(update)
    return jsonify({"status": "ok"}), 200

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(application.initialize())
    loop.run_until_complete(application.bot.set_webhook(WEBHOOK_URL))
    logging.info("🔌 Webhook set to: %s", WEBHOOK_URL)
    loop.run_forever()

if __name__ == "__main__":
    Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
