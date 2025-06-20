# app.py
import os
from telegram.ext import ApplicationBuilder
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from handlers.start import start_handler
from handlers.help import help_handler
from handlers.menu import menu_handler
from dotenv import load_dotenv
from fastapi import FastAPI, Request
import uvicorn

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "djgoldsecret")

app = FastAPI()
bot_app = ApplicationBuilder().token(TOKEN).build()

# Register handlers
bot_app.add_handler(CommandHandler("start", start_handler))
bot_app.add_handler(CommandHandler("help", help_handler))
bot_app.add_handler(CommandHandler("menu", menu_handler))

@app.post(f"/webhook/{WEBHOOK_SECRET}")
async def telegram_webhook(req: Request):
    data = await req.json()
    await bot_app.update_queue.put(data)
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "DJGOLD_BOT online 🚀"}
