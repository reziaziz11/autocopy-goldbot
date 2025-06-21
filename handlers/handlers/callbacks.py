from telegram import Update
from telegram.ext import ContextTypes

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "cek_sinyal":
        await query.edit_message_text("📈 Fitur cek sinyal sedang dalam pengembangan.")
    elif query.data == "daftar_akun":
        await query.edit_message_text("💼 Daftarkan akun MT5 kamu segera. (Fitur segera aktif!)")
    elif query.data == "vip":
        await query.edit_message_text("👑 Membership VIP akan segera dibuka!")
