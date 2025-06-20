import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from handlers.start import start_handler
from handlers.help import help_handler
from handlers.menu import menu_handler
import asyncio

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("menu", menu_handler))

    print("✅ Bot aktif via polling")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
