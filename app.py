from telegram.ext import ApplicationBuilder, CommandHandler
import asyncio
import os
from handlers.start import start_handler
from handlers.menu import menu_handler
from handlers.help import help_handler

TOKEN = os.getenv("BOT_TOKEN")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Tambahkan handler
    app.add_handler(start_handler)
    app.add_handler(menu_handler)
    app.add_handler(help_handler)

    # Start bot
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
