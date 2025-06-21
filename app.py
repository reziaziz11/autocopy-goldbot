from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import Update
from telegram.ext import ContextTypes
import os
from dotenv import load_dotenv
import asyncio

# Load token dari .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Handler command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif, siap menerima perintah!")

# Fungsi utama
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot sedang dijalankan...")
    await app.run_polling()

# Eksekusi program
if __name__ == "__main__":
    asyncio.run(main())
