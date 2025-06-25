application.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    import threading

    def run_webhook():
        asyncio.run(application.bot.set_webhook(WEBHOOK_URL))

    threading.Thread(target=run_webhook).start()
    app.run(host="0.0.0.0", port=10000)
