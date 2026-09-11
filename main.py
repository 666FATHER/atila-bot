import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")

app_flask = Flask(__name__)

@app_flask.route("/")
def home():
    return "ATILA SUPER PRO OK - BOT ACTIVO", 200

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola Father! Soy ATILA y estoy online ✅")

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    await update.message.reply_text(f"Recibido Father: {texto}")

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app_flask.run(host="0.0.0.0", port=port)

def main():
    if not BOT_TOKEN:
        print("ERROR: Falta BOT_TOKEN en Variables")
        # Mantenemos Flask vivo para que no crashee Railway
        run_flask()
        return

    threading.Thread(target=run_flask, daemon=True).start()
    
    app_bot = Application.builder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    
    print("ATILA INICIADO...")
    app_bot.run_polling()

if __name__ == "__main__":
    main()
