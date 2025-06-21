from telegram.ext import ApplicationBuilder, CommandHandler
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

async def start(update, context):
    await update.message.reply_text("Bot aktif, siap menerima perintah!")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("Bot sedang dijalankan...")
    await app.run_polling()

# GANTI INI (hapus baris ini kalau masih ada)
# asyncio.run(main())

# GUNAKAN INI:
import asyncio
asyncio.get_event_loop().run_until_complete(main())
