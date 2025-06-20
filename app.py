from telegram.ext import ApplicationBuilder, CommandHandler
from handlers.start import start_handler
from handlers.menu import menu_handler
from handlers.help import help_handler
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

app = ApplicationBuilder().token(TOKEN).build()

# Tambahkan handler
app.add_handler(CommandHandler("start", start_handler))
app.add_handler(CommandHandler("menu", menu_handler))
app.add_handler(CommandHandler("help", help_handler))

# Gunakan polling
if __name__ == "__main__":
    print("✅ Bot aktif bro...")
    app.run_polling()
