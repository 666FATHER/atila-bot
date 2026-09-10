import os
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN") or os.getenv("TOKEN")

app_flask = Flask(__name__)
@app_flask.route("/")
def home():
    return "ATILA VIVO FATHER"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ATILA ACTIVO FATHER. Usa /marea")

async def marea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Marea: subiendo en MDQ FATHER - probando")

def main():
    print("ATILA INICIADO FATHER")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("marea", marea))
    app.run_polling()

if __name__ == "__main__":
    import threading
    port = int(os.environ.get("PORT", 8080))
    threading.Thread(target=lambda: app_flask.run(host="0.0.0.0", port=port)).start()
    main()
