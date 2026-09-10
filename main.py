import os
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = (os.getenv("BOT_TOKEN") or os.getenv("BOT_TOK") or os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRA") or "").strip()

flask_app = Flask(__name__)
@flask_app.route("/")
def home():
    return "ATILA VIVO"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ATILA ACTIVO FATHER")

async def marea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Marea OK FATHER")

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    print("ATILA INICIADO FATHER")
    import threading
    threading.Thread(target=run_flask, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("marea", marea))
    app.run_polling()
