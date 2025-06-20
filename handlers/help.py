from telegram import Update
from telegram.ext import ContextTypes

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❓ Butuh bantuan? Hubungi admin atau ketik /start untuk mulai.")
