async def main():
    bot_app = Application.builder().token(TOKEN).build()

    # Handler
    bot_app.add_handler(CommandHandler("start", start))

    # Initialize dan start webhook
    await bot_app.initialize()
    await bot_app.start()
    await bot_app.updater.start_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        url_path=TOKEN,
        webhook_url=f"{BASE_URL}/webhook"
    )
    print("✅ Webhook telah diset ke:", f"{BASE_URL}/webhook")

    await bot_app.updater.wait()
