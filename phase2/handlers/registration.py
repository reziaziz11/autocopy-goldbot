from telegram import Update
from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# States
ASK_NAME, ASK_EMAIL, ASK_PHONE, ASK_BROKER, ASK_ACCOUNT = range(5)

async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🟡 Masukkan nama lengkap Anda:")
    return ASK_NAME

async def ask_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("📧 Masukkan email Anda:")
    return ASK_EMAIL

async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["email"] = update.message.text
    await update.message.reply_text("📱 Masukkan nomor HP Anda:")
    return ASK_PHONE

async def ask_broker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("💼 Masukkan broker yang Anda gunakan:")
    return ASK_BROKER

async def ask_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["broker"] = update.message.text
    await update.message.reply_text("🔢 Masukkan nomor akun MT5 Anda:")
    return ASK_ACCOUNT

async def finish_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["account"] = update.message.text

    summary = (
        f"✅ Pendaftaran selesai!\n\n"
        f"🧑 Nama: {context.user_data['name']}\n"
        f"📧 Email: {context.user_data['email']}\n"
        f"📱 HP: {context.user_data['phone']}\n"
        f"💼 Broker: {context.user_data['broker']}\n"
        f"🔢 Akun MT5: {context.user_data['account']}"
    )

    await update.message.reply_text(summary)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Pendaftaran dibatalkan.")
    return ConversationHandler.END

registration_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("daftar", start_registration)],
    states={
        ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_email)],
        ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
        ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_broker)],
        ASK_BROKER: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_account)],
        ASK_ACCOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, finish_registration)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
