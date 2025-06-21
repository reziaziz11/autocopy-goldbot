from telegram import Update
from telegram.ext import ContextTypes

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🆘 *Pusat Bantuan*\n\n"
        "Berikut beberapa perintah yang bisa kamu gunakan:\n"
        "/start - Mulai bot & tampilkan menu\n"
        "/help - Tampilkan bantuan\n"
        "/status - Cek status akun kamu\n"
        "Jika butuh bantuan lebih lanjut, hubungi admin."
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")
