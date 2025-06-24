import os, asyncio, logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from threading import Thread

load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "djgoldwebhook")
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook/{WEBHOOK_SECRET}"

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))

@app.route(f"/webhook/{WEBHOOK_SECRET}", methods=["POST"])
def webhook_handler():
    try:
        payload = request.get_json(force=True)
        update = Update.de_json(payload, application.bot)
        application.update_queue.put_nowait(update)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        logging.exception("Error in webhook")
        return jsonify({"error": "internal server error"}), 500

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(application.initialize())
    loop.run_until_complete(application.bot.set_webhook(WEBHOOK_URL))
    loop.run_until_complete(application.start())
    logging.info("🚀 Bot & webhook aktif di %s", WEBHOOK_URL)
    loop.run_forever()

@app.route("/")
def index():
    return "DJGOLD Bot is running."

if __name__ == "__main__":
    Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
