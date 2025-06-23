import os
import logging
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

logging.basicConfig(level=logging.INFO)

# === BOT SETUP ===
bot_app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ DJGOLD BOT AKTIF!\nGunakan menu di bawah ini untuk mulai trading.")

bot_app.add_handler(CommandHandler("start", start))

# === FLASK SETUP ===
app = Flask(__name__)

@app.route('/')
def home():
    return "DJGOLD BOT AKTIF ✅"

@app.route('/webhook', methods=["POST"])
async def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot_app.bot)
        await bot_app.update_queue.put(update)
        return "ok"

# === RUN BOT (needed for handling queue) ===
import asyncio
from threading import Thread

def run_asyncio():
    asyncio.run(bot_app.initialize())
    asyncio.run(bot_app.start())

Thread(target=run_asyncio).start()
