from telegram import Update
from telegram.ext import ContextTypes

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 Menu:\n1. Mulai Trading\n2. Cek Status\n3. Bantuan")
