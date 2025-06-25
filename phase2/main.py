from flask import Flask, request
import requests
import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    CommandHandler, MessageHandler, Filters,
    ConversationHandler, CallbackContext, Dispatcher
)
from telegram import Bot
import os

# === Setup bot ===
TOKEN = os.environ.get("BOT_TOKEN")  # atau langsung ganti dengan token kamu
bot = Bot(token=TOKEN)

app = Flask(__name__)

# === Webhook endpoint ===
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == "POST":
        data = request.get_json()
        if "message" in data:
            update = Update.de_json(data, bot)
            dispatcher.process_update(update)
    return "OK"

@app.route('/')
def index():
    return 'Phase 2 bot is running.'

# === Form Pendaftaran ===
(
    NAMA_LENGKAP, EMAIL, NO_HP,
    BROKER, AKUN_MT5
) = range(5)

user_data_dict = {}

def start(update: Update, context: CallbackContext):
    keyboard = [['📝 Daftar']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(
        "Selamat datang di DJGOLD BOT!\nSilakan pilih menu di bawah ini.",
        reply_markup=reply_markup
    )

def daftar(update: Update, context: CallbackContext):
    update.message.reply_text("Masukkan nama lengkap Anda:")
    return NAMA_LENGKAP

def input_nama(update: Update, context: CallbackContext):
    user_data_dict[update.message.chat_id] = {"nama": update.message.text}
    update.message.reply_text("Masukkan email Anda:")
    return EMAIL

def input_email(update: Update, context: CallbackContext):
    user_data_dict[update.message.chat_id]["email"] = update.message.text
    update.message.reply_text("Masukkan nomor HP Anda:")
    return NO_HP

def input_hp(update: Update, context: CallbackContext):
    user_data_dict[update.message.chat_id]["hp"] = update.message.text
    update.message.reply_text("Masukkan nama broker Anda:")
    return BROKER

def input_broker(update: Update, context: CallbackContext):
    user_data_dict[update.message.chat_id]["broker"] = update.message.text
    update.message.reply_text("Masukkan nomor akun MT5 Anda:")
    return AKUN_MT5

def input_akun(update: Update, context: CallbackContext):
    user_data_dict[update.message.chat_id]["akun"] = update.message.text

    data = user_data_dict[update.message.chat_id]
    summary = f"✅ Pendaftaran berhasil!\n\n" \
              f"👤 Nama: {data['nama']}\n" \
              f"📧 Email: {data['email']}\n" \
              f"📱 HP: {data['hp']}\n" \
              f"🏦 Broker: {data['broker']}\n" \
              f"📈 Akun MT5: {data['akun']}"

    update.message.reply_text(summary)

    # Kirim notifikasi ke admin
    ADMIN_ID = os.environ.get("ADMIN_ID")  # atau ganti manual
    if ADMIN_ID:
        bot.send_message(chat_id=ADMIN_ID, text=f"🔔 Pendaftar baru:\n\n{summary}")

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Pendaftaran dibatalkan.")
    return ConversationHandler.END

# === Dispatcher ===
from telegram.ext import Updater
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

conv_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('^📝 Daftar$'), daftar)],
    states={
        NAMA_LENGKAP: [MessageHandler(Filters.text & ~Filters.command, input_nama)],
        EMAIL: [MessageHandler(Filters.text & ~Filters.command, input_email)],
        NO_HP: [MessageHandler(Filters.text & ~Filters.command, input_hp)],
        BROKER: [MessageHandler(Filters.text & ~Filters.command, input_broker)],
        AKUN_MT5: [MessageHandler(Filters.text & ~Filters.command, input_akun)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(conv_handler)
