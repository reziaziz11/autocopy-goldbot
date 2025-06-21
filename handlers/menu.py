from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📈 Mulai Copy Trading", callback_data="start_copy")],
        [InlineKeyboardButton("🧾 Daftar Akun", callback_data="daftar")],
        [InlineKeyboardButton("📊 Status Saya", callback_data="status")],
        [InlineKeyboardButton("🆘 Bantuan", callback_data="bantuan")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📍 Pilih menu di bawah ini untuk melanjutkan:", reply_markup=reply_markup)
