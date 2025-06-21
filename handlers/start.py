# handlers/start.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Fungsi handler untuk /start
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name if user else "Trader"

    # Tombol inline
    keyboard = [
        [
            InlineKeyboardButton("📈 Cek Sinyal", callback_data="cek_sinyal"),
            InlineKeyboardButton("💳 Membership", callback_data="membership"),
        ],
        [
            InlineKeyboardButton("📊 Statistik", callback_data="statistik"),
            InlineKeyboardButton("❓ Bantuan", callback_data="bantuan"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"👋 Hai {name}!\n\n"
        "Selamat datang di *DJGOLD_BOT* — sistem auto copy trading XAUUSD 💰\n\n"
        "Silakan pilih menu di bawah ini untuk mulai:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
