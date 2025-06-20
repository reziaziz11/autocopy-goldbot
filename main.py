import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler

# Ambil BOT_TOKEN dari phase_1_core
from phase_1_core.config import BOT_TOKEN

# Import semua handler
from handlers.start import start_handler
from handlers.menu import menu_handler
from handlers.help import help_handler

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Daftarkan command handler
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("menu", menu_handler))
    app.add_handler(CommandHandler("help", help_handler))

    print("✅ DJGOLD_BOT sudah aktif bro...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
