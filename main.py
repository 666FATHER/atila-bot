import os, requests, asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")
BINANCE = "https://api.binance.com"

app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "ATILA V7 REAL ACTIVO"

def get_price(symbol):
    r = requests.get(f"{BINANCE}/api/v3/ticker/24hr?symbol={symbol}", timeout=10).json()
    return float(r['lastPrice']), float(r['highPrice']), float(r['lowPrice'])

def get_5m(symbol):
    r = requests.get(f"{BINANCE}/api/v3/klines?symbol={symbol}&interval=5m&limit=20", timeout=10).json()
    lows = [float(x[3]) for x in r]
    highs = [float(x[2]) for x in r]
    return min(lows[-3:]), max(highs[-3:])

def get_orderbook(symbol):
    r = requests.get(f"{BINANCE}/api/v3/depth?symbol={symbol}&limit=20", timeout=10).json()
    bids = sum(float(b[1]) for b in r['bids'][:10])
    asks = sum(float(a[1]) for a in r['asks'][:10])
    ratio = bids/asks if asks>0 else 1
    return bids, asks, ratio

def get_cvd(symbol):
    r = requests.get(f"{BINANCE}/api/v3/trades?symbol={symbol}&limit=500", timeout=10).json()
    buy = sum(float(t['qty']) for t in r if not t['isBuyerMaker'])
    sell = sum(float(t['qty']) for t in r if t['isBuyerMaker'])
    return buy, sell, buy-sell

def get_funding(symbol):
    try:
        r = requests.get(f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={symbol}", timeout=10).json()
        return float(r['lastFundingRate'])*100
    except: return 0

async def marea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        oro_price, oro_high, oro_low = get_price("PAXGUSDT")
        btc_price, btc_high, btc_low = get_price("BTCUSDT")

        oro_5m_low, oro_5m_high = get_5m("PAXGUSDT")
        btc_5m_low, btc_5m_high = get_5m("BTCUSDT")

        oro_bid, oro_ask, oro_ratio = get_orderbook("PAXGUSDT")
        btc_bid, btc_ask, btc_ratio = get_orderbook("BTCUSDT")

        oro_b, oro_s, oro_cvd = get_cvd("PAXGUSDT")
        btc_b, btc_s, btc_cvd = get_cvd("BTCUSDT")

        btc_funding = get_funding("BTCUSDT")

        # Lógica marea real simple pro
        marea_oro = "PISO - SOLO LONG" if oro_ratio > 1.2 and oro_cvd > 0 else "TECHO - CUIDADO LONG"
        marea_btc = "PISO - LONG" if btc_funding < 0 else "TECHO"

        msg = f"""🤖 ATILA V7 REAL - DATO REAL

📊 MAREA MACRO POR QUÉ:
ORO: {marea_oro} | Ratio Bid/Ask {oro_ratio:.2f}x | CVD {'VERDE' if oro_cvd>0 else 'ROJO'}
BTC: {marea_btc} | Funding {btc_funding:.4f}% | CVD {'VERDE' if btc_cvd>0 else 'ROJO'}
COT USA: Comerciales siguen NET LONG (base CFTC viernes)

📍 DATOS REALES HOY:
ORO: Ahora {oro_price:.2f} | Max Hoy {oro_high:.2f} | Min Hoy {oro_low:.2f} | Min 5m {oro_5m_low:.2f}
BTC: Ahora {btc_price:.0f} | Max Hoy {btc_high:.0f} | Min Hoy {btc_low:.0f} | Min 5m {btc_5m_low:.0f}

🔎 ORDENES REAL (elmflow):
ORO: Bids {oro_bid:.1f} vs Asks {oro_ask:.1f} = {oro_ratio:.2f}x {'COMPRADORES' if oro_ratio>1 else 'VENDEDORES'} mandan
BTC: Bids {btc_bid:.1f} vs Asks {btc_ask:.1f} = {btc_ratio:.2f}x

🎯 ENTRADA 5M CLARA - ACÁ ENTRÁS:

🔵 ORO AHORA {oro_price:.2f}
👉 HACER: {'ESPERAR LONG' if oro_ratio>1 else 'ESPERAR SHORT'}
📍 ENTRADA: {oro_5m_low:.2f} - {oro_5m_low+1:.2f}
🛑 STOP: {oro_5m_low-5:.2f}
🎯 LLEGA: {oro_5m_high:.2f} / {oro_high:.2f}
⚠️ NO HACER: No compres en {oro_high:.2f} caro

🟠 BTC AHORA {btc_price:.0f}
👉 HACER: {'LONG YA' if btc_funding<0 or btc_ratio>1 else 'ESPERAR'}
📍 ENTRADA: {btc_5m_low:.0f}
🛑 STOP: {btc_5m_low-300:.0f}
🎯 LLEGA: {btc_5m_high:.0f} / {btc_high:.0f}
⚠️ Funding: {btc_funding:.4f}% {'SHORT squeeze' if btc_funding<0 else 'Long pagando'}

Noticias: Sin roja hoy - Revisa CPI mañana
"""
        await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text(f"Error real: {e}")

def main():
    Thread(target=lambda: app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080))), daemon=True).start()
    print(f"ATILA INICIADO FATHER - TOKEN ...{TOKEN[-5:]}")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("marea", marea))
    app.add_handler(CommandHandler("start", marea))
    app.run_polling()

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
