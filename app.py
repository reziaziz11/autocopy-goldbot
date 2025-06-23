import os
import asyncio
import nest_asyncio
from dotenv import load_dotenv
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder

# === INIT ===
load_dotenv()
nest_asyncio.apply()
app = Flask(__name__)

# === BOT ===
TOKEN = os.getenv("TOKEN")
application = ApplicationBuilder().token(TOKEN).build()

# === HANDLER STAGE 2 ===
from stage2.welcome import welcome_handler
application.add_handler(welcome_handler)

# === WEBHOOK ENDPOINT ===
@app.post("/webhook")
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.update_queue.put(update)
    return "ok", 200

@app.route('/')
def index():
    return '✅ DJGOLD_BOT aktif', 200

# === JALANKAN BOT DI BACKGROUND ===
async def run_bot():
    await application.initialize()
    await application.start()

# === MAIN RUN ===
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
