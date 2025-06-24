import os, asyncio, logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from threading import Thread

# Load ENV
load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "djgoldwebhook")
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook/{WEBHOOK_SECRET}"

# Logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

# Flask App
app = Flask(__name__)

# Telegram Bot
application = ApplicationBuilder().token(TOKEN).build()

# Bot Command Handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

application.add_handler(CommandHandler("start", start))

# Webhook Handler - ASYNC FIXED
@app.route(f"/webhook/{WEBHOOK_SECRET}", methods=["POST"])
async def webhook_handler():
    try:
        payload = await request.get_json(force=True)
        logging.debug(f"📥 Incoming update: {payload}")
        update = Update.de_json(payload, application.bot)
        await application.update_queue.put(update)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        logging.exception("❌ Error in webhook_handler:")
        return jsonify({"error": str(e)}), 500

# Index route
@app.route("/")
def index():
    return "DJGOLD Bot is running."

# Bot Runner
def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(application.initialize())
    loop.run_until_complete(application.bot.set_webhook(WEBHOOK_URL))
    loop.run_until_complete(application.start())
    logging.info("🚀 Bot & webhook aktif di %s", WEBHOOK_URL)
    loop.run_forever()

# Start server
if __name__ == "__main__":
    Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
