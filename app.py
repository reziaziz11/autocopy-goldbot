from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import Update
from telegram.ext import ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

# Handler untuk perintah /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif, siap menerima perintah!")

# Eksekusi aplikasi langsung tanpa asyncio.run()
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("Bot sedang dijalankan...")
    app.run_polling()  # ⚠️ Ini sinkron, tidak perlu async/await

if __name__ == "__main__":
    main()
