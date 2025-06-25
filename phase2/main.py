import os
import asyncio
from telegram import Bot, Update
from telegram.constants import ParseMode
from flask import Flask, request

# Ambil token & secret dari variabel environment
BOT_TOKEN = os.environ.get("BOT_TOKEN", "ISI_TOKEN_KAMU")
SECRET_PATH = os.environ.get("SECRET_PATH", "webhook")

# Inisialisasi Flask
app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

# Webhook handler (POST dari Telegram)
@app.route(f"/{SECRET_PATH}", methods=["POST"])
def webhook_handler():
    if request.method == "POST":
        data = request.get_json(force=True)
        update = Update.de_json(data, bot)

        if update.message:
            chat_id = update.message.chat.id
            message = update.message.text

            # Balas otomatis
            asyncio.run(bot.send_message(
                chat_id=chat_id,
                text=f"Halo! Kamu kirim: <b>{message}</b>",
                parse_mode=ParseMode.HTML
            ))

        return "ok", 200

# Tes kirim pesan manual (akses dari luar, opsional)
@app.route("/test")
def test_send():
    chat_id = os.environ.get("TEST_CHAT_ID", "")  # set di env
    if chat_id:
        asyncio.run(bot.send_message(chat_id=chat_id, text="Test dari /test endpoint"))
        return "Pesan test dikirim!", 200
    return "CHAT_ID belum di-set", 400

# Jalankan Flask di Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
