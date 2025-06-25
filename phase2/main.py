from telegram.ext import Application
from handlers.registration import get_registration_handler
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot_app = Application.builder().token(TOKEN).build()

# Tambahkan handler form pendaftaran
bot_app.add_handler(get_registration_handler())

if __name__ == '__main__':
    bot_app.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url="https://djgoldbot.onrender.com/webhook"
    )
