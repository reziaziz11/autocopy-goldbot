import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes
from telegram.ext import filters
from dotenv import load_dotenv
from handlers import start, handle_message

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

bot_app = Application.builder().token(TOKEN).build()

# Register command and message handlers
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Webhook endpoint
@app.route('/webhook', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    await bot_app.process_update(update)
    return 'OK', 200

# Health check
@app.route('/', methods=['GET'])
def home():
    return 'DJGOLD_BOT is alive ✅'

if __name__ == '__main__':
    bot_app.run_polling()  # won't be called on Render, but for local test
