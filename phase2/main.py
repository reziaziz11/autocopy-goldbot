import os
from telegram.ext import Application
from handlers.registration import registration_conversation_handler
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = Flask(__name__)

bot_app = Application.builder().token(TOKEN).build()
bot_app.add_handler(registration_conversation_handler)

@app.route('/webhook', methods=['POST'])
async def webhook():
    await bot_app.update_queue.put(
        bot_app.update_queue._application._parse_webhook_data(await request.get_data())
    )
    return 'OK'

@app.route('/')
def index():
    return 'DJGOLD_BOT webhook is active!'

if __name__ == '__main__':
    import asyncio
    bot_app.run_webhook(
        listen='0.0.0.0',
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=f"{WEBHOOK_URL}/webhook"
    )
