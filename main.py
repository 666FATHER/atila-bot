import os
import requests
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# TOKEN LIMPIO - Arregla el error InvalidToken
TOKEN = (os.getenv("TELEGRAM_TOKEN") or os.getenv("BOT_TOKEN") or "").strip()

# Servidor falso para Railway
app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "ATILA VIVO FATHER - BOT ACTIVO"

def get_price(symbol):
    """Trae precio de Binance"""
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        data = requests.get(url, timeout=10).json()
        return float(data['price'])
    except:
        return 0.0

async def marea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /marea"""
    oro = get_price("PAXG")
    btc = get_price("BTC")
    eth = get_price("ETH")
    
    mensaje = f"""🌊 ATILA - MAREA FATHER 🌊

🥇 ORO: ${oro:,.2f} USD
₿ BTC: ${btc:,.2f} USD
💎 ETH: ${eth:,.2f} USD

Fuente: Binance
Bot: Activo 24/7
"""
    await update.message.reply_text(mensaje)

def main():
    # Inicia Flask en segundo plano
    Thread(
        target=lambda: app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080))),
        daemon=True
    ).start()
    
    print(f"ATILA INICIADO FATHER - TOKEN ...{TOKEN[-6:]}")
    
    # Inicia Bot de Telegram
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("marea", marea))
    app.add_handler(CommandHandler("start", marea))
    app.add_handler(CommandHandler("oro", marea))
    
    app.run_polling()

if __name__ == "__main__":
    main()
