from flask import Flask, request import requests import json from telegram import Update, ReplyKeyboardMarkup from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, Dispatcher

app = Flask(name)

--- Konstanta state ---

(NAMA, EMAIL, NO_HP, BROKER, AKUN_MT5) = range(5)

--- Tombol menu awal ---

def start(update: Update, context: CallbackContext): keyboard = [["Daftar"]] reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True) update.message.reply_text("Selamat datang di DJGOLD_BOT!\n\nSilakan pilih menu:", reply_markup=reply_markup)

--- Mulai form daftar ---

def daftar(update: Update, context: CallbackContext): update.message.reply_text("📄 Masukkan Nama Lengkap Anda:", parse_mode='Markdown') return NAMA

def input_nama(update: Update, context: CallbackContext): context.user_data['nama'] = update.message.text update.message.reply_text("📧 Masukkan Email Anda:", parse_mode='Markdown') return EMAIL

def input_email(update: Update, context: CallbackContext): context.user_data['email'] = update.message.text update.message.reply_text("📱 Masukkan Nomor HP Anda:", parse_mode='Markdown') return NO_HP

def input_nohp(update: Update, context: CallbackContext): context.user_data['no_hp'] = update.message.text update.message.reply_text("🏦 Masukkan Broker yang Anda gunakan:", parse_mode='Markdown') return BROKER

def input_broker(update: Update, context: CallbackContext): context.user_data['broker'] = update.message.text update.message.reply_text("🔢 Masukkan Nomor Akun MT5 Anda:", parse_mode='Markdown') return AKUN_MT5

def input_akun(update: Update, context: CallbackContext): context.user_data['akun_mt5'] = update.message.text

# Kirim ringkasan pendaftaran ke admin
data = context.user_data
summary = f"🆕 Pendaftaran Baru:\n\n👤 Nama: {data['nama']}\n📧 Email: {data['email']}\n📱 No HP: {data['no_hp']}\n🏦 Broker: {data['broker']}\n🔢 Akun MT5: {data['akun_mt5']}"
update.message.reply_text("✅ Pendaftaran berhasil dikirim! Admin akan segera memverifikasi.")

# Ganti ID dengan ID Telegram admin kamu
admin_id = 123456789
context.bot.send_message(chat_id=admin_id, text=summary)
return ConversationHandler.END

def cancel(update: Update, context: CallbackContext): update.message.reply_text("❌ Pendaftaran dibatalkan.") return ConversationHandler.END

--- Webhook Flask + Telegram ---

@app.route("/") def index(): return "DJGOLD_BOT Phase 2 Aktif"

@app.route("/webhook", methods=["POST"]) def webhook(): update = Update.de_json(request.get_json(force=True), bot) dispatcher.process_update(update) return "ok"

--- Token & Dispatcher ---

from telegram import Bot from telegram.ext import Updater

TOKEN = "7524328423:AAGbx7KMgXRzIr9gAmg9I4WznFRmWiXKuNQ" bot = Bot(token=TOKEN) dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

--- Register handler ---

conv_handler = ConversationHandler( entry_points=[MessageHandler(Filters.regex("^(Daftar)$"), daftar)], states={ NAMA: [MessageHandler(Filters.text & ~Filters.command, input_nama)], EMAIL: [MessageHandler(Filters.text & ~Filters.command, input_email)], NO_HP: [MessageHandler(Filters.text & ~Filters.command, input_nohp)], BROKER: [MessageHandler(Filters.text & ~Filters.command, input_broker)], AKUN_MT5: [MessageHandler(Filters.text & ~Filters.command, input_akun)], }, fallbacks=[CommandHandler("cancel", cancel)] )

dispatcher.add_handler(CommandHandler("start", start)) dispatcher.add_handler(conv_handler)

