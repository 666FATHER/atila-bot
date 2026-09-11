import os, threading, requests
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
app_flask = Flask(__name__)

@app_flask.route("/")
def home():
    return "ATILA SUPER PRO OK", 200

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola Father! Soy ATILA SUPER PRO y estoy activo ✅")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Recibido: {update.message.text}")

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app_flask.run(host="0.0.0.0", port=port)

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    app_bot = Application.builder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app_bot.run_polling()

if __name__ == "__main__":
    main()
