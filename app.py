import os, logging
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from threading import Thread

# === Load Config ===
load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "djgoldwebhook")
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook/{WEBHOOK_SECRET}"

# === Logging ===
logging.basicConfig(level=logging.INFO)

# === Flask App ===
app = Flask(__name__)

# === Bot Handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

# === Bot Setup ===
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))

# === Webhook Endpoint ===
@app.route(f"/webhook/{WEBHOOK_SECRET}", methods=["POST"])
async def webhook_handler():
    try:
        payload = await request.get_json()
        update = Update.de_json(payload, application.bot)
        await application.update_queue.put(update)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        logging.exception("Webhook error")
        return jsonify({"error": str(e)}), 500

# === Index Page ===
@app.route("/")
def index():
    return "✅ DJGOLD Bot is running."

# === Run Bot in Thread ===
async def start_bot():
    await application.initialize()
    await application.bot.set_webhook(WEBHOOK_URL)
    await application.start()
    logging.info(f"🚀 Bot & webhook aktif di {WEBHOOK_URL}")
    await application.updater.start_polling()  # untuk jaga-jaga

def run_bot():
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot())
    loop.run_forever()

# === Start Everything ===
if __name__ == "__main__":
    Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
