import os
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN") or os.getenv("TOKEN") or os.getenv("BOT_TOK")

app_flask = Flask(__name__)
@app_flask.route("/")
def home():
    return "ATILA VIVO"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ATILA ACTIVO FATHER 🔥 Usa /marea")

async def marea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Marea MDQ: Subiendo FATHER - bot funcionando")

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app_flask.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    print("ATILA INICIADO FATHER")
    import threading
    threading.Thread(target=run_flask, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("marea", marea))
    app.run_polling()
