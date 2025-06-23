import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "djgoldbot123")

# === Telegram Application ===
app = Flask(__name__)
loop = asyncio.get_event_loop()
application = ApplicationBuilder().token(TOKEN).updater(None).build()

# === Command Handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

application.add_handler(CommandHandler("start", start))

# === Webhook Handler ===
@app.post(f"/webhook/{WEBHOOK_SECRET}")
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.update_queue.put(update)
    return "OK", 200

@app.get("/setwebhook")
async def set_webhook():
    url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook/{WEBHOOK_SECRET}"
    await application.bot.set_webhook(url)
    return f"✅ Webhook set to {url}"

@app.get("/")
def index():
    return "DJGOLD BOT is alive"

# === Start the bot ===
async def run():
    await application.initialize()
    await application.start()
    print("✅ Bot started via webhook")

if __name__ == "__main__":
    loop.create_task(run())
    import hypercorn.asyncio
    from hypercorn.config import Config
    config = Config()
    config.bind = ["0.0.0.0:10000"]
    loop.run_until_complete(hypercorn.asyncio.serve(app, config))
