import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)
from dotenv import load_dotenv
import asyncio

load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "djgoldbot123")

app = Flask(__name__)
loop = asyncio.get_event_loop()
application = ApplicationBuilder().token(TOKEN).build()

# === Handler Bot ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

application.add_handler(CommandHandler("start", start))

# === Webhook route ===
@app.route(f"/webhook/{WEBHOOK_SECRET}", methods=["POST"])
async def webhook_handler():
    if request.method == "POST":
        await application.update_queue.put(Update.de_json(request.get_json(force=True), application.bot))
        return "OK", 200

# === Manual webhook trigger route ===
@app.route("/setwebhook")
async def set_webhook():
    url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook/{WEBHOOK_SECRET}"
    await application.bot.set_webhook(url=url)
    return f"✅ Webhook set to: {url}"

@app.route("/")
def index():
    return "DJGOLD BOT is alive"

# === Start bot background loop ===
async def startup():
    await application.initialize()
    await application.start()
loop.create_task(startup())

# === Run Flask ===
if __name__ == "__main__":
    app.run()
