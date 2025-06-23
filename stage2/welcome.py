from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot aktif dan siap menerima perintah!")

welcome_handler = CommandHandler("start", welcome)
