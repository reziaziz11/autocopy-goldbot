async def main():
    # Inisialisasi Application
    bot_app = Application.builder().token(TOKEN).build()

    # Tambahkan handler (contoh start)
    bot_app.add_handler(CommandHandler("start", start))

    # WAJIB panggil initialize dulu
    await bot_app.initialize()

    # Set webhook
    await bot_app.bot.set_webhook(f"{WEBHOOK_URL}/webhook")

    # Mulai webhook
    await bot_app.start()
    await bot_app.updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="/webhook",
        webhook_url=f"{WEBHOOK_URL}/webhook",
    )

    print(f"✅ Webhook telah diset ke: {WEBHOOK_URL}/webhook")

    # Tunggu sampai dihentikan
    await bot_app.updater.wait()
