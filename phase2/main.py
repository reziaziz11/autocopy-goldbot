phase2/main.py

import os from telegram.ext import Application from handlers.registration import registration_conversation_handler from dotenv import load_dotenv

load_dotenv() TOKEN = os.getenv("BOT_TOKEN")

bot_app = Application.builder().token(TOKEN).build()

bot_app.add_handler(registration_conversation_handler)

if name == "main": bot_app.run_webhook( listen="0.0.0.0", port=int(os.environ.get("PORT", 5000)), webhook_url=os.environ.get("WEBHOOK_URL") )

