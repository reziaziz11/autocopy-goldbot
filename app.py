import os
from telegram.ext import ApplicationBuilder
from handlers.start import start_handler
from handlers.menu import menu_handler
from handlers.help import help_handler
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(start_handler)
    app.add_handler(menu_handler)
    app.add_handler(help_handler)

    print("Bot started...")
    await app.run_polling()  # ✅ Cara baru, nggak ada .updater lagi

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
