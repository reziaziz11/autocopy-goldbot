from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "7524328423:AAFPrLxZtxnyyGmmguhc5KU_e524xnq4thI"
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

@app.route("/")
def home():
    return "Bot aktif."

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("DATA MASUK:", data)  # Debug log akan tampil di Render Logs

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        reply = f"📩 Kamu mengirim: {text}"

        requests.post(URL, json={
            "chat_id": chat_id,
            "text": reply
        })

    return {"ok": True}
