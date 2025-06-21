import os
import asyncio
from dotenv import load_dotenv
from flask import Flask
from threading import Thread
from main import build_bot

load_dotenv()

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = "https://djgoldbot.onrender.com/webhook"

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ DJGOLD Bot is running!'

async def main():
    bot_app = await build_bot()

    # ✅ Jalankan bot dengan webhook_url (bukan webhook_path)
    bot_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=WEBHOOK_URL,
    )

def run():
    asyncio.run(main())

if __name__ == "__main__":
    # ✅ Set webhook manual sebelum bot jalan
    from telegram import Bot
    bot = Bot(token=TOKEN)
    bot.set_webhook(url=WEBHOOK_URL)
    print(f"✅ Webhook telah diset ke: {WEBHOOK_URL}")

    # ✅ Jalankan bot di thread terpisah
    Thread(target=run).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
