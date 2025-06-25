from flask import Flask, request
from telegram import Bot, Update
from telegram.constants import ParseMode
import os

# Token bot Telegram kamu
BOT_TOKEN = "7524328423:AAFPrLxZtxnyyGmmguhc5KU_e524xnq4thI"
bot = Bot(token=BOT_TOKEN)

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!"

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        data = request.get_json(force=True)
        update = Update.de_json(data, bot)
        handle_update(update)
        return "OK", 200
    return "Method Not Allowed", 405

def handle_update(update):
    if update.message:
        chat_id = update.message.chat.id
        text = update.message.text

        if text == "/start":
            bot.send_message(chat_id=chat_id, text="Selamat datang di @DJGOLD_BOT!", parse_mode=ParseMode.HTML)
        else:
            bot.send_message(chat_id=chat_id, text="Perintah tidak dikenal.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
