from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Hai {user.first_name}!\n\n"
        "Selamat datang di *DJGOLD BOT*.\n\n"
        "Gunakan tombol /menu atau /help untuk mulai.\n",
        parse_mode="Markdown"
    )
