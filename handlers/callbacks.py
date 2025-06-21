from telegram import Update
from telegram.ext import ContextTypes

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "join":
        await query.edit_message_text("🚀 Untuk bergabung sebagai member, silakan ketik /start dan ikuti instruksi.")
    elif query.data == "status":
        await query.edit_message_text("ℹ️ Status akun kamu akan ditampilkan di sini (fitur dalam pengembangan).")
    elif query.data == "bantuan":
        await query.edit_message_text("🆘 Bantuan tersedia. Ketik /help untuk informasi lengkap.")
    else:
        await query.edit_message_text("❓ Opsi tidak dikenali.")
