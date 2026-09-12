import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Atila vivo Father!")

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("FALTA BOT_TOKEN")
        return
        app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot iniciado...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
