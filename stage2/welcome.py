from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first = update.effective_user.first_name or "Trader"

    welcome_text = (
        f"👋 Halo *{user_first}*, selamat datang di *DJGOLD_BOT*!\n\n"
        "📡 *Sinyal XAUUSD otomatis & copy trading real-time!*\n\n"
        "Silakan pilih menu di bawah untuk mulai:"
    )

    keyboard = [
        [InlineKeyboardButton("📈 Lihat Sinyal", callback_data="lihat_sinyal")],
        [InlineKeyboardButton("👤 Daftar Akun", callback_data="daftar_akun")],
        [InlineKeyboardButton("💳 Membership", callback_data="membership")],
        [InlineKeyboardButton("❓ Bantuan", callback_data="bantuan")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
