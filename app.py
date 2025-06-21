import os
import asyncio
from dotenv import load_dotenv
from flask import Flask, request
from main import build_bot

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = Flask(__name__)

@app.route('/')
def index():
    return "DJGOLD_BOT Aktif", 200

@app.route('/webhook', methods=['POST'])
async def webhook():
    if request.method == "POST":
        await bot_app.update_queue.put(request.json)
        return "OK", 200

async def main():
    global bot_app
    bot_app = await build_bot()
    await bot_app.bot.set_webhook(url=WEBHOOK_URL)
    print(f"✅ Webhook telah diset ke: {WEBHOOK_URL}")
    bot_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_path="/webhook",
    )

if __name__ == "__main__":
    asyncio.run(main())
