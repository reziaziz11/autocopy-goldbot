from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📈 Cek Sinyal", callback_data="cek_sinyal"),
            InlineKeyboardButton("💼 Daftar Akun", callback_data="daftar_akun")
        ],
        [
            InlineKeyboardButton("👑 Membership VIP", callback_data="vip")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 Selamat datang di *DJGOLD_BOT*!\n\n"
        "Saya akan bantu kamu mendapatkan sinyal XAUUSD terbaik dan auto-copy ke akun kamu.\n\n"
        "Silakan pilih menu di bawah ini untuk mulai 👇",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
