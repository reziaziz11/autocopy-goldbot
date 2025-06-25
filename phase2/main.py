from telegram.ext import Application, CommandHandler
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update, context):
    await update.message.reply_text("Halo! Bot aktif dan siap!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # Jalankan bot via webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        webhook_url=os.environ.get("WEBHOOK_URL")  # contoh: https://djgoldbot.onrender.com/webhook
    )

if __name__ == "__main__":
    main()
