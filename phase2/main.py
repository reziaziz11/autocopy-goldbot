# phase2/main.py

from telegram.ext import Application, CommandHandler
import os

# Ganti ini dengan token bot kamu, atau ambil dari environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN", "7524328423:AAGbx7KMgXRzIr9gAmg9I4WznFRmWiXKuNQ")

# Fungsi command awal
async def start(update, context):
    await update.message.reply_text("Hai! Bot aktif 🎉")

# Bangun application (NO Updater, NO legacy mode)
application = Application.builder().token(BOT_TOKEN).build()

# Tambahkan handler seperti biasa
application.add_handler(CommandHandler("start", start))

# Jalankan bot dengan polling (paling mudah dan stabil)
if __name__ == "__main__":
    application.run_polling()
