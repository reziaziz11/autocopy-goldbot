import os, asyncio, logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from threading import Thread

load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "djgoldwebhook")
HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
WEBHOOK_URL = f"https://{HOSTNAME}/webhook/{WEBHOOK_SECRET}"

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Received /start from chat_id=%s", update.effective_chat.id)
    await update.message.reply_text(
        "✅ Bot aktif dan siap menerima perintah!\n"
        "Gunakan /daftar untuk mulai."
    )

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))

@app.route(f"/webhook/{WEBHOOK_SECRET}", methods=["POST"])
def webhook_handler():
    data = request.get_json(force=True)
    logging.info("Incoming webhook payload: %s", data)
    update = Update.de_json(data, application.bot)
    application.update_queue.put_nowait(update)
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "DJGOLD Bot is running", 200

def run_webhook_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(application.initialize())
    loop.run_until_complete(application.bot.set_webhook(WEBHOOK_URL))
    logging.info("🤖 Webhook set to %s", WEBHOOK_URL)
    loop.run_until_complete(application.start())
    loop.run_forever()

if __name__ == "__main__":
    Thread(target=run_webhook_bot, daemon=True).start()
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
