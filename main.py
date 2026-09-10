import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN", "").strip()
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "ATILA VIVO"

async def pro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 ATILA PRO FATHER\nORO 5M: Piso 4312.0 RSI 36.7\n🔥 LONG YA SL 4307.5 TP +9 +19\nMarea: SOLO LONG")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ATILA VIVO - Usa /pro")

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pro", pro))
    app.add_handler(CommandHandler("marea", pro))
    app.add_handler(CommandHandler("scalp", pro))
    print("ATILA 3.13 OK")
    app.run_polling()
