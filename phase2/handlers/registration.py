from telegram import Update
from telegram.ext import (
    ContextTypes, ConversationHandler, CommandHandler,
    MessageHandler, filters
)

NAMA, EMAIL, WHATSAPP, BROKER, AKUN = range(5)

async def start_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Selamat datang di DJGOLD BOT 🚀\n\nYuk daftar dulu!\n\n✏️ Siapa nama lengkap kamu?"
    )
    return NAMA

async def get_nama(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['nama'] = update.message.text
    await update.message.reply_text("📧 Email kamu?")
    return EMAIL

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['email'] = update.message.text
    await update.message.reply_text("📱 Nomor WhatsApp kamu?")
    return WHATSAPP

async def get_whatsapp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['whatsapp'] = update.message.text
    await update.message.reply_text("💼 Broker yang kamu pakai?")
    return BROKER

async def get_broker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['broker'] = update.message.text
    await update.message.reply_text("🔢 Nomor akun MT5 kamu?")
    return AKUN

async def get_akun(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['akun'] = update.message.text
    data = context.user_data

    summary = (
        f"✅ Data kamu tercatat:\n\n"
        f"👤 Nama: {data['nama']}\n"
        f"📧 Email: {data['email']}\n"
        f"📱 WA: {data['whatsapp']}\n"
        f"💼 Broker: {data['broker']}\n"
        f"🔢 Akun MT5: {data['akun']}"
    )

    await update.message.reply_text(summary)
    return ConversationHandler.END

def get_registration_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("start", start_form)],
        states={
            NAMA: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_nama)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            WHATSAPP: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_whatsapp)],
            BROKER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_broker)],
            AKUN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_akun)],
        },
        fallbacks=[],
    )
