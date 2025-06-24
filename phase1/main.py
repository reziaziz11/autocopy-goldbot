from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "7524328423:AAFPrLxZtxnyyGmmguhc5KU_e524xnq4thI"
URL = f"https://api.telegram.org/bot{TOKEN}"

@app.route("/")
def home():
    return "Bot Aktif! (Phase 1)"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if data.get("message"):
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        requests.post(f"{URL}/sendMessage", json={
            "chat_id": chat_id,
            "text": f"Halo! Kamu mengirim: {text}"
        })
    return {"ok": True}

if __name__ == "__main__":
    app.run()
