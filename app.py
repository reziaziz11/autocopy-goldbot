import os
from flask import Flask, request
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler
from stage2.welcome import welcome_handler

load_dotenv()
TOKEN = os.getenv("TOKEN")

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()
application.add_handler(welcome_handler)

@app.route('/')
def index():
    return "✅ DJGOLD_BOT aktif"

@app.route('/webhook', methods=['POST'])
async def webhook():
    if request.method == 'POST':
        update = Update.de_json(request.get_json(force=True), application.bot)
        await application.process_update(update)
        return 'ok'
