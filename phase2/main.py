import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from handlers.registration import registration_conversation_handler
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 5000))

bot_app = Application.builder().token(TOKEN).build()

# Tambahkan handler pendaftaran (form interaktif Phase 2)
bot_app.add_handler(registration_conversation_handler)

# Webhook Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Bot is running!'

@app.route('/webhook', methods=['POST'])
def webhook():
    update = bot_app.bot._extract_update(request.get_json(force=True), bot_app.bot)
    bot_app.update_queue.put(update)
    return 'OK'

if __name__ == '__main__':
    bot_app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=os.getenv("WEBHOOK_URL"),
        allowed_updates=bot_app.allowed_updates,
    )
