======== DEBUG CHECK BOT DJGOLD_BOT ========

from flask import Flask, request from telegram import Update from telegram.ext import Application, CommandHandler, ContextTypes import nest_asyncio import asyncio import os from dotenv import load_dotenv

=== Load env ===

load_dotenv() TOKEN = os.getenv("TOKEN")

=== Flask App ===

app = Flask(name)

=== Bot App ===

bot_app = Application.builder().token(TOKEN).build()

=== Handler /start ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

bot_app.add_handler(CommandHandler("start", start))

=== Flask Webhook Endpoint ===

@app.route("/webhook", methods=["POST"]) def webhook(): if request.method == "POST": update = Update.de_json(request.get_json(force=True), bot_app.bot) asyncio.create_task(bot_app.process_update(update)) return "ok"

=== Run Flask + Nest Asyncio ===

nest_asyncio.apply() if name == 'main': bot_app.initialize() app.run(host='0.0.0.0', port=10000)

