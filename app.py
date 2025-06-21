import os
from flask import Flask
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
)
import threading
import asyncio

# === Load Env ===
load_dotenv()
TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", 10000))

# === Flask App ===
app_flask = Flask(__name__)

@app_flask.route("/")
def index():
    return "✅ DJGOLD_BOT aktif!"

# === Bot Handler Functions ===
from handlers.start import start_handler
from handlers.callbacks import button_handler  # pastikan file ini ada

# === Jalankan Bot ===
async def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()

    # Tambah handler
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🚀 Bot Telegram dijalankan via polling...")
    await app.run_polling()

# === Main Start ===
if __name__ == "__main__":
    # Jalankan Flask di thread terpisah
    threading.Thread(target=app_flask.run, kwargs={"host": "0.0.0.0", "port": PORT}).start()

    # Jalankan Telegram bot (tanpa asyncio.run)
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    loop.run_forever()
