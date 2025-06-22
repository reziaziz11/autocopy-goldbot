import os
import asyncio
import nest_asyncio
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

nest_asyncio.apply()
load_dotenv()
TOKEN = os.getenv("TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://djgoldbot.onrender.com{WEBHOOK_PATH}"

app = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📬 Handler /start dipanggil oleh:", update.effective_user.id)
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

bot_app.add_handler(CommandHandler("start", start))

@app.route("/")
def index():
    return "✅ DJGOLD BOT AKTIF"

@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    payload = request.get_json(force=True)
    print("👉 OTAK TERIMA UPDATE:", payload)
    update = Update.de_json(payload, bot_app.bot)
    await bot_app.process_update(update)
    return "OK", 200

async def main():
    await bot_app.initialize()
    await bot_app.bot.set_webhook(url=WEBHOOK_URL)
    await bot_app.start()
    print(f"✅ Webhook aktif di: {WEBHOOK_URL}")

if __name__ == "__main__":
    asyncio.get_event_loop().create_task(main())
    app.run(host="0.0.0.0", port=10000)
