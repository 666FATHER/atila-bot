import os
import threading
import requests
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN", "").strip()
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "ATILA SUPER PRO VIVO"

# --- FUNCIONES INSTITUCIONALES ---
def get_institutional():
    try:
        price = requests.get("https://fapi.binance.com/fapi/v1/ticker/price?symbol=BTCUSDT", timeout=5).json()['price']
        funding = requests.get("https://fapi.binance.com/fapi/v1/fundingRate?symbol=BTCUSDT&limit=1", timeout=5).json()[0]
        oi = requests.get("https://fapi.binance.com/fapi/v1/openInterest?symbol=BTCUSDT", timeout=5).json()['openInterest']
        lsr = requests.get("https://fapi.binance.com/fapi/v1/globalLongShortAccountRatio?symbol=BTCUSDT&period=5m&limit=1", timeout=5).json()[0]

        return {
            "price": float(price),
            "funding": float(funding['fundingRate'])*100,
            "oi": float(oi),
            "long_short": float(lsr['longShortRatio']),
            "funding_time": funding['fundingTime']
        }
    except Exception as e:
        return None

def get_scalp_signal():
    try:
        # Velas 5m
        klines = requests.get("https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=5m&limit=50", timeout=5).json()
        closes = [float(k[4]) for k in klines]

        # EMA 9 y 21 simple
        ema9 = sum(closes[-9:]) / 9
        ema21 = sum(closes[-21:]) / 21

        # RSI 14 simple
        gains = [max(0, closes[i]-closes[i-1]) for i in range(1, len(closes))]
        losses = [max(0, closes[i-1]-closes[i]) for i in range(1, len(closes))]
        avg_gain = sum(gains[-14:]) / 14
        avg_loss = sum(losses[-14:]) / 14
        rs = avg_gain / (avg_loss if avg_loss!= 0 else 0.001)
        rsi = 100 - (100 / (1 + rs))

        price = closes[-1]

        if ema9 > ema21 and rsi > 55:
            signal = "🟢 LONG SCALP 5M"
            action = "Entrada larga con confirmación alcista"
        elif ema9 < ema21 and rsi < 45:
            signal = "🔴 SHORT SCALP 5M"
            action = "Entrada corta con confirmación bajista"
        else:
            signal = "🟡 ESPERAR"
            action = "Sin tendencia clara, no entrar"

        return price, ema9, ema21, rsi, signal, action
    except Exception as e:
        return None

# --- COMANDOS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ATILA SUPER PRO VIVO FATHER\nUsa /pro para info institucional + señal 5m")

async def pro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Analizando institucional FATHER...")

    inst = get_institutional()
    scalp = get_scalp_signal()

    if not inst or not scalp:
        await update.message.reply_text("Error al traer datos de Binance, reintentá en 10 seg FATHER")
        return

    price, ema9, ema21, rsi, signal, action = scalp

    msg = f"""🏛️ **ATILA SUPER PRO - INSTITUCIONAL**

💰 BTC: ${inst['price']:,.2f}
📊 Open Interest: {inst['oi']:,.0f} BTC
💸 Funding Rate: {inst['funding']:.04f}%
⚖️ Long/Short Ratio: {inst['long_short']:.2f}

📈 **SCALP 5M**
Precio: ${price:,.2f}
EMA 9: ${ema9:,.2f}
EMA 21: ${ema21:,.2f}
RSI 14: {rsi:.1f}

{signal}
👉 {action}

> Fuente: Binance Futures (Real Time)
"""
    await update.message.reply_text(msg, parse_mode='Markdown')

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pro", pro))
    app.add_handler(CommandHandler("marea", pro))
    app.add_handler(CommandHandler("scalp", pro))
    print("ATILA SUPER PRO OK")
    app.run_polling()
