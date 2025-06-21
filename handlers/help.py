from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

# Fungsi handler untuk perintah /help
async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ℹ️ Bantuan: Gunakan perintah yang tersedia untuk berinteraksi dengan bot.")

# Export handler sebagai 'help_command' agar bisa diimport di main.py
help_command = CommandHandler("help", handle_help)
