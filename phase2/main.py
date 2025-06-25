from telegram.ext import Application, CommandHandler
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_ACTUAL_BOT_TOKEN")

async def start(update, context):
    await update.message.reply_text("Halo! DJGOLD_BOT aktif 🚀")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == '__main__':
    main()
