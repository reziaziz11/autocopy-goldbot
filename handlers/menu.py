from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

# Fungsi handler untuk perintah /menu
async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 Ini adalah menu utama. Pilih perintah yang ingin kamu gunakan:")

# Export handler sebagai 'menu' agar bisa diimport di main.py
menu = CommandHandler("menu", handle_menu)
