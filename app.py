import os
import logging
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()

TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Logging
logging.basicConfig(level=logging.INFO)

# === BOT SETUP ===
app_bot = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

app_bot.add_handler(CommandHandler("start", start))

# === FLASK SETUP ===
app = Flask(__name__)

@app.route('/')
def home():
    return "DJGOLD BOT AKTIF ✅"

@app.route('/webhook', methods=["POST"])
async def webhook():
    if request.method == "POST":
        await app_bot.update_queue.put(Update.de_json(request.get_json(force=True), app_bot.bot))
        return "OK"
