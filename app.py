import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
from handlers.start import start_handler
from handlers.help import help_handler
from handlers.menu import menu_handler

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

app = FastAPI()
bot_app = ApplicationBuilder().token(TOKEN).build()

# Tambah handler ke app
bot_app.add_handler(CommandHandler("start", start_handler))
bot_app.add_handler(CommandHandler("help", help_handler))
bot_app.add_handler(CommandHandler("menu", menu_handler))

@app.on_event("startup")
async def on_startup():
    print("🌐 Webhook FastAPI dijalankan")

@app.post("/webhook")
async def handle_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return {"status": "ok"}

@app.get("/")
async def home():
    return {"message": "DJGOLD_BOT aktif bro 🚀"}
