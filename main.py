import os, requests, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = (os.getenv("BOT_TOKEN") or "").strip()
app_flask = Flask(__name__)

@app_flask.route("/")
def home():
    return "ATILA VIVO"

def get_data():
    return f"📊 ATILA PRO FATHER - ORO ${4316.5}\nRSI: 36.7 - ESPERANDO BARRIDA\nMarea: SOLO LONG - Comerciales comprando"

async def pro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_data())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ATILA VIVO /pro")

def run_flask():
    app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    a = Application.builder().token(TOKEN).build()
    a.add_handler(CommandHandler("start", start))
    a.add_handler(CommandHandler("pro", pro))
    a.add_handler(CommandHandler("marea", pro))
    a.add_handler(CommandHandler("scalp", pro))
    print("ATILA INICIADO")
    a.run_polling()
