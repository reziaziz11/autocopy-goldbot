from telegram import Update, ForceReply
from telegram.ext import ContextTypes

# Menyimpan data sementara (bisa diganti ke database nanti)
user_states = {}

# Langkah-langkah form
form_steps = ['full_name', 'email', 'phone', 'broker', 'mt5_account']

# Label pertanyaan
form_questions = {
    'full_name': "📛 Masukkan *Nama Lengkap* Anda:",
    'email': "📧 Masukkan *Email* aktif Anda:",
    'phone': "📱 Masukkan *Nomor HP* Anda:",
    'broker': "🏦 Masukkan *Nama Broker* Anda:",
    'mt5_account': "💹 Masukkan *Nomor Akun MT5* Anda:"
}

# Memulai pendaftaran
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = {'step': 0, 'data': {}}
    await update.message.reply_markdown(form_questions[form_steps[0]], reply_markup=ForceReply())

# Menangani tiap input user
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    # Jika belum mulai pendaftaran
    if user_id not in user_states:
        await update.message.reply_text("Ketik /start untuk memulai pendaftaran.")
        return

    state = user_states[user_id]
    current_step = form_steps[state['step']]
    state['data'][current_step] = text
    state['step'] += 1

    if state['step'] < len(form_steps):
        next_step = form_steps[state['step']]
        await update.message.reply_markdown(form_questions[next_step], reply_markup=ForceReply())
    else:
        # Pendaftaran selesai
        data = state['data']
        user_states.pop(user_id)
        summary = (
            "✅ *Pendaftaran Selesai!*\n\n"
            f"• Nama: {data['full_name']}\n"
            f"• Email: {data['email']}\n"
            f"• HP: {data['phone']}\n"
            f"• Broker: {data['broker']}\n"
            f"• Akun MT5: {data['mt5_account']}\n"
        )
        await update.message.reply_markdown(summary)
