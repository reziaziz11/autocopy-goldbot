import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "djgoldbot123")
RENDER_HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME", "localhost")

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# === Telegram Bot Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

application.add_handler(CommandHandler("start", start))

@app.route("/")
def home():
    return "DJGOLD BOT is running"

@app.route(f"/webhook/{WEBHOOK_SECRET}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return "ok"

@app.route("/setwebhook")
async def set_webhook():
    webhook_url = f"https://{RENDER_HOST}/webhook/{WEBHOOK_SECRET}"
    await application.bot.set_webhook(webhook_url)
    return f"✅ Webhook set to: {webhook_url}"

async def run():
    await application.initialize()
    await application.start()
    # Jangan stop application di sini
    import hypercorn.asyncio
    from hypercorn.config import Config

    config = Config()
    config.bind = ["0.0.0.0:10000"]
    await hypercorn.asyncio.serve(app, config)

if __name__ == "__main__":
    asyncio.run(run())
