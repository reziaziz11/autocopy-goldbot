import os
import asyncio
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from handlers.start import start
from handlers.callbacks import button_handler

# === Load Token dari .env ===
load_dotenv()
TOKEN = os.getenv("TOKEN")

# === Inisialisasi Flask ===
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "DJGOLD_BOT Aktif 🔥"

# === Fungsi untuk menjalankan Flask di thread lain ===
def run_flask():
    flask_app.run(host="0.0.0.0", port=10000)

# === Fungsi utama untuk menjalankan bot ===
async def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()

    # === Tambahkan Handler di sini ===
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))  # << Ini penting

    # === Jalankan polling ===
    await app.initialize()
    await app.start()
    print("🚀 Bot Telegram dijalankan via polling...")
    await app.run_polling()

# === Jalankan Flask dan Bot secara bersamaan ===
if __name__ == "__main__":
    # Jalankan Flask di thread terpisah
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Jalankan Bot di thread utama (asyncio)
    asyncio.run(run_bot())
