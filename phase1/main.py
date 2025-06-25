from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler

TOKEN = "7524328423:AAFPrLxZtxnyyGmmguhc5KU_e524xnq4thI"
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)

# Handler
def start(update, context):
    update.message.reply_text("Bot aktif!")

dispatcher.add_handler(CommandHandler("start", start))

# Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return 'Bot aktif di root'

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'OK'

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
