import os
import logging
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# === Load environment ===
load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")
PORT = int(os.getenv("PORT", 10000))

# === Logger ===
logging.basicConfig(level=logging.INFO)

# === Flask App ===
app = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()

# === Command Handler ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan merespons!")

# === Register handler ke bot ===
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(MessageHandler(filters.TEXT, start))  # Default fallback sementara

# === Flask endpoint untuk webhook ===
@app.route(WEBHOOK_PATH, methods=["POST"])
async def telegram_webhook():
    if request.method == "POST":
        await bot_app.update_queue.put(Update.de_json(request.get_json(force=True), bot_app.bot))
        return "ok"
    return "Method Not Allowed", 405

# === Start webhook manual di dalam Flask ===
async def main():
    await bot_app.initialize()
    await bot_app.start()
    await bot_app.bot.set_webhook(url=f"https://djgoldbot.onrender.com{WEBHOOK_PATH}")
    print("🚀 Bot siap menerima webhook!")

# === Jalankan Flask + Webhook secara bersamaan ===
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    app.run(host="0.0.0.0", port=PORT)
